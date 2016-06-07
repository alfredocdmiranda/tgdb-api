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
        game = get_object_or_404(Game, Game.id == game_id)

        return game.to_json()

    def put(self, game_id):
        args = self.parser.parse_args()

        game = get_object_or_404(Game, Game.id == game_id)
        for k in args:
            if args[k]:
                # TODO Update error message
                if k == 'publisher':
                    args[k] = get_object_or_404(Publisher, Publisher.id == args[k])
                elif k == 'rating':
                    args[k] = get_object_or_404(Rating, Rating.id == args[k])
                elif k == 'genre':
                    args[k] = get_object_or_404(Genre, Genre.id == args[k])

                setattr(game, k, args[k])

        db.session.commit()

        return None, 204

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
        args['publisher'] = get_object_or_404(Publisher, Publisher.id == args['publisher'])
        args['genre'] = get_object_or_404(Genre, Genre.id == args['genre'])
        args['rating'] = get_object_or_404(Rating, Rating.id == args['rating'])

        game = Game(**args)
        db.session.add(game)
        db.session.commit()

        return game.to_json(), 201

class APIGenre(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type = str)
        super(APIGenre, self).__init__()

    def get(self, genre_id):
        genre = get_object_or_404(Genre, Genre.id == genre_id)

        return genre.to_json()

    def put(self, game_id):
        args = self.parser.parse_args()

        genre = get_object_or_404(Genre, Genre.id == genre_id)
        for k in args:
            if args[k]:
                setattr(game, k, args[k])

        db.session.commit()

        return None, 204

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
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type = str)
        super(APIPublisher, self).__init__()

    def get(self, publisher_id):
        publisher = get_object_or_404(Publisher, Publisher.id == publisher_id)

        return publisher.to_json()

    def put(self, game_id):
        args = self.parser.parse_args()

        publisher = get_object_or_404(Publisher, Publisher.id == publisher_id)
        for k in args:
            if args[k]:
                setattr(game, k, args[k])

        db.session.commit()

        return None, 204

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
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type = str)
        super(APIRating, self).__init__()

    def get(self, rating_id):
        rating = get_object_or_404(Rating, Rating.id == rating_id)

        return rating.to_json()

    def put(self, game_id):
        args = self.parser.parse_args()

        rating = get_object_or_404(Rating, Rating.id == rating_id)
        for k in args:
            if args[k]:
                setattr(game, k, args[k])

        db.session.commit()

        return None, 204

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
