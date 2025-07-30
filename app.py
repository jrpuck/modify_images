import os
from flask import Flask, jsonify, request, send_from_directory
from actions import bp as actions_bp
from filters import bp as filters_bp
from android import bp as android_bp
from helpers import allowed_extension, get_secure_filename_filepath, upload_to_s3
import boto3,botocore
from dotenv import load_dotenv

load_dotenv()

UPLOAD_FOLDER = 'uploads/'
DOWNLOAD_FOLDER = 'downloads/'
app = Flask(__name__)
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

app.config['S3_BUCKET'] = 'images-api-me'
app.config['S3_KEY'] = os.environ.get("AWS_ACCESS_KEY_ID")
app.config['S3_SECRET'] = os.environ.get("AWS_SECRET_ACCESS_KEY")
app.config['S3_LOCATION'] = 'https://images-api-me.s3.eu-west-3.amazonaws.com/uploads/'


app.secret_key ="kjslekro^zel6+"

app.register_blueprint(actions_bp)
app.register_blueprint(filters_bp)
app.register_blueprint(android_bp)

@app.route('/images',methods=['GET','POST'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file was selected'}), 400
        
        file = request.files['file']

        if file.filename =='':
            return jsonify({'error': 'No file was selected'}), 400
        
        if not allowed_extension(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400
        
        #filename,filepath = get_secure_filename_filepath(file.filename)
        
        #file.save(filepath)
        output = upload_to_s3(file, app.config['S3_BUCKET'])
        return jsonify({'message': 'File uploaded successfully', 'filename': output}), 200
    
    images = []
    s3_resource = boto3.resource('s3', aws_access_key_id=app.config['S3_KEY'],
                                 aws_secret_access_key=app.config['S3_SECRET'])
    s3_bucket = s3_resource.Bucket(app.config['S3_BUCKET'])
    for obj in s3_bucket.objects.filter(Prefix='uploads/'):
        if obj.key == 'uploads/':
            continue
        images.append(obj.key)
    return jsonify({"data": images}), 200

@app.route('/downloads/<name>')
def get_image(name):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], name)