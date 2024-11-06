import pymupdf4llm
import json
from langchain_text_splitters import MarkdownHeaderTextSplitter
import re
import pathlib

CONTEXT_WINDOW = 2048

def split_by_headers(markdown_text):

    # Regex pattern for markdown headers (supports # through ######)
    header_pattern = r'^#{1,6}\s+(.+?)$'
    title_pattern = r'^#\s+(.+?)$'
    
    # Split the text into lines
    lines = markdown_text.split('\n')
    
    title = ''
    sections = {}
    current_header = None
    current_content = []
    
    for line in lines:

        if not title:
            title_match = re.match(header_pattern, line, re.MULTILINE)
            if title_match:
                title = title_match.group(1)

        # Check if line is a header
        header_match = re.match(header_pattern, line, re.MULTILINE)
        
        if header_match:
            # If we have a previous section, save it
            if current_header is not None:
                sections[current_header] = '\n'.join(current_content).strip()
            
            # Start new section
            current_header = header_match.group(1)
            current_content = []
        else:
            # Add line to current section
            if current_header is not None:
                current_content.append(line)
            else:
                # Handle content before first header
                sections['preamble'] = line if not sections.get('preamble') else sections['preamble'] + '\n' + line
    
    # Save the last section
    if current_header is not None:
        sections[current_header] = '\n'.join(current_content).strip()
    
    return title, sections

def get_section(markdown_text, header_title):

    sections = split_by_headers(markdown_text)
    return sections.get(header_title)

def clean_page_breaks(s):

    # Remove page markers
    s = re.sub(r'\n*-----\n*((\w\s)+\n*)?(\w)',r' \3', s)
    s = re.sub(r'-----','', s)
    s = re.sub(r'\n{3,}','\n\n', s)

    return s

def remove_links(s):
    s = re.sub(r'\[(.*)\]\(http.*\)', r'\1',s)
    
    return s

def remove_references(s):
    s = re.sub(r'\[\[\d{,3}\]\]', ' ',s)
    s = re.sub(r'\[\w\]', '',s)
    return s

def clean_formatting(s):

    s = re.sub(r'_([^_]*)_', r'\1',s)
    s = re.sub(r'\*\*(.*)\*\*', r'\1',s)

    return s

def is_paragraph(text, min_length=100, max_bold_percentage=20):
    # Check minimum length
    if len(text.strip()) < min_length:
        return False
            
    # Check first characters of each line for list patterns
    lines = text.strip().split('\n')
    tracker = {'marker': 0, 'alphabet':0, 'key_value': 0 }
    for line in lines:
        line = line.strip()
        if line:
            # Check for common list markers including alphabetic lists
            if re.match(r'^[\d.)+\-*•◦‣⁃●○⚫]+\s', line):
                tracker['marker'] += 1
            # Check for alphabetic list patterns (A), B), C) or A. B. C. or a. b. c.)
            if re.match(r'^[A-Za-z][\.\)\s]', line):
                tracker['alphabet'] += 1
            # Check for label: value pattern
            if re.match(r'^[^\n:]+:\s', line):
                tracker['key_value'] += 1
    if tracker['marker'] > 1 or \
        tracker['alphabet'] > 1 or \
            tracker['key_value'] > 1:
        return False       
    
    # Check format percentage
    bold_pattern = r'\*\*(.*?)\*\*|__(.*?)__'
    bold_matches = re.findall(bold_pattern, text)
    bold_length = sum(len(match[0] or match[1]) for match in bold_matches)
    clean_text = re.sub(r'\*\*|__', '', text)
    total_length = len(clean_text.strip())
    
    if total_length == 0:
        return False
        
    bold_percentage = (bold_length / total_length) * 100
    if bold_percentage >= max_bold_percentage:
        return False
    
    return True

def clean_paragraph(s):
    
    s = re.sub(r'\n+', ' ',s)
    s = re.sub(r' {2,}', ' ',s)

    return s

