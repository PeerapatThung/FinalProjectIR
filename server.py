from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import cross_origin
import main as module

app = Flask(__name__)
db = SQLAlchemy(app)
# cors = CORS(app, resources={r'/api/*', {'origins': "http://localhost:3000"}})

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    instruction = db.Column(db.String(), nullable=False)
    ingredient = db.Column(db.String(), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(), nullable=False)

    favourite_id = db.Column(db.Integer, db.ForeignKey('favourite.id'), nullable=True)
    favourite = db.relationship('Favourite', backref=db.backref('favourite', lazy=True))

class Favourite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    recipe = db.relationship('Recipe', backref=db.backref('recipe', lazy=True))

db.create_all()
for index in range(len(module.dataset)):
    toAdd = Recipe(title=module.dataset['Title'][index],
                   ingredient=module.dataset['Cleaned_Ingredients'][index],
                   instruction=module.dataset['Instructions'][index])
    db.session.add(toAdd)
    db.session.commit()

print(Recipe.query.all())

@app.route('/title', methods=['POST','GET'])
@cross_origin(origins=['http://localhost:3000'])
def search_title():
    if request.method == 'POST':
        body = request.get_json()
        return module.query_by_title(body['query'])

@app.route('/ingre', methods=['POST','GET'])
@cross_origin(origins=['http://localhost:3000'])
def search_ingredient():
    if request.method == 'POST':
        body = request.get_json()
        return module.query_by_ingredients(body['query'])

@app.route('/hello')
def hello():
    q = request.args.get('q')
    print(q)
    return { "message": "Hello!"}, 201

if __name__ == '__main__':
    app.run()