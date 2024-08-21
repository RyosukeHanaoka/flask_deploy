from flask import Flask, session
from apps.data.extensions import db, migrate  # migrateが適切にインポートされていることを確認
from flask import Blueprint

def create_app(config_name):
    app = Flask(__name__)
    # 必要な設定や拡張機能を設定する
    return app
