from flask import Flask, request, jsonify, render_template, session
from flask_sqlalchemy import SQLAlchemy
from django.core.paginator import Paginator
from flask_cors import cross_origin
import main as module

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/database.db'
db = SQLAlchemy(app)
# cors = CORS(app, resources={r'/api/*', {'origins': "http://localhost:3000"}})

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
                   instruction=module.dataset['Instructions'][index],
                   image=module.dataset['Image_Name'][index]+".jpg")
    db.session.add(toAdd)
    db.session.commit()

@app.route('/title', methods=['POST','GET'])
@cross_origin(origins=['http://localhost:3000'])
def search_title():
    if request.method == 'POST':
        body = request.get_json()
        return module.query_by_title(body['query'])

@app.route('/ingre/<int:page>', methods=['POST','GET'])
@cross_origin(origins=['http://localhost:3000'])
def search_ingredient(page):
    if request.method == 'POST':
        body = request.get_json()
        ranking = module.query_by_ingredients(body['query'])
        paginator = Paginator(ranking, 10)
        a = list(paginator.page(page))
        for i in range(len(a)):
            print(type(a[i]))
            a[i] = int(a[i])
        print(a)
        a = map(lambda x:x+1, a)
        # a = map(int, a)
        result = Recipe.query.filter(Recipe.id.in_(a))
        print(result.all())
        return jsonify({'result': [a.get_recipe() for a in result]})

@app.route('/recipes/<int:page>', methods=['GET'])
@cross_origin(origins=['http://localhost:3000'])
def show_all(page):
    if request.method == 'GET':
        result = Recipe.query.paginate(per_page=10, page=page)
        return jsonify({'result': [a.get_recipe() for a in result.items]})

@app.route('/hello')
def hello():
    q = request.args.get('q')
    print(q)
    return { "message": "Hello!"}, 201

if __name__ == '__main__':
    app.run()