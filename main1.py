from django.core.paginator import Paginator
from flask import Blueprint, render_template, request, jsonify
from flask_cors import cross_origin
from flask_login import login_required, current_user
from .models import Recipe
from . import functions

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/title/<int:page>', methods=['POST','GET'])
@cross_origin(origins=['http://localhost:3000'])
def search_title(page):
    if request.method == 'POST':
        body = request.get_json()
        ranking = functions.query_by_title(body['query'])
        paginator = Paginator(ranking, 10)
        a = list(paginator.page(page))
        for i in range(len(a)):
            print(type(a[i]))
            a[i] = int(a[i])
        print(a)
        a = map(lambda x: x + 1, a)
        result = Recipe.query.filter(Recipe.id.in_(a))
        print(result.all())
        return jsonify({'result': [a.get_recipe() for a in result]})

@main.route('/ingre/<int:page>', methods=['POST','GET'])
@cross_origin(origins=['http://localhost:3000'])
def search_ingredient(page):
    if request.method == 'POST':
        body = request.get_json()
        ranking = functions.query_by_ingredients(body['query'])
        paginator = Paginator(ranking, 10)
        a = list(paginator.page(page))
        for i in range(len(a)):
            print(type(a[i]))
            a[i] = int(a[i])
        print(a)
        a = map(lambda x:x+1, a)
        result = Recipe.query.filter(Recipe.id.in_(a))
        print(result.all())
        return jsonify({'result': [a.get_recipe() for a in result]})

@main.route('/recipes/<int:page>', methods=['GET'])
@cross_origin(origins=['http://localhost:3000'])
def show_all(page):
    if request.method == 'GET':
        result = Recipe.query.paginate(per_page=10, page=page)
        return jsonify({'result': [a.get_recipe() for a in result.items]})