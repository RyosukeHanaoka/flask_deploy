import pytest
from apps.data.extensions import db
from models import User, Symptom, Criteria, HandPicData, RightHandData, LeftHandData, LargeJointData, FootJointData
from werkzeug.security import check_password_hash
from apps.data import create_app


@pytest.fixture(scope='module')
def new_user():
    user = User(email='test@example.com', password='testpassword')
    return user

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('testing')

    # Flaskのアプリケーションコンテキストを作成
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client  # テストの実行

@pytest.fixture(scope='module')
def init_database(test_client):
    # データベースを初期化
    db.create_all()

    # テストデータを追加
    user1 = User(email='test1@example.com', password='password1')
    user2 = User(email='test2@example.com', password='password2')
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    yield db  # テストの実行

    db.drop_all()

def test_new_user(new_user):
    assert new_user.email == 'test@example.com'
    assert new_user.check_password('testpassword')

def test_user_password_hashing(new_user):
    new_user.set_password('newpassword')
    assert new_user.check_password('newpassword')
    assert not new_user.check_password('wrongpassword')
