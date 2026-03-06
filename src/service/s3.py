import boto3
import os
from botocore.exceptions import NoCredentialsError
from typing import Optional

# These should be set in your environment variables
S3_BUCKET = os.getenv("AWS_S3_BUCKET")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

# def upload_file_to_s3(file_content, file_name, content_type) -> Optional[str]:
#     """
#     Uploads a file to an S3 bucket and returns the public URL.
#     """
#     try:
#         s3_client.put_object(
#             Bucket=S3_BUCKET,
#             Key=file_name,
#             Body=file_content,
#             ContentType=content_type,
#             # ACL='public-read' # Uncomment if your bucket allows public-read ACL
#         )
        
#         url = f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{file_name}"
#         return url
#     except NoCredentialsError:
#         print("Credentials not available")
#         return None
#     except Exception as e:
#         print(f"Error uploading to S3: {e}")
#         return None

def upload_file_to_s3(file_content, file_name, content_type):
    try:
        bucket = os.getenv("AWS_S3_BUCKET")

        s3_client.put_object(
            Bucket=bucket,
            Key=file_name,
            Body=file_content,
            ContentType=content_type
        )

        url = f"https://{bucket}.s3.{os.getenv('AWS_REGION')}.amazonaws.com/{file_name}"
        return url

    except Exception as e:
        print("Error uploading to S3:", e)
        return None