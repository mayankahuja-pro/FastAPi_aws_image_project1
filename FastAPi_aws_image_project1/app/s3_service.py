# AWS S3 se interact karne ke liye boto3 library
import boto3
import os
from dotenv import load_dotenv  # .env file se keys padhne ke liye

# .env file load karo taaki AWS keys environment mein aa jayein
load_dotenv()

# AWS S3 client banao - ye S3 se baat karta hai
s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),         # AWS ka access key
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"), # AWS ka secret key
    region_name=os.getenv("AWS_REGION"),                      # S3 bucket ka region
)

# Bucket ka naam .env se lo
BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")


def upload_file_to_s3(file_obj, filename, content_type):
    """
    File ko S3 bucket pe upload karta hai aur public URL return karta hai.
    """
    # S3 pe file upload karo
    s3_client.upload_fileobj(
        file_obj,                              # File ka data
        BUCKET_NAME,                           # Bucket ka naam
        filename,                             # S3 mein file ka naam
        ExtraArgs={"ContentType": content_type},  # File type set karo (image/jpeg etc.)
    )

    # Uploaded file ka public URL banao
    file_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{filename}"
    return file_url  # URL wapas bhejo