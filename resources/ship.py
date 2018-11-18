from db import db
from flask_restful import Resource, reqparse
from flask_accept import accept
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    jwt_optional,
    get_jwt_identity,
    fresh_jwt_required
)
from models.ship import ShipModel
from models.user import UserModel

class ShipPost(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str
                        )
    parser.add_argument('type',
                        type=str
                        )
    parser.add_argument('length',
                        type=float
                       )
    parser.add_argument('owner',
                        type=str
                       )
    parser.add_argument('self_ship',
                        type=str
                       )


    @jwt_required
    def post(self):
      data = Ship.parser.parse_args()
      name = data['name']
      str1 = "https://ship-user-login.herokuapp.com/"
      str2 = str1 + name
      user_id = get_jwt_identity()
      # user = UserModel(find_by_username())
      if ShipModel.find_by_name(name):
          return {'message': "A ship with name '{}' already exists.".format(name)}, 400

      # data = Ship.parser.parse_args()

      ship = ShipModel(name, data['type'], data['length'], data['owner'],  str2)
      try:
          ship.save_to_db()
      except:
          return {"message": "An error occurred creating the ship."}, 500

      return ship.json(), 201


class Ship(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str
                        )
    parser.add_argument('type',
                        type=str
                        )
    parser.add_argument('length',
                        type=float
                       )
    parser.add_argument('owner',
                        type=str
                       )
    parser.add_argument('self_ship',
                        type=str
                       )


    @jwt_required
    def get(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Owner privilege required'}, 403
        ship = ShipModel.find_by_name(name)
        if ship:
            return ship.json()



    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Owner privilege required'}, 403
        ship = ShipModel.find_by_name(name)
        if ship:
            ship.delete_from_db()
            return {'message': 'ship deleted'}

        return {'message': 'Ship not found.'}, 400

class GetUserShips(Resource):
    @jwt_required
    def get(self, user_id):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Owner privilege required'}, 403
        user =UserModel.find_by_id(user_id)
        if user:
            return user.json()

        return{'message': 'User not found'}, 404



class Ships(Resource):
    def get(self):
        return {'ships': list(map(lambda x: x.json(), ShipModel.query.all()))}
        # user_id = get_jwt_identity()
        # ships = [ship.json() for ship in ShipModel.find_all()]
        # if user_id:
        #     return {'ships': ships}, 200
        # return {'ships': [ship['name'] for ship in ships],
        #         'message': 'More data available if you log in'}, 200
