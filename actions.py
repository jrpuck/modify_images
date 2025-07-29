import os
from flask import Blueprint, current_app, jsonify, redirect, request, url_for
from PIL import Image


from helpers import doawnload_from_s3, get_secure_filename_filepath

bp = Blueprint('actions', __name__,url_prefix='/actions')

@bp.route('/resize', methods=['POST'])
def resize():
    filename = request.json.get('filename')
    filename, filepath = get_secure_filename_filepath(filename)

    try:
        width, height = request.json.get('width'), request.json.get('height')
        file_stream = doawnload_from_s3(filename)
        image = Image.open(file_stream)
        resized_image = image.resize((width, height))
        resized_image.save(os.path.join(current_app.config['DOWNLOAD_FOLDER'],filename))
        return redirect(url_for('get_image', name=filename))
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404

@bp.route('/presets/<preset>', methods=['POST'])
def presets_image(preset):
    presets = {'small': (100, 100),'medium': (300, 300),'large': (800, 800)}
    if preset not in presets:
        return {'error': 'Preset not found'}, 404 
    filename = request.json.get('filename')
    filename, filepath = get_secure_filename_filepath(filename)
    try:
        image = Image.open(filepath)
        resized_image = image.resize(presets[preset])
        resized_image.save(filepath)
        return redirect(url_for('get_image', name=filename))
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404

@bp.route('/rotate',methods=['POST'])
def rotate():
    filename = request.json.get('filename')
    filename, filepath = get_secure_filename_filepath(filename)

    try:
        angle = float(request.json.get('degree'))
        image = Image.open(filepath)
        rotated_image = image.rotate(angle)
        rotated_image.save(filepath)
        return redirect(url_for('get_image', name=filename))
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404

@bp.route('/flip', methods=['POST'])
def flip(): 
    filename = request.json.get('filename')
    filename, filepath = get_secure_filename_filepath(filename)

    try:
        direction = request.json.get('direction', 'horizontal')
        image = Image.open(filepath)
        if direction == 'horizontal':
            flipped_image = image.transpose(Image.FLIP_LEFT_RIGHT)
        else:
            flipped_image = image.transpose(Image.FLIP_TOP_BOTTOM)
        flipped_image.save(filepath)
        return redirect(url_for('get_image', name=filename))
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404