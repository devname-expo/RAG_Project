import json
import boto3
import base64
import logging
from botocore.exceptions import ClientError

levels = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

def create_log(module, log_level='warning'):

    logger = logging.getLogger(module)

    consoleLog = logging.StreamHandler()

    if log_level in levels:
        logger.setLevel(levels[log_level])
        consoleLog.setLevel(levels[log_level])
    else:
        logger.setLevel(levels['warning'])
        consoleLog.setLevel(levels['warning'])

    formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s: %(message)s')  # noqa: E501
    consoleLog.setFormatter(formatter)

    logger.addHandler(consoleLog)
    return logger

def get_secret(secret_name: str, region_name: str = "us-east-1") -> dict:
    """
    Retrieve a secret from AWS Secrets Manager
    
    Args:
        secret_name: Name or ARN of the secret
        region_name: AWS region where the secret is stored
    
    Returns:
        dict: Decrypted secret value
    """
    
    # Create a Secrets Manager client
    try:
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )
    
        # Get the secret value
        response = client.get_secret_value(
            SecretId=secret_name
        )
        
        # Decode and return the secret
        if 'SecretString' in response:
            secret = json.loads(response['SecretString'])
            response  = secret[secret_name]
        else:
            # Handle binary secrets
            binary_secret = base64.b64decode(response['SecretBinary'])
            response =  binary_secret[secret_name]
        
        return response    
    
    except ClientError as e:
        raise e
