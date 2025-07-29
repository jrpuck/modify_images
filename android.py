import datetime
import os
from os.path import basename
import shutil
from flask import Blueprint, app, current_app, redirect, request, url_for
from PIL import Image
from helpers import doawnload_from_s3, get_secure_filename_filepath
from zipfile import ZipFile
bp = Blueprint('/android',__name__, url_prefix='/android')

Icon_SIZES = [16, 24, 32, 48, 64, 96, 128, 192, 256, 512]


@bp.route('/', methods=['POST'])
def create_image():
    filename = request.json.get('filename')
    filename, filepath = get_secure_filename_filepath(filename)
    
    tempfolder = os.path.join(current_app.config['DOWNLOAD_FOLDER'], 'temp')
    os.makedirs(tempfolder, exist_ok=True)

    for size in Icon_SIZES:
        icon_path = os.path.join(tempfolder, f'{size}.png')
        file_stream = doawnload_from_s3(filename)
        image = Image.open(file_stream)
        image = image.resize((size, size))
        image.save(icon_path, 'PNG')
    
    now  = datetime.datetime.now()
    timesfile = str(datetime.datetime.timestamp(now)).rsplit('.')[0]
    zip_filename = f'{timesfile}.zip'
    zip_filepath = os.path.join(current_app.config['DOWNLOAD_FOLDER'], zip_filename)
    with ZipFile(zip_filepath, 'w') as zipf:
        for foldername, subfolder, filenames in os.walk(tempfolder):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                zipf.write(file_path, basename(file_path))
        shutil.rmtree(tempfolder)
        return redirect(url_for('get_image', name=zip_filename))