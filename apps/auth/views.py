# Flaskの必要なモジュールをインポート
from flask import Blueprint, render_template, request, redirect, url_for, flash
"""Blueprint: アプリケーションの機能を分割するためのクラス
# render_template: テンプレートをレンダリングするための関数
# request: HTTPリクエストを処理するためのオブジェクト
# redirect: 別のURLにリダイレクトするための関数
# url_for: URLを生成するための関数
# flash: フラッシュメッセージを表示するための関数"""

#Flask-Loginの必要なモジュールをインポート
from flask_login import login_required, login_user, logout_user, current_user, UserMixin, LoginManager
"""login_required: ログインが必要なビューを装飾するためのデコレータ
#login_user: ユーザーをログインさせるための関数
#logout_user: ユーザーをログアウトさせるための関数
#current_user: 現在ログインしているユーザーを表すオブジェクト
#UserMixin: ユーザークラスに必要なメソッドを提供するクラス
#LoginManager: ログイン管理を行うためのクラス"""

#Werkzeugのセキュリティ関連のモジュールをインポート
from werkzeug.security import generate_password_hash, check_password_hash
"""generate_password_hash: パスワードをハッシュ化する関数
check_password_hash: ハッシュ化されたパスワードを検証するための関数"""
# クラス"User"をインポート
from apps.data.models import User
# アプリケーションのデータベース拡張機能をインポート
from apps.data.extensions import db
# ログインマネージャーのインスタンスを作成
login_manager = LoginManager()
# Blueprintオブジェクトを作成
auth_blueprint = Blueprint('auth_blueprint', __name__, template_folder='templates', static_folder='static')
# ログインマネージャーの設定
@login_manager.user_loader
# ユーザーIDを元にユーザーオブジェクトを取得する関数
def load_user(user_id):
    # ユーザーIDを受け取り、データベースからユーザーオブジェクトを取得
    return User.query.get(int(user_id))

# ログインページのルーティング
@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    # POSTリクエストの場合、フォームからメールアドレスとパスワードを取得
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # メールアドレスとパスワードが一致するユーザーをデータベースから取得
        user = User.query.filter_by(email=email).first()
        # ユーザーが存在し、パスワードが一致する場合、ログイン処理を行い、データページにリダイレクト
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('data_blueprint.index'))
        else:
            flash('ログイン失敗', 'error')
    return render_template('login.html')

# ログアウトページのルーティング
@auth_blueprint.route('/logout')
@login_required
def logout():
    # ログアウト処理を行い、ログインページにリダイレクト
    logout_user()
    return redirect(url_for('auth_blueprint.login'))

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('登録完了', 'success')
        return redirect(url_for('auth_blueprint.login'))
    return render_template('register.html')

@auth_blueprint.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            # パスワードリセットのメールを送信する処理を実装
            flash('パスワードリセットリンクがメールに送られました。', 'info')
        else:
            flash('メールアドレスが見つかりません', 'error')
    return render_template('reset_password.html')

@auth_blueprint.route('/signin', methods=['GET', 'POST'])
def signin():
    #POSTリクエストの場合、フォームからメールアドレスとパスワードを取得
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # メールアドレスの重複チェックを行い、重複している場合はエラーメッセージを表示してsigninページにリダイレクトする。
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('そのメールアドレスは既に登録されています。', 'error')
            return redirect(url_for('auth_blueprint.signin'))

        # 重複していない場合は、新しいユーザーオブジェクトを作成し、パスワードをハッシュ化してデータベースに保存
        new_user = User(email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        # 登録完了のメッセージを表示し、ログインページにリダイレクトする。
        flash('登録が完了しました。ログインしてください。', 'success')
        return redirect(url_for('auth_blueprint.login'))
    # GETリクエストの場合は、signin.htmlをレンダリングする。
    return render_template('signin.html')