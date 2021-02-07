import flask
from flask_cors import CORS
# OR, explicitly providing path to '.env'
from pathlib import Path  # python3 only


from app.api.api import mainAPI
from app.errors.custom_error import CustomError
from app.errors.error_handler import handle_custom_error


def create_app():
    application = flask.Flask(__name__)
    CORS(application, supports_credentials=True)
    application.config["DEBUG"] = True
    application.register_error_handler(CustomError, handle_custom_error)
    application.register_blueprint(mainAPI)
    return application


if __name__ == "__main__":
    application = create_app()
    application.run(host='0.0.0.0')
