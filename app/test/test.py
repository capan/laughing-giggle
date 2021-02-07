import flask_unittest
import flask.globals
import json
from flask import jsonify

from app.app import create_app


class Test(flask_unittest.ClientTestCase):
    # Assign the `Flask` app object
    app = create_app()
    app.testing = True

    def setUp(self, client):
        # Perform set up before each test, using client
        pass

    def tearDown(self, client):
        # Perform tear down after each test, using client
        pass

    def test_word_list_client(self, client):
        send = {"words": ["adasdas", "dsfdsfds", "cscasd", "assdfe"]}
        # print("Data to send: ", json.dumps(send))
        result = client.post("/api/word-list", data=json.dumps(send))
        decoded = result.data.decode("UTF-8")
        self.assertEquals(decoded,
                          '{\n  "single_string": "adasdas|dsfdsfds|cscasd|assdfe"\n}\n')
