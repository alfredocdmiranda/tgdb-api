from datetime import date

from app import db

class Game(db.Model):
    __tablename__ = 'game'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    players = db.Column(db.Integer)
    release_date = db.Column(db.Date)
    developer = db.Column(db.String(50))
    publisher_id = db.Column(db.Integer, db.ForeignKey('publisher.id'))
    publisher = db.relationship("Publisher", back_populates="games")
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))
    genre = db.relationship("Genre", back_populates="games")
    rating_id = db.Column(db.Integer, db.ForeignKey('rating.id'))
    rating = db.relationship("Rating", back_populates="games")

    def __init__(self, *args, **kwargs):
        self.title = kwargs.pop('title')
        self.players = kwargs.pop('players', 1)
        self.release_date = kwargs.pop('release_date')
        self.developer = kwargs.pop('developer', 'Unknown')
        self.publisher = kwargs.pop('publisher', 0)
        self.genre = kwargs.pop('genre', 0)
        self.rating = kwargs.pop('rating', 0)

    def to_json(self):
        return {'title': self.title,
                'players': self.players,
                'release_date': self.release_date.strftime("%d/%m/%Y"),
                'developer': self.developer,
                'publisher': self.publisher}

class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15))
    games = db.relationship("Game", back_populates="genre")

class Publisher(db.Model):
    __tablename__ = 'publisher'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    games = db.relationship("Game", back_populates="publisher")

class Rating(db.Model):
    __tablename__ = 'rating'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15))
    games = db.relationship("Game", back_populates="rating")
