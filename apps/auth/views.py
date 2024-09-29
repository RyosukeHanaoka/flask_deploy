from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user, UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
import random
from apps.data.models import User
from apps.data.extensions import db

login_manager = LoginManager()
auth_blueprint = Blueprint('auth_blueprint', __name__, template_folder='templates', static_folder='static')

from itsdangerous import URLSafeTimedSerializer

# シークレットキーとセキュリティ用のソルト
secret_key = 'your-secret-key'
salt = 'your-salt'
serializer = URLSafeTimedSerializer(secret_key)

# メール設定
mail = Mail()

# ログインマネージャーの設定
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ログインページのルーティング
@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('auth_blueprint.login_success'))
        else:
            return redirect(url_for('auth_blueprint.login_failure'))
    return render_template('login.html')

# ログアウトページのルーティング
@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('logout.html')

# ログイン失敗ページのルーティング
@auth_blueprint.route('/login_failure', methods=['GET', 'POST'])
def login_failure():
    return render_template('login_failure.html')

# ログイン成功ページのルーティング
@auth_blueprint.route('/login_success', methods=['GET', 'POST'])
@login_required
def login_success():
    return render_template('login_success.html')

def generate_reset_token(email):
    return serializer.dumps(email, salt=salt)

def send_reset_password_email(email):
    user = User.query.filter_by(email=email).first()
    if user:
        token = generate_reset_token(user.email)
        reset_url = url_for('auth_blueprint.reset_password_confirm', token=token, _external=True)
        msg = Message('パスワードリセットのリクエスト', 
                      recipients=[email])
        msg.body = f'パスワードリセットのリクエストを受け取りました。以下のリンクをクリックして新しいパスワードを設定してください。\n\n{reset_url}\n\nこのリンクは一定時間のみ有効です。'
        mail.send(msg)

# **新しく追加するエンドポイント**
@auth_blueprint.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form.get('email')
        send_reset_password_email(email)
        flash('パスワードリセットのメールを送信しました。', 'success')
        #return redirect(url_for('auth_blueprint.login'))
    return render_template('reset_password_request.html')

# **既存のエンドポイント名を変更**
@auth_blueprint.route('/reset_password_confirm/<token>', methods=['GET', 'POST'])
def reset_password_confirm(token):
    try:
        email = serializer.loads(token, salt=salt, max_age=3600)
    except:
        flash('無効または期限切れのトークンです。', 'error')
        return redirect(url_for('auth_blueprint.reset_password'))

    if request.method == 'POST':
        new_password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        
        if not new_password or not password_confirm:
            flash('すべてのフィールドを入力してください。', 'error')
            return render_template('reset_password.html')
        
        user = User.query.filter_by(email=email).first()
        if user:
            if new_password != password_confirm:
                flash('パスワードが一致しません。', 'error')
                return render_template('reset_password.html')
            user.password_hash = generate_password_hash(new_password)
            db.session.commit()
            flash('パスワードが正常に更新されました。', 'success')
            return redirect(url_for('auth_blueprint.login'))
    return render_template('reset_password.html')

# サインインページのルーティング
@auth_blueprint.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        password_confirm = request.form['password_confirm']
        if password != password_confirm:
            #return redirect(url_for('auth_blueprint.signin_failure'))
            flash('パスワードが一致しません')
            return render_template('signin.html')
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return redirect(url_for('auth_blueprint.signin_failure'))
        else:
            verification_code = str(random.randint(100000, 999999))
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(email=email, password_hash=hashed_password, verification_code=verification_code)
            db.session.add(new_user)
            db.session.commit()
            send_verification_email(email, verification_code)
            return redirect(url_for('auth_blueprint.verify', user_id=new_user.id))
    return render_template('signin.html')

def send_verification_email(email, code):
    msg = Message('Your Verification Code',
                  sender='braindamage261@gmail.com',
                  recipients=[email])
    msg.body = f'あなたの認証番号: {code}'
    mail.send(msg)

@auth_blueprint.route('/signin_failure', methods=['GET', 'POST'])
def signin_failure():
    return render_template('signin_failure.html')

# ユーザー認証ページのルーティング
@auth_blueprint.route('/verify/<int:user_id>', methods=['GET', 'POST'])
def verify(user_id):
    user = User.query.get(user_id)
    if not user:
        flash('ユーザーが見つかりません', 'error')
        return redirect(url_for('auth_blueprint.signin'))
    
    if request.method == 'POST':
        code = request.form.get('code')
        if code == user.verification_code:
            login_user(user)
            user.is_verified = True
            user.verification_code = None  # コードを使用済みにする
            db.session.commit()
            return redirect(url_for('auth_blueprint.login_success'))
        else:
            return redirect(url_for('auth_blueprint.verification_error'))
    return render_template('verify.html')
