import json
import boto3
import uuid
import os
from datetime import datetime, timezone
import traceback

BUCKET_NAME = os.environ["BUCKET_NAME"]
ALLOWED_FILE_TYPES = ["application/pdf"]
URL_EXPIRATION = 3600

def lambda_handler(event, context):
    print('Starting Lambda')
    try:
        # Parse request body
        body = json.loads(event.get("body", "{}"))
        print(f"Parsed body: {body}")

        # Get filename and content type
        filename = body.get("filename")
        content_type = body.get("contentType")
        print(f"Filename: {filename}, Content Type: {content_type}")

        # Basic validation
        if not filename or not content_type:
            print("Validation failed: missing filename or content type")
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "filename and contentType are required"}),
            }

        if content_type not in ALLOWED_FILE_TYPES:
            print(f"Validation failed: invalid content type {content_type}")
            return {
                "statusCode": 400,
                "body": json.dumps(
                    {"error": f"Content type must be one of: {ALLOWED_FILE_TYPES}"}
                ),
            }

        # Generate a unique file path
        date_prefix = datetime.now(timezone.utc).strftime("%Y/%m/%d")
        file_uuid = str(uuid.uuid4())
        key = f"uploads/{date_prefix}/{file_uuid}/{filename}"
        print(f"Generated key: {key}")

        s3_client = boto3.client(
            "s3",
            region_name="us-east-1",
            config=boto3.session.Config(signature_version="s3v4"),
        )

        # Generate the presigned URL with specific conditions
        presigned_url = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': BUCKET_NAME,
                'Key': key,
                'ContentType': content_type,
                'ACL': 'bucket-owner-full-control'
            },
            ExpiresIn=URL_EXPIRATION,
            HttpMethod='PUT'
        )
        print(f"URL generated successfully: {presigned_url[:100]}...")

        return {
            "statusCode": 200,
            "body": json.dumps({
                "uploadUrl": presigned_url,
                "key": key,
                "expiresIn": URL_EXPIRATION,
                "contentType": content_type
            }),
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST",
            },
        }

    except Exception as e:
        print(f"Unhandled error: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}