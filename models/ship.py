from db import db

class ShipModel(db.Model):
    __tablename__ = 'ships'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    type = db.Column(db.String(80))
    length = db.Column(db.Float)

    def __init__(self, name, type, length):
        self.name = name
        self.type = type
        self.length = length

    def json(self):
        return {'id': self.id, 'name': self.name, 'type': self.type, 'length': self.length}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # @classmethod
    # def find_by_name(cls, name):
    #     connection = sqlite3.connect('data.db')
    #     cursor = connection.cursor()
    #
    #     query = "SELECT * FROM ships WHERE name=?"
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
    #     query = "INSERT INTO ships VALUES(?, ?, ?)"
    #     cursor.execute(query, (self.name, self.type, self.length))
    #
    #     connection.commit()
    #     connection.close()
    #
    #
    # def update(self):
    #     connection = sqlite3.connect('data.db')
    #     cursor = connection.cursor()
    #
    #     query = "UPDATE ships SET type=? WHERE name=? length=?"
    #     cursor.execute(query, (self.type, self.name, self.length))
    #
    #     connection.commit()
    #     connection.close()
