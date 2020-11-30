from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_ckeditor import CKEditor
from Zoom.config import Config


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"
ckeditor = CKEditor()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    #init extensions
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    ckeditor.init_app(app)

    #import routes
    from Zoom.main.routes import main
    from Zoom.auth.routes import auth
    from Zoom.post.routes import post
    from Zoom.user.routes import user

    #registre blueprints
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(post)
    app.register_blueprint(user)

    return app