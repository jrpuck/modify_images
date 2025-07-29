import os
from flask import Blueprint, current_app, jsonify, redirect, request, url_for
from PIL import ImageFilter, Image, ImageEnhance

from helpers import get_secure_filename_filepath,doawnload_from_s3

bp = Blueprint('filters', __name__, url_prefix='/filters')

@bp.route('/blur', methods=['POST'])
def blur():
    filename = request.json.get('filename')
    filename, filepath = get_secure_filename_filepath(filename)
    try:
        radius = int(request.json.get('radius'))
        filestream = doawnload_from_s3(filename)
        image = Image.open(filestream)
        blurred_image = image.filter(ImageFilter.GaussianBlur(radius))
        blurred_image.save(os.path.join(current_app.config['DOWNLOAD_FOLDER'], filename))
        return redirect(url_for('get_image', name=filename))
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404

@bp.route('/contrast', methods=['POST'])
def contrast():
    filename = request.json.get('filename')
    filename, filepath = get_secure_filename_filepath(filename)
    try:
        factor = float(request.json.get('factor', 1.0))
        image = Image.open(filepath)
        enhancer = ImageEnhance.Contrast(image)
        contrasted_image = enhancer.enhance(factor)
        contrasted_image.save(filepath)

        return redirect(url_for('get_image', name=filename))
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404

@bp.route('/brightness', methods=['POST'])
def brightness():   
    filename = request.json.get('filename')
    filename, filepath = get_secure_filename_filepath(filename)
    try:
        factor = float(request.json.get('factor', 1.0))
        image = Image.open(filepath)
        enhancer = ImageEnhance.Brightness(image)
        brightened_image = enhancer.enhance(factor)
        brightened_image.save(filepath)
        return redirect(url_for('get_image', name=filename))
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404