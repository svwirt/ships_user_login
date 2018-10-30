from flask_restful import Resource, reqparse
# from flask_jwt import jwt_required
from models.ship import ShipModel


class Ship(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('type',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('length',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def get(self, name):
        ship = ShipModel.find_by_name(name)
        if ship:
            return ship.json()
        return {'message': 'Ship not found'}, 404


    def post(self, name):
        if ShipModel.find_by_name(name):
            return {'message': "An ship with name '{}' already exists.".format(name)}, 400

        data = Ship.parser.parse_args()

        ship = ShipModel(name, **data)

        try:
            ship.save_to_db()
        except:
            return {"message": "An error occurred inserting the ship."}, 500

        return ship.json(), 201

    def delete(self, name):
        ship = ShipModel.find_by_name(name)
        if ship:
            ship.delete_from_db()
            return {'message': 'Ship deleted.'}
        return {'message': 'Ship not found.'}, 404

    def put(self, name):
        data = Ship.parser.parse_args()

        ship = ShipModel.find_by_name(name)

        if ship:
            ship.type = data['type']
            ship.length = data['length']
        else:
            ship = ShipModel(name, **data)

        ship.save_to_db()

        return ship.json()


class Ships(Resource):
    def get(self):
        return {'ships': list(map(lambda x: x.json(), ShipModel.query.all()))}

    # TABLE_NAME = 'ships'
    #
    # def get(self):
    #     connection = sqlite3.connect('data.db')
    #     cursor = connection.cursor()
    #
    #     query = "SELECT * FROM ships"
    #     result = cursor.execute(query)
    #     ships = []
    #     for row in result:
    #         ships.append({'id': row[0] 'name': row[1], 'type': row[2], 'length': row[3]})
    #     connection.close()
    #
    #     return {'ships': ships}
