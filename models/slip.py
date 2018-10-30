from datetime import date
from db import db

class SlipModel(db.Model):

    __tablename__ = 'slips'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    arrival_date = db.Column(db.Integer)
    current_boat = db.Column(db.Integer, db.ForeignKey('ships.id'))
    ships = db.relationship('ShipModel', backref='owner')
    # ships = db.relationship('ShipModel')


    def __init__(self, number, arrival_date, current_boat):
        self.number = number
        self.arrival_date = arrival_date
        self.current_boat = current_boat


    def json(self):
        return {'id': self.id, 'number': self.number, 'arrival_date': self.arrival_date, 'current_boat': self.current_boat}

    @classmethod
    def find_by_number(cls, number):
        return cls.query.filter_by(number=number).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # @classmethod
    # def find_by_number(cls, name):
    #     connection = sqlite3.connect('data.db')
    #     cursor = connection.cursor()
    #
    #     query = "SELECT * FROM slips WHERE name=?"
    #     result = cursor.execute(query, (name,))
    #     row = result.fetchone()
    #     connection.close()
    #     if row:
    #         # argument unpacking
    #         return cls(*row)

    #
    # def insert(self):
    #     connection = sqlite3.connect('data.db')
    #     cursor = connection.cursor()
    #
    #     query = "INSERT INTO slips VALUES(?, ?, ?)"
    #     cursor.execute(query, (self.number, self.current_boat, self.arrival_date))
    #
    #     connection.commit()
    #     connection.close()
    #
    #
    # def update(self):
    #     connection = sqlite3.connect('data.db')
    #     cursor = connection.cursor()
    #
    #     query = "UPDATE slips SET number=? WHERE current_boat=? arrival_date=?"
    #     cursor.execute(query, (self.number, self.current_boat, self.arrival_date))
    #
    #     connection.commit()
    #     connection.close()
