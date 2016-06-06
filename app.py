from datetime import datetime, date

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import exc

__API_VERSION__ = '0.1'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
db = SQLAlchemy(app)

from models import *

def get_object_or_404(model, *criterion):
    try:
        return model.query.filter(*criterion).one()
    except (exc.NoResultFound, exc.MultipleResultsFound) as err:
        abort(404)

class APIGame(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('title', type = str)
        self.parser.add_argument('release_date', type = str)
        self.parser.add_argument('players', type = int)
        self.parser.add_argument('developer', type = str)
        self.parser.add_argument('publisher', type = int)
        self.parser.add_argument('genre', type = int)
        self.parser.add_argument('rating', type = int)
        super(APIGame, self).__init__()

    def get(self, game_id):
        game = Game.query.filter_by(id=game_id).first()
        if not game:
            abort(404)

        return game.to_json()

    def put(self, game_id):
        args = self.parser.parse_args()

        game = Game.query.filter_by(id=game_id).first()
        if not game:
            abort(404)

        for k in args:
            # TODO Update error message
            if k == 'publisher':
                args[k] = get_object_or_404(Publisher, Publisher.id == args[k])
            elif k == 'rating':
                args[k] = get_object_or_404(Rating, Rating.id == args[k])
            elif k == 'genre':
                args[k] = get_object_or_404(Genre, Genre.id == args[k])

            if args[k]:
                setattr(game, k, args[k])

        db.session.commit()


class APIGameList(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('title', type = str, required = True,
            help = 'No game title provided')
        self.parser.add_argument('release_date', type = str, required = True,
            help = 'No game release date provided')
        self.parser.add_argument('players', type = int, default = 1)
        self.parser.add_argument('developer', type = str, default = "Unknown")
        self.parser.add_argument('publisher', type = int, default = 1)
        self.parser.add_argument('genre', type = int, default = 1)
        self.parser.add_argument('rating', type = int, default = 1)
        super(APIGameList, self).__init__()

    def get(self):
        games = [ g.to_json() for g in Game.query.all()]

        return games

    def post(self):
        args = self.parser.parse_args()
        args['release_date'] = datetime.strptime(args['release_date'], "%d/%m/%Y").date()
        args['publisher'] = Publisher.query.filter_by(id=args['publisher']).first()
        args['genre'] = Genre.query.filter_by(id=args['genre']).first()
        args['rating'] = Rating.query.filter_by(id=args['rating']).first()

        game = Game(**args)
        db.session.add(game)
        db.session.commit()

        return game.to_json(), 201

class APIGenre(Resource):
    def get(self, genre_id):
        genre = Genre.query.filter_by(id=genre_id).first()
        if not genre:
            abort(404)

        return genre.to_json()

class APIGenreList(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type = str, required = True,
            help = 'No genre name provided')
        super(APIGenreList, self).__init__()

    def get(self):
        genres = [ g.to_json() for g in Genre.query.all()]

        return genres

    def post(self):
        args = self.parser.parse_args()

        genre = Genre(**args)
        db.session.add(genre)
        db.session.commit()

        return genre.to_json(), 201

class APIPublisher(Resource):
    def get(self, publisher_id):
        publisher = Publisher.query.filter_by(id=publisher_id).first()
        if not publisher:
            abort(404)

        return publisher.to_json()

class APIPublisherList(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type = str, required = True,
            help = 'No publisher name provided')
        super(APIPublisherList, self).__init__()

    def get(self):
        publishers = [ g.to_json() for g in Publisher.query.all()]

        return publishers

    def post(self):
        args = self.parser.parse_args()

        publisher = Publisher(**args)
        db.session.add(publisher)
        db.session.commit()

        return publisher.to_json(), 201

class APIRating(Resource):
    def get(self, rating_id):
        rating = Rating.query.filter_by(id=rating_id).first()
        if not rating:
            abort(404)

        return rating.to_json()

class APIRatingList(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type = str, required = True,
            help = 'No rating name provided')
        super(APIRatingList, self).__init__()

    def get(self):
        ratings = [ g.to_json() for g in Rating.query.all()]

        return ratings

    def post(self):
        args = self.parser.parse_args()

        rating = Rating(**args)
        db.session.add(rating)
        db.session.commit()

        return rating.to_json(), 201

class APIStatus(Resource):
    def get(self):
        return {
            'version': __API_VERSION__,
            'status': 'alive'
        }

api.add_resource(APIStatus, '/status', endpoint='status')
api.add_resource(APIGameList, '/games', endpoint='games')
api.add_resource(APIGame, '/games/<game_id>', endpoint='game')
api.add_resource(APIGenreList, '/genres', endpoint='genres')
api.add_resource(APIGenre, '/genres/<genre_id>', endpoint='genre')
api.add_resource(APIPublisherList, '/publishers', endpoint='publishers')
api.add_resource(APIPublisher, '/publishers/<publisher_id>', endpoint='publisher')
api.add_resource(APIRatingList, '/ratings', endpoint='ratings')
api.add_resource(APIRating, '/ratings/<rating_id>', endpoint='rating')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