def get_docs(filename, outfile, break_on_ref=True):
    # Transform to markdown
    doc = pymupdf4llm.to_markdown(filename)
    doc = clean_page_breaks(doc)

    pathlib.Path("outputcheck.md").write_bytes(doc.encode())

    # Split by subjects
    title, splits = split_by_headers(doc)


    # Format anything descriptive
    ref_found= False
    f_splits = {}
    for header,content in splits.items():

        # formatting

        is_ref = any(header.lower().strip() in ref for ref in {'reference', 'references', 'works cited', 'bibliography', 'works referenced', 'citations'})
        if break_on_ref:
            if is_ref or ref_found:
                break

        sub_sections = splits[header].split('\n\n')
        f_sub_sections = []
        phrase_collector = []
        combined_phrase_size = 0
        for sub in sub_sections:
            
            if is_paragraph(sub):

                # save clean out the phrase collector
                if phrase_collector:
                    f_sub_sections.append('; '.join(phrase_collector))
                    phrase_collector=[]
                
                if not break_on_ref and ref_found: 
                    # just basic cleaning
                    temp = clean_formatting(sub)
                    temp = clean_paragraph(temp)
                    f_sub_sections.append(temp)
                else:
                    # format the paragraph
                    temp = remove_references(sub)
                    temp = clean_formatting(temp)
                    temp = remove_links(temp)

                if len(temp) < CONTEXT_WINDOW:
                    temp = clean_paragraph(temp)
                    f_sub_sections.append(temp)
                else:
                    breaks = temp.split('\n\n')
                    if len(breaks) > 1:
                        for b in breaks:
                            if len(temp) < CONTEXT_WINDOW:
                                temp = clean_paragraph(temp)
                                f_sub_sections.append(temp)
                            else:
                                # will update this later with function call
                                raise Exception("Unexpected size")
                    else:
                        # will update this later with function call
                        raise Exception("Unexpected size")

            else:
                if not break_on_ref and ref_found:
                    # just basic cleaning
                    temp = clean_formatting(sub)
                    phrase_collector.append(temp.replace('\n','; '))
                
                else:
                    temp = remove_references(sub)
                    temp = clean_formatting(temp)
                    temp = remove_links(temp)
                    temp = temp.replace('\n','; ')
                # collect the phrase to be combined with others nearby
                new_size = combined_phrase_size + len(temp)
                if  new_size < CONTEXT_WINDOW:
                    phrase_collector.append(temp)
                else:
                    f_sub_sections.append('; '.join(phrase_collector))
                    phrase_collector=[temp]
        
        # save clean out the phrase collector
        if phrase_collector:
            new_size = combined_phrase_size + len(temp)
            if  new_size < CONTEXT_WINDOW:
                phrase_collector.append(temp)
            else:
                f_sub_sections.append('; '.join(phrase_collector))
                phrase_collector=[temp]

        f_splits[header] = f_sub_sections

    # output = []
    # for header,content in f_splits.items():
    #     output.append(f'{title} {header.upper()}\n\n')
    #     for c in content:
    #         output.append(f'{c}\n\n')
    #     output.append('\n\n\n')

    # pathlib.Path("outputclean.md").write_bytes(''.join(output).encode())

    docs = []
    for section in f_splits[title]:
        docs.append(f'{title}: {section}')

    for header,sections in f_splits.items():
        for section in sections[1:]:
            docs.append(f'{title} {header}: {section}')

    with open(f'{outfile}.json', 'w') as f:
        json.dump(docs, f)

    pathlib.Path(f"{outfile}.txt").write_bytes('\n\n'.join(docs).encode())


if __name__ == '__main__':
    get_docs("src/Processor/Renard R.31 (1) (1).pdf", "docs1")
    get_docs("docs/pdfs/Australia Women's Softball Team (1) (1).pdf", "docs2")