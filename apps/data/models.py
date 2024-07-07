from datetime import datetime
from .extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = "user"
    #ユーザーのID (主キー)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #ユーザーのメールアドレス (一意制約、非Null制約)
    email = db.Column(db.String(120), unique=True, nullable=False)
    #ハッシュ化されたパスワード
    password_hash = db.Column(db.String(128))
    #ユーザーが作成された日時
    created_at = db.Column(db.DateTime, default=datetime.now)
    #ユーザーが最後に更新された日時
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    #与えられたパスワードをハッシュ化してpassword_hash属性に設定
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    #与えられたパスワードが、保存されているハッシュ値と一致するかチェック
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    #ユーザーIDを文字列として返す (Flask-Loginで必要)
    def get_id(self):
        return str(self.id)
    #ユーザーを表す文字列表現を返す
    def __repr__(self):
        return '<User {}>'.format(self.email)

class Symptom(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sex = db.Column(db.String(10))
    birth_year = db.Column(db.Integer)
    birth_month = db.Column(db.Integer)
    birth_day = db.Column(db.Integer)
    onset_year = db.Column(db.Integer)
    onset_month = db.Column(db.Integer)
    onset_day = db.Column(db.Integer)
    morning_stiffness = db.Column(db.String(50))
    stiffness_duration = db.Column(db.Integer)
    pain_level = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    six_weeks_duration = db.Column(db.Integer)

    def calculate_age(self, current_year, current_month, current_day):
        age = current_year - self.birth_year
        if (current_month, current_day) < (self.birth_month, self.birth_day):
            age -= 1
        return age    