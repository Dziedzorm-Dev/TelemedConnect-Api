import base64
import secrets
import string

import boto3
from botocore.exceptions import NoCredentialsError
from flask_jwt_extended import decode_token
from jwt import ExpiredSignatureError, InvalidTokenError
import hashlib
import random
import uuid


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def generate_token():
    return str(uuid.uuid4())


def generate_id():
    alphabet = string.ascii_letters + string.digits
    random_part = ''.join(secrets.choice(alphabet) for _ in range(10))
    uuid_part = base64.urlsafe_b64encode(uuid.uuid4().bytes).decode('utf-8').rstrip('=')[:10]
    unique_str = random_part + uuid_part
    return unique_str


def is_token_expired(token):
    try:
        decode_token(token)
        return False  # Token is valid and not expired
    except ExpiredSignatureError:
        return True  # Token is expired
    except InvalidTokenError:
        return True  # Token is invalid


def upload_to_s3(file_name, file_type, bucket_name, object_name=None):
    """
    Upload a file to an S3 bucket
    :param file_type:
    :param file_name: File to upload
    :param bucket_name: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Initialize a session using Amazon S3
    s3_client = boto3.client('s3')

    try:
        # Upload the file
        s3_client.upload_file(file_name, bucket_name, object_name)
        print(f"File '{file_name}' uploaded to bucket '{bucket_name}' as '{object_name}'.")
        return True
    except FileNotFoundError:
        print(f"The file '{file_name}' was not found.")
        return False
    except NoCredentialsError:
        print("Credentials not available.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

