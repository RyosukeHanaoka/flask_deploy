from flask import Flask, session
from apps.data.extensions import db, migrate  # migrateが適切にインポートされていることを確認
from flask import Blueprint

