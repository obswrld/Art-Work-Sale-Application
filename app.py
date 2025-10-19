from flask import Flask
from flask_migrate import Migrate
from config.config import db

def create_app():
    apps = Flask(__name__)

    apps.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///artwork_sales.db'
    apps.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    apps.config['SECRET_KEY'] = 'super-secret'

    db.init_app(apps)
    migrate = Migrate(apps, db)

    from controllers.user_controllers import user_info
    apps.register_blueprint(user_info, url_prefix='/user')

    return apps

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)