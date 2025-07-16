
from flask import current_app

from werkzeug.utils import secure_filename
import os

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