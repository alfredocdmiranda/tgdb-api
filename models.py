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
        self.publisher = kwargs.pop('publisher', 1)
        self.genre = kwargs.pop('genre', 1)
        self.rating = kwargs.pop('rating', 1)

    def to_json(self):
        return {'id': self.id,
                'title': self.title,
                'players': self.players,
                'release_date': self.release_date.strftime("%d/%m/%Y"),
                'developer': self.developer,
                'publisher': self.publisher.name,
                'rating': self.rating.name,
                'genre': self.genre.name}

class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15))
    games = db.relationship("Game", back_populates="genre")

    def __init__(self, name):
        self.name = name

    def to_json(self):
        return {'id': self.id,
                'name': self.name}

class Publisher(db.Model):
    __tablename__ = 'publisher'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    games = db.relationship("Game", back_populates="publisher")

    def __init__(self, name):
        self.name = name

    def to_json(self):
        return {'id': self.id,
                'name': self.name}

class Rating(db.Model):
    __tablename__ = 'rating'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15))
    games = db.relationship("Game", back_populates="rating")

    def __init__(self, name):
        self.name = name

    def to_json(self):
        return {'id': self.id,
                'name': self.name}

class Platform(db.Model):
    __tablename__ = 'platform'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15))
    developer_id = db.Column(db.Integer, db.ForeignKey('developer.id'))
    developer = db.relationship("Developer", back_populates="platforms")
    manufacturer_id = db.Column(db.Integer, db.ForeignKey('manufacturer.id'))
    manufacturer = db.relationship("Manufacturer", back_populates="platforms")

    def __init__(self,  *args, **kwargs):
        self.name = kwargs.pop('name')
        self.developer = kwargs.pop('developer')
        self.manufacturer = kwargs.pop('manufacturer')

    def to_json(self):
        return {'id': self.id,
                'name': self.name}

class Developer(db.Model):
    __tablename__ = 'developer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    platforms = db.relationship("Platform", back_populates="developer")

    def __init__(self, name):
        self.name = name

    def to_json(self):
        return {'id': self.id,
                'name': self.name}

class Manufacturer(db.Model):
    __tablename__ = 'manufacturer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    platforms = db.relationship("Platform", back_populates="manufacturer")

    def __init__(self, name):
        self.name = name

    def to_json(self):
        return {'id': self.id,
                'name': self.name}
