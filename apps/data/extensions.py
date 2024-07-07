from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# データベースインスタンスの作成
db = SQLAlchemy()

# マイグレーションインスタンスの作成（この時点ではアプリケーションとバインドされていません）
migrate = Migrate()
