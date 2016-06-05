from datetime import datetime, date

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_sqlalchemy import SQLAlchemy

__API_VERSION__ = '0.1'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app, catch_all_404s=True)
db = SQLAlchemy(app)

from models import *

class APIGame(Resource):
    def get(self, game_id):
        game = Game.query.filter_by(id=game_id).first()
        if not game:
            abort(404)

        return game.to_json()

class APIGameList(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('title', type = str, required = True,
            help = 'No game title provided')
        self.parser.add_argument('release_date', type = str, required = True,
            help = 'No game release date provided')
        self.parser.add_argument('players', type = int, default = 1)
        self.parser.add_argument('developer', type = str, default = "Unknown")
        self.parser.add_argument('publisher', type = str, default = "Unknown")
        super(APIGameList, self).__init__()

    def get(self):
        games = [ g.to_json() for g in Game.query.all()]

        return games

    def post(self):
        args = self.parser.parse_args()
        args['release_date'] = datetime.strptime(args['release_date'], "%d/%m/%Y").date()
        game = Game(**args)
        print(game)
        db.session.add(game)
        db.session.commit()

        return game.to_json(), 201

class APIStatus(Resource):
    def get(self):
        return {
            'version': __API_VERSION__,
            'status': 'alive'
        }

api.add_resource(APIStatus, '/status', endpoint='status')
api.add_resource(APIGameList, '/games', endpoint='games')
api.add_resource(APIGame, '/games/<game_id>', endpoint='game')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
