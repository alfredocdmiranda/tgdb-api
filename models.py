from datetime import date

from app import db

class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    players = db.Column(db.Integer)
    release_date = db.Column(db.Date)
    developer = db.Column(db.String(50))
    publisher = db.Column(db.String(50))

    def __init__(self, *args, **kwargs):
        self.title = kwargs.pop('title')
        self.players = kwargs.pop('players', 1)
        self.release_date = kwargs.pop('release_date')
        self.developer = kwargs.pop('developer', 'Unknown')
        self.publisher = kwargs.pop('publisher', 'Unknown')

    def to_json(self):
        return {'title': self.title,
                'players': self.players,
                'release_date': self.release_date.strftime("%d/%m/%Y"),
                'developer': self.developer,
                'publisher': self.publisher}
