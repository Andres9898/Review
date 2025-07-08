import boto3
from botocore.exceptions import NoCredentialsError
from flask import current_app
import os

def upload_file_to_s3(file, filename):
    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY']
        )
        
        bucket_name = current_app.config['S3_BUCKET']
        
        s3.upload_fileobj(
            file,
            bucket_name,
            filename,
            ExtraArgs={
                "ACL": "public-read",
                "ContentType": file.content_type
            }
        )
        
        return f"https://{bucket_name}.s3.amazonaws.com/{filename}"
        
    except NoCredentialsError:
        return None
    except Exception as e:
        print(f"S3 Upload Error: {str(e)}")
        return None