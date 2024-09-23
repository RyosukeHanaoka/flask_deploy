import sys
import os

# アプリケーションのディレクトリを追加
sys.path.insert(0, os.path.dirname(__file__))

# Flaskアプリケーションをインポート
from main import app as application