from db import db
from flask import jsonify, render_template, request
from string import Template
# from models.user import UserModel


class ShipModel(db.Model):
    __tablename__ = 'ships'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    type = db.Column(db.String(80))
    length = db.Column(db.Float)
    owner = db.Column(db.String(80))
    self_ship = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    users = db.relationship('UserModel', back_populates="ships")

    # user_name = db.Column(db.String, db.ForeignKey('users.username'))
    # users = db.relationship('UserModel')


    def __init__(self, name, type, length, owner, self_ship):
        self.name = name
        self.type = type
        self.length = length
        self.owner = owner
        self.self_ship = self_ship


    def json(self):
        return {'id': self.id,
                'name': self.name,
                'type': self.type,
                'length': self.length,
                'owner': self.owner,
                'self': self.self_ship}


    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
