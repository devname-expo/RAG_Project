import os
import time
from pathlib import Path
from pdf_to_docs import get_docs
from docs_to_embeddings import read_docs, upload_embeddings
from inference import answer_question
from pinecone import Pinecone
PINECONE_DEV_KEY = os.environ.get("PINECONE_DEV_KEY")


if __name__ == '__main__':

    pc = Pinecone(api_key=PINECONE_DEV_KEY)
    index_name = 'semantic-search-gemini'
    print(pc.list_indexes().names())
    index = pc.Index(index_name)
    # print(index.describe_index_stats())
    pc.delete_index(index_name)
    time.sleep(5)

    for i,filename in enumerate(["docs/pdfs/Renard R.31 (1) (1).pdf","docs/pdfs/Australia Women's Softball Team (1) (1).pdf"]):
        
        p = Path(filename)
        get_docs(p, f".local/output/docs{i}")     
        upload_embeddings(read_docs(f".local/output/docs{i}.json"), p.stem)
    
    print(answer_question('Which two companies created the R.31 reconnaissance aircraft?'))
    print()
    print()
    print(answer_question('What guns were mounted on the Renard R.31?'))
    print()
    print()
    print(answer_question('Who was the first softball player to represent any country at four World Series of Softball?'))
    print()
    print()
    print(answer_question('Who were the pitchers on the Australian softball team\'s roster at the 2020 Summer Olympics?'))
