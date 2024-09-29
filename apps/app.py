from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from apps.auth.views import auth_blueprint, login_manager
from apps.data.views import data_blueprint
from .edit import edit_blueprint
from apps.data.extensions import db, migrate
from apps.settings import Config

def create_app():
    app = Flask(__name__)  # テンプレートフォルダの指定
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config.from_object('apps.settings.Config')  # Configクラスから設定を読み込む

    # データベースとマイグレーションの設定（インポートされたインスタンスを使用）
    db.init_app(app)
    migrate.init_app(app, db)

    # メール機能の設定
    mail = Mail(app)
    app.config.from_object(Config)
    mail.init_app(app)

    # ログインマネージャーの設定
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth_blueprint.login"
    login_manager.login_message = "ログインが必要です"
    
    @login_manager.user_loader
    def load_user(user_id):
        from apps.data.models import User
        return User.query.get(int(user_id))

    # Blueprintを登録
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(data_blueprint, url_prefix='/data')
    app.register_blueprint(edit_blueprint, url_prefix='/edit') 

    return app

#app = create_app()
if __name__ == '__app__':
    app = create_app()
    app.run(debug=True)