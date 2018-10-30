import time
from datetime import date
from flask_restful import Resource, reqparse
from models.slip import SlipModel
# from resources.ship import Ship


class Slip(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('arrival_date',
                        type=str
                        )
    parser.add_argument('current_boat',
                        type=str
                        )

    def get(self, number):
        slip = SlipModel.find_by_number(number)
        if slip:
            return slip.json()
        return {'message': 'Slip not found'}, 404

    def post(self, number):
        if SlipModel.find_by_number(number):
            return {'message': "A slip with number '{}' already exists.".format(number)}, 400
        data = Slip.parser.parse_args()
        if(data['current_boat']):
            data['arrival_date'] = date.today()
            slip = SlipModel(number, **data)
        else:
            slip = SlipModel(number, **data)
        try:
            slip.save_to_db()
        except:
            return {"message": "An error occurred creating the slip."}, 500

        return slip.json(), 201

    def delete(self, number):
        slip = SlipModel.find_by_number(number)
        if slip:
            slip.delete_from_db()
            return {'message': 'Slip deleted'}
        return {'message': 'Slip not found.'}, 404

    def put(self, number):
        data = Slip.parser.parse_args()

        slip = SlipModel.find_by_number(number)

        if slip:
            if(data['current_boat']):
                data['arrival_date'] = date.today()
                slip.current_boat = data['current_boat']
                slip.arrival_date = data['arrival_date']
            else:
                slip.current_boat = data['current_boat']
                slip.arrival_date = data['arrival_date']
        else:
            slip = SlipModel(number, **data)

        slip.save_to_db()

        return slip.json()



class Slips(Resource):
    def get(self):
        return {'slips': list(map(lambda x: x.json(), SlipModel.query.all()))}

    # TABLE_NAME = 'slips'
    #
    # def get(self):
    #     connection = sqlite3.connect('data.db')
    #     cursor = connection.cursor()
    #
    #     query = "SELECT * FROM slips"
    #     result = cursor.execute(query)
    #     ships = []
    #     for row in result:
    #         ships.append({'id': row[0] 'number': row[1], 'current_boat': row[2], 'arrival_date': row[3]})
    #     connection.close()
    #
    #     return {'slips': slips}
