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
    USERNAME = os.environ.get('username') 
    PASSWORD = os.environ.get('password') 
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/pictures')

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') 
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')  

    # AWS S3の設定
    S3_BUCKET = os.environ.get("S3_BUCKET_NAME")
    S3_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
    S3_SECRET = os.environ.get("AWS_SECRET_ACCESS_KEY")
    S3_LOCATION = f"http://{S3_BUCKET}.s3.amazonaws.com/"