import os

class Config:
    # アプリケーションのディレクトリを基点として絶対パスを設定
    BASEDIR = os.path.abspath(os.path.dirname(__file__))

    # データベースのURI設定
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASEDIR,'instance', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # セキュリティ強化のためのシークレットキー
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-for-development' """os.urandom(24)"""

    # 管理者のユーザー名とパスワードを設定
    USERNAME = os.environ.get('ADMIN_USERNAME') 
    PASSWORD = os.environ.get('ADMIN_PASSWORD') 