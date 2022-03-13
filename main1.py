from django.core.paginator import Paginator
from flask import Blueprint, render_template, request, jsonify
from flask_cors import cross_origin
from flask_login import login_required, current_user
from .models import Recipe, User, Favourite
from . import functions, db

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
        corrections = []
        body = request.get_json()
        ranking, correction = functions.query_by_title(body['query'])
        paginator = Paginator(ranking, 10)
        a = list(paginator.page(page))
        a = map(lambda x: x + 1, a)
        for x in correction:
            if x != body['query']:
                corrections.append(x)
        if corrections:
            return jsonify({'result': [Recipe.query.get(int(x)).get_recipe() for x in a],'total': len(ranking), 'correction': corrections})
        else:
            return jsonify({'result': [Recipe.query.get(int(x)).get_recipe() for x in a],'total': len(ranking)})

@main.route('/ingre/<int:page>', methods=['POST','GET'])
@cross_origin(origins=['http://localhost:3000'])
def search_ingredient(page):
    if request.method == 'POST':
        corrections = []
        body = request.get_json()
        ranking, correction = functions.query_by_ingredients(body['query'])
        paginator = Paginator(ranking, 10)
        a = list(paginator.page(page))
        a = map(lambda x:x+1, a)
        for x in correction:
            if x != body['query']:
                corrections.append(x)
        if corrections:
            return jsonify({'result': [Recipe.query.get(int(x)).get_recipe() for x in a], 'total': len(ranking), 'correction': corrections})
        else:
            return jsonify({'result': [Recipe.query.get(int(x)).get_recipe() for x in a], 'total': len(ranking)})

@main.route('/recipes/<int:page>', methods=['GET'])
@cross_origin(origins=['http://localhost:3000'])
def show_all(page):
    if request.method == 'GET':
        result = Recipe.query.paginate(per_page=10, page=page)
        return jsonify({'result': [a.get_recipe() for a in result.items], 'total': 13493})

@main.route('/recipe/<int:id>', methods=['GET'])
@cross_origin(origins=['http://localhost:3000'])
def show(id):
    if request.method == 'GET':
        result = Recipe.query.get(id)
        return jsonify({'result': result.get_recipe()})

@main.route('/setFav', methods=['POST'])
@cross_origin(origins=['http://localhost:3000'])
def setFav():
    if request.method == 'POST':
        body = request.get_json()
        user = User.query.filter_by(id=body['userid']).first()
        recipe = Recipe.query.filter_by(id=body['recipeid']).first()

        new_fav = Favourite(user_id=user.get_id(), recipe_id=recipe.get_id())

        db.session.add(new_fav)
        db.session.commit()
    return jsonify({'success': 'Marked Successful'})

@main.route('/fav/<int:userid>', methods=['POST','GET'])
@cross_origin(origins=['http://localhost:3000'])
def seeFav(userid):
    if request.method == 'GET':
        fav_list = Favourite.query.filter_by(user_id=userid)
        return jsonify({'result': [a.get_favourite() for a in fav_list]})

@main.route('/showfav/<int:page>', methods=['POST','GET'])
@cross_origin(origins=['http://localhost:3000'])
def showFav(page):
    if request.method == 'POST':
        body = request.get_json()
        total = Favourite.query.filter_by(user_id=body['userid']).all()
        fav_list = Favourite.query.filter_by(user_id=body['userid'])
        fav_list_paginated = fav_list.paginate(per_page=10, page=page)
        itemid = [a.get_favourite() for a in fav_list_paginated.items]

        return jsonify({'result': [Recipe.query.get(int(a)).get_recipe() for a in itemid], 'total': len(total)})

@main.route('/removeFav', methods=['POST'])
@cross_origin(origins=['http://localhost:3000'])
def removeFav():
    if request.method == 'POST':
        body = request.get_json()
        user = User.query.filter_by(id=body['userid']).first()
        recipe = Recipe.query.filter_by(id=body['recipeid']).first()

        Favourite.query.filter_by(user_id=user.get_id(), recipe_id=recipe.get_id()).delete()
        db.session.commit()
    return jsonify({'success': 'Removed Successful'})

@main.route('/searchfav/<int:userid>', methods=['POST','GET'])
@cross_origin(origins=['http://localhost:3000'])
def searchFav(userid):
    if request.method == 'POST':
        corrections = []
        body = request.get_json()
        ranking, correction = functions.query_in_favourite(body['query'], userid)
        for x in correction:
            if x != body['query']:
                corrections.append(x)
        if corrections:
            return jsonify({'result': [Recipe.query.get(int(a)).get_recipe() for a in ranking], 'correction': corrections})
        else:
            return jsonify({'result': [Recipe.query.get(int(a)).get_recipe() for a in ranking]})

@main.route('/recommend', methods=['POST','GET'])
@cross_origin(origins=['http://localhost:3000'])
def recommend():
    if request.method == 'POST':
        body = request.get_json()
        ranking = functions.recommendation(body['query'])
        a = map(lambda x:x+1, ranking)
        return jsonify({'result': [Recipe.query.get(int(x)).get_recipe() for x in a]})


