import argparse
import requests
from pathlib import Path
import mimetypes

GENERATOR_URL = 'https://kj0317un2f.execute-api.us-east-1.amazonaws.com/Prod/upload'
PROCESSOR_URL = 'temp'

def upload_pdf(pdf_path: str) -> None:
    """
    Upload PDF to S3 using pre-signed URL and trigger processing.
    
    Args:
        pdf_path: Path to local PDF file
    """
    # Validate file exists and is PDF
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {pdf_path}")
        
    content_type, _ = mimetypes.guess_type(pdf_path)
    if content_type != 'application/pdf':
        raise ValueError("File must be a PDF")

    # Get pre-signed URL
    response = requests.post(
        GENERATOR_URL,
        json={
            'filename': path.name,
            'contentType': content_type
        }
    )
    response.raise_for_status()
    data = response.json()
    upload_url = data['uploadUrl']
    file_key = data['key']

    # Upload file to S3 using pre-signed URL
    with open(pdf_path, 'rb') as file:
        print(f"Making request to: {upload_url}")
        print(f"With headers: {{'Content-Type': {content_type}}}")
        response = requests.put(
            upload_url,
            data=file,
            headers={'Content-Type': content_type}
        )
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
        response.raise_for_status()

    # # Trigger processing
    # response = requests.post(
    #     PROCESSOR_URL,
    #     json={'key': file_key}
    # )
    # response.raise_for_status()
    
    # print(f"Upload successful! File key: {file_key}")

def main():
    parser = argparse.ArgumentParser(description='Upload PDF to S3 and trigger processing')
    parser.add_argument('pdf_path', help='Path to the PDF file')
    
    args = parser.parse_args()
    
    try:
        upload_pdf(args.pdf_path)
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)

if __name__ == '__main__':
    main()