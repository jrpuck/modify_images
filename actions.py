from flask import Blueprint

bp = Blueprint('actions', __name__,url_prefix='/actions')

@bp.route('/resize', methods=['POST'])
def resize():
    pass

@bp.route('/presets/<preset>', methods=['POST'])
def presets_image(preset):
    pass

@bp.route('/rotate',methods=['POST'])
def rotate():
    pass

@bp.route('/flip', methods=['POST'])
def flip(): 
    pass