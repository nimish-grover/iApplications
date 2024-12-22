from flask import make_response,send_from_directory,Blueprint

blp = Blueprint("controllers","controllers")

@blp.route('/sw.js')
def service_worker():
    response = make_response(send_from_directory('static','service-worker.js'))
    return response


@blp.route('/manifest.json')
def manifest():
    return make_response(send_from_directory('static', 'manifest.json'))

@blp.route('/style.css')
def styles():
    response = make_response(send_from_directory('static', 'css/style.css'))
    return response
