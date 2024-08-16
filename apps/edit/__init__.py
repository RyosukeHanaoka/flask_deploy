from flask import Flask
# from flask_sqlalchemy import SQLAlchemy この行は不要
from apps.data.extensions import db, migrate  # migrateが適切にインポートされていることを確認
from flask import Blueprint

from apps.data.views import data_blueprint
from apps.edit.views import edit_blueprint