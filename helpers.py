
from flask import current_app

from werkzeug.utils import secure_filename
import os
import boto3, botocore

def allowed_extension(filename):
    """
    Check if the file extension is allowed.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def get_secure_filename_filepath(filename):
    """
    Generate a secure filename and its full path for saving.
    """

    filename = secure_filename(filename)
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    
    return filename, filepath


def upload_to_s3(file, bucket_name, acl = 'public-read'):
    """
    Upload a file to an S3 bucket.
    """
    s3 = boto3.client('s3',aws_access_key_id=current_app.config['S3_KEY'],aws_secret_access_key=current_app.config['S3_SECRET'])
    
    file.filename = secure_filename(file.filename)
    file.path= os.path.join('uploads/', file.filename)

    try:
        s3.upload_fileobj(file, bucket_name, file.path, ExtraArgs={'ACL': acl, 'ContentType': file.content_type})
    except botocore.exceptions.ClientError as e:
        return f"Failed to upload file to S3: {e}"
    return file.filename

def doawnload_from_s3(file_key):
    
    if not os.path.exists(current_app.config['DOWNLOAD_FOLDER']):
        os.makedirs(current_app.config['DOWNLOAD_FOLDER'])
    file_path = os.path.join('uploads/', file_key)
    s3 = boto3.resource('s3',aws_access_key_id=current_app.config['S3_KEY'],aws_secret_access_key=current_app.config['S3_SECRET'])
    bucket = s3.Bucket(current_app.config['S3_BUCKET'])
    s3_object = bucket.Object(file_path)
    response = s3_object.get()
    return response['Body']