from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask import Flask, render_template
from flask_login import login_required, current_user
from apps.data.models import User, Symptom, Criteria, HandPicData, RightHandData, LeftHandData, LargeJointData, FootJointData

app = Flask(__name__)
edit_blueprint = Blueprint('edit_blueprint', __name__, template_folder='templates', static_folder='static')
@edit_blueprint.route('/dashboard', methods=['GET'])
#@login_required  # ログインしているユーザのみアクセス可能
def dashboard():
    # ログイン中のユーザのデータを各テーブルから取得
    symptoms = Symptom.query.filter_by(user_id=current_user.id).all()
    criteria = Criteria.query.filter_by(user_id=current_user.id).all()
    hand_pics = HandPicData.query.filter_by(user_id=current_user.id).all()
    right_hand_data = RightHandData.query.filter_by(user_id=current_user.id).all()
    left_hand_data = LeftHandData.query.filter_by(user_id=current_user.id).all()
    large_joint_data = LargeJointData.query.filter_by(user_id=current_user.id).all()
    foot_joint_data = FootJointData.query.filter_by(user_id=current_user.id).all()

    return render_template('dashboard.html', 
                           symptoms=symptoms, 
                           criteria=criteria,
                           hand_pics=hand_pics,
                           right_hand_data=right_hand_data,
                           left_hand_data=left_hand_data,
                           large_joint_data=large_joint_data,
                           foot_joint_data=foot_joint_data)
