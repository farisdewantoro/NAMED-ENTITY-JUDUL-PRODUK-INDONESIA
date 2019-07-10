from datetime import datetime
from server import db, ma
from sqlalchemy import func, TIMESTAMP


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    created_at = db.Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = db.Column(TIMESTAMP(timezone=True), onupdate=func.now())

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return '<User %r>' % self.username


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "username", "email", "created_at", "updated_at")


# Init schema
user_schema = UserSchema(strict=True)
users_schema = UserSchema(many=True, strict=True)
