from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
from . import functions

dataset = functions.dataset

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'thisismysecretkeydonotstealit'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main1 import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .models import Recipe

    if not Path('db.sqlite3').exists():
        with app.app_context():
            db.create_all()
            for index in range(len(dataset)):
                toAdd = Recipe(title=dataset['Title'][index],
                               ingredient=dataset['Cleaned_Ingredients'][index],
                               instruction=dataset['Instructions'][index],
                               image=dataset['Image_Name'][index] + ".jpg")
                db.session.add(toAdd)
                db.session.commit()

    return app