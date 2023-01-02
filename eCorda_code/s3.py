import os
import boto3
from retry import retry
from io import BytesIO, TextIOWrapper
from application.server.main.logger import get_logger

client = boto3.client(
    's3',
    endpoint_url=os.getenv('S3_ENDPOINT'),
    aws_access_key_id=os.getenv('S3_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('S3_SECRET_KEY'),
    region_name=os.getenv('S3_REGION'),
)

logger = get_logger(__name__)

@retry(delay=2, tries=50, logger=logger)
def upload_object(container: str, filename: str) -> str:
    object_name = f"{os.getenv('CARTABLE_ID')}/{filename.split('/')[-1]}"
    logger.debug(f'Uploading {filename} in {container} as {object_name}')
    data = open(f'{filename}', 'rb')
  
    client.put_object(Key=object_name, Body=data, Bucket=container)
    return f'ok: 1'