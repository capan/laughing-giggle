#!/usr/bin/env python
# encoding: utf-8
import json
import os
from flask import Blueprint, Flask, jsonify, request, abort, make_response
import io
import csv
from werkzeug.wrappers import Response
from cerberus import Validator
from datetime import datetime
from random import randint

from app.utils.errors import make_error
mainAPI = Blueprint("api", __name__,  url_prefix="/api")


@mainAPI.route('/word-list', methods=["POST"])
def wordList():
    req_data = json.loads(request.data)
    if(req_data["words"] is None):
        return make_error(400, None, "Query parameters are malformed!", "Check request query parameters! Example: ?word-list=a,b,c")
    else:
        new_word_list = '|'.join(req_data["words"])
        return jsonify({'single_string': new_word_list})


@mainAPI.route('/sum', methods=["POST"])
def sum():
    if request.files:
        si = io.StringIO()
        cw = csv.writer(si)
        cw.writerow(["number 1", "number 2", "answer"])
        uploaded_file = request.files.get("upload")
        lines = uploaded_file.readlines()
        for line in lines:
            decoded_line = line.decode("utf-8")
            decoded_stripped_line = ''.join(decoded_line).strip()
            if decoded_stripped_line:
                try:
                    col1 = decoded_stripped_line.split(",")[0]
                    col2 = decoded_stripped_line.split(",")[1]
                    summ = float(col1) + float(col2)
                    new_csv_row = [col1, col2, summ]
                    cw.writerow(new_csv_row)
                except:
                    new_csv_row = [decoded_stripped_line, "[ERROR]"]
                    cw.writerow(new_csv_row)
            else:
                new_csv_row = decoded_line + "," + "[ERROR]"
                cw.writerow(new_csv_row)
        response = make_response(si.getvalue())
        cd = "attachment; filename=result.csv"
        response.headers['Content-Disposition'] = cd
        response.mimetype = 'text/csv'
        return response
    else:
        return make_error(400, None, "CSV file is required!", "Make sure to send a valid CSV file for summation!")


@mainAPI.route('/pass-gen', methods=["POST"])
def passwordGenerator():
    def to_date(s): return datetime.strptime(s, '%Y-%m-%d')
    req_data = json.loads(request.data)
    user_schema = {
        "first_name": {"type": "string", "minlength": 1, "maxlength": 50},
        "last_name": {"type": "string"},
        "d_o_b": {"type": "datetime", "coerce": to_date},
        "favorite_film": {"type": "string"}
    }
    v = Validator()
    v.schema = user_schema
    if(req_data["user"] is None):
        return make_error(422, None, "User object required!", "Provide a valid user object to request body.")
    else:
        validation = v.validate(req_data["user"], user_schema)
        if(validation):
            fields = ["first_name", "last_name", "d_o_b", "favorite_film"]
            f1 = fields[randint(0, 3)]
            f2 = fields[randint(0, 3)]

            def field_to_rand_str(field, data):
                if(field == "d_o_b"):
                    arr = data[field].split("-")
                    return arr[randint(0, 2)]
                else:
                    s = data[field].strip()
                    s = s.replace(" ", "")
                    s = s.join(s.split())
                    return s
            generatedPassword = field_to_rand_str(
                f1, req_data["user"]) + field_to_rand_str(f2, req_data["user"])
            created_at = datetime.now()
            return jsonify({
                **req_data["user"],
                "password": generatedPassword,
                "created_at": created_at
            })
        else:
            print(v.errors)
            return make_error(422, None, "User object is not valid! Errors: " + json.dumps(v.errors), """Fix your request object!. Sample object: {
                "first_name": "John",
                "last_name": "Smith",
                "d_o_b": "1985-12-04",
                "favorite_film": "Back to the Future"
            }""")
