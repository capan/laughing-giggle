from flask import jsonify
from cerberus import errors


def make_error(status_code, sub_code, message, action):
    response = jsonify({
        'status': status_code,
        'sub_code': sub_code,
        'message': message,
        'action': action
    })
    response.status_code = status_code
    return response


class validation_error_handler(errors.BasicErrorHandler):
    messages = errors.BasicErrorHandler.messages.copy()
    messages[errors.FORBIDDEN_VALUE.code] = "Not Allowed!"
