import wtforms_json
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from server.config import Config
from flask_marshmallow import Marshmallow
from flask_socketio import SocketIO, emit

import os
# from flask_wtf import CSRFProtect
db = SQLAlchemy()
ma = Marshmallow()
# csrf = CSRFProtect()

socketio = SocketIO()

wtforms_json.init()


def server_app(config_class=Config):
    template_dir = os.path.abspath('./client/templates/')
    static_dir = os.path.abspath('./client/static/')
    app = Flask(__name__, static_folder=static_dir,
                template_folder=template_dir)

    app.config.from_object(Config)
    db.init_app(app)
    # csrf.init_app(app)
    ma.init_app(app)
    with app.app_context():
        from server.users.routes import users
        from server.chat.routes import chat
        app.register_blueprint(chat)
        @app.route('/')
        def home():
            return render_template('index.html')

        db.create_all()
        socketio.init_app(app)

    return app
