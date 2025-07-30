from flask import jsonify


def success_response(data=None, message="Operation successful", status=200):

    response = {
        'success': True,
        'message': message
    }
    if data is not None:
        response['data'] = data
    return jsonify(response)


def error_response(message="An error occurred", status=400):

    response = {
        'success': False,
        'message': message
    }
    return jsonify(response)