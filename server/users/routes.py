from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify
from server.users.models import User, users_schema
from server.users.forms import RegistrationFormUser
from pprint import pprint
from server import db
import json

users = Blueprint('users', __name__)


@users.route('/')
def hello_world():
    pprint(request.__dict__)
    # data = db.engine.execute('SELECT * from user')
    # result = [dict(r) for r in data]
    data = User.query.all()
    result = users_schema.dump(data)
    return jsonify(result.data)


@users.route('/create', methods=['POST'])
def create():
    if request.is_json:
        pprint(RegistrationFormUser.__dict__)
        form = RegistrationFormUser(data=request.json)

        return jsonify('MUST BE STRING DUDE')
        # if form.validate_on_submit():

        #     # user = User(username=form.username.data,
        #     #              email=form.email.data, password=hashed_password)
        #     # db.session.add(user)
        #     # db.session.commit()

        #     return jsonify('MUST BE STRING DUDE')
    else:
        return jsonify('MUST BE STRING DUDE')
