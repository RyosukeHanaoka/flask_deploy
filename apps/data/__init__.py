from flask import Flask
# from flask_sqlalchemy import SQLAlchemy この行は不要
from .extensions import db, migrate  # migrateが適切にインポートされていることを確認
from flask import Blueprint

from .views import data_blueprint