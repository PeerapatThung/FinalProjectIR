from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    instruction = db.Column(db.String(), nullable=False)
    ingredient = db.Column(db.String(), nullable=False)
    image = db.Column(db.String(), nullable=False)

    def get_recipe(self):
        return {
            'id': self.id,
            'title': self.title,
            'instruction': self.instruction,
            'ingredient': self.ingredient,
            'image': self.image
        }

class Favourite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)