import argparse
import requests
from pathlib import Path
import mimetypes
import json
from typing import Optional, Dict

GENERATOR_URL = 'https://3gde7dimc6.execute-api.us-east-1.amazonaws.com/Prod/upload'
PROCESSOR_URL = 'temp'
INFERENCE_URL = 'https://3gde7dimc6.execute-api.us-east-1.amazonaws.com/Prod/inference'

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

def query_model(question: str) -> Optional[Dict]:
    """
    Query the Lambda endpoint with a question
    
    Args:
        question (str): The question to process
        url (str): The endpoint URL (defaults to test.com/inference)
        
    Returns:
        Optional[Dict]: Response from the server or None if request fails
    """
    try:
        headers = {
            'Content-Type': 'application/json'
        }
        
        payload = {
            'question': question
        }
        
        response = requests.post(
            INFERENCE_URL,
            headers=headers,
            json=payload,
            timeout=60  # 30 second timeout
        )
        
        # Raise an exception for bad status codes
        response.raise_for_status()
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Error querying inference endpoint: {str(e)}")
        return None


def main():
    parser = argparse.ArgumentParser(description='Upload PDF to S3 and trigger processing')
    parser.add_argument('--pdf_path', help='Path to the PDF file')
    parser.add_argument('--query', help='question for the model')
    args = parser.parse_args()
    
    try:
        if args.pdf_path:
            upload_pdf(args.pdf_path)

        if args.query:
            query_model(args.query)
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)

if __name__ == '__main__':
    main()