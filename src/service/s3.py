import boto3
import os
from botocore.exceptions import NoCredentialsError
from typing import Optional

# These should be set in your environment variables
S3_BUCKET = os.getenv("AWS_S3_BUCKET")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")

if not all([S3_BUCKET, AWS_ACCESS_KEY, AWS_SECRET_KEY]):
    print("Warning: AWS S3 credentials or bucket name not found in environment variables.")

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

def upload_file_to_s3(file_content, file_name, content_type) -> Optional[str]:
    """
    Uploads a file to an S3 bucket and returns the public URL.
    """
    try:
        if not S3_BUCKET:
            raise ValueError("S3_BUCKET environment variable is not set")
            
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=file_name,
            Body=file_content,
            ContentType=content_type
        )
        
        url = f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{file_name}"
        return url
    except NoCredentialsError:
        print("Credentials not available")
        return None
    except Exception as e:
        print(f"Error uploading to S3: {e}")
        return None