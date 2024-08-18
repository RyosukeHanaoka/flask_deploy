from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, session
from flask_login import login_required, current_user
from apps.data.models import Symptom, RightHandData, LeftHandData, LargeJointData, FootJointData, Criteria, HandPicData
from apps.data.extensions import db
from datetime import datetime
import os
from apps.data.vit import Vit

vit = Vit(model_checkpoint='/Users/hanaokaryousuke/flask/apps/data/model.pth')

edit_blueprint = Blueprint('edit_blueprint', __name__, template_folder='edit_templates', static_folder='edit_static')

@edit_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def dashboard():
    object_ids = db.session.query(Symptom.object_id).filter_by(user_id=current_user.id).distinct().all()
    object_ids = [obj_id[0] for obj_id in object_ids]
    
    if request.method == 'POST':
        selected_object_id = request.form.get('object_id')
        return redirect(url_for('edit_blueprint.symptom', object_id=selected_object_id))
    
    return render_template('edit_dashboard.html', object_ids=object_ids)

@edit_blueprint.route('/edit_symptom/<string:object_id>', methods=['GET', 'POST'])
@login_required
def edit_symptom(object_id):
    symptom_data = Symptom.query.filter_by(object_id=object_id, user_id=current_user.id).first()
    
    if request.method == 'POST':
        symptom_data.sex = request.form.get('sex', symptom_data.sex)
        symptom_data.birth_year = int(request.form.get('birth_year', symptom_data.birth_year))
        symptom_data.birth_month = int(request.form.get('birth_month', symptom_data.birth_month))
        symptom_data.birth_day = int(request.form.get('birth_day', symptom_data.birth_day))
        symptom_data.onset_year = int(request.form.get('onset_year', symptom_data.onset_year))
        symptom_data.onset_month = int(request.form.get('onset_month', symptom_data.onset_month))
        symptom_data.onset_day = int(request.form.get('onset_day', symptom_data.onset_day))
        symptom_data.morning_stiffness = request.form.get('morning_stiffness', symptom_data.morning_stiffness)
        symptom_data.six_weeks_duration = request.form.get('six_weeks_duration', symptom_data.six_weeks_duration)
        symptom_data.stiffness_duration = int(request.form.get('stiffness_duration', symptom_data.stiffness_duration))
        symptom_data.pain_level = int(request.form.get('pain_level', symptom_data.pain_level))

        db.session.commit()
        flash('症状データが更新されました！', 'success')
        return redirect(url_for('edit_blueprint.edit_righthand', object_id=object_id))

    years = range(1920, datetime.date.today().year + 1)
    months = range(1, 13)
    days = range(1, 32)
    stiffness_durations = [0, 5, 10, 15, 20, 30, 40, 50, 60, 120]

    return render_template('edit_symptom.html', symptom_data=symptom_data, years=years, months=months, days=days, stiffness_durations=stiffness_durations)

@edit_blueprint.route('/edit_righthand/<string:object_id>', methods=['GET', 'POST'])
@login_required
def edit_righthand(object_id):
    right_hand_data = RightHandData.query.filter_by(object_id=object_id, user_id=current_user.id).first()

    if request.method == 'POST':
        right_hand_data.dip_joint_right_2 = int(request.form.get('dip_joint_right_2', right_hand_data.dip_joint_right_2))
        right_hand_data.dip_joint_right_3 = int(request.form.get('dip_joint_right_3', right_hand_data.dip_joint_right_3))
        right_hand_data.dip_joint_right_4 = int(request.form.get('dip_joint_right_4', right_hand_data.dip_joint_right_4))
        right_hand_data.dip_joint_right_5 = int(request.form.get('dip_joint_right_5', right_hand_data.dip_joint_right_5))
        right_hand_data.thumb_ip_joint_right = int(request.form.get('thumb_ip_joint_right', right_hand_data.thumb_ip_joint_right))
        right_hand_data.pip_joint_right_2 = int(request.form.get('pip_joint_right_2', right_hand_data.pip_joint_right_2))
        right_hand_data.pip_joint_right_3 = int(request.form.get('pip_joint_right_3', right_hand_data.pip_joint_right_3))
        right_hand_data.pip_joint_right_4 = int(request.form.get('pip_joint_right_4', right_hand_data.pip_joint_right_4))
        right_hand_data.pip_joint_right_5 = int(request.form.get('pip_joint_right_5', right_hand_data.pip_joint_right_5))
        right_hand_data.mp_joint_right_1 = int(request.form.get('mp_joint_right_1', right_hand_data.mp_joint_right_1))
        right_hand_data.mp_joint_right_2 = int(request.form.get('mp_joint_right_2', right_hand_data.mp_joint_right_2))
        right_hand_data.mp_joint_right_3 = int(request.form.get('mp_joint_right_3', right_hand_data.mp_joint_right_3))
        right_hand_data.mp_joint_right_4 = int(request.form.get('mp_joint_right_4', right_hand_data.mp_joint_right_4))
        right_hand_data.mp_joint_right_5 = int(request.form.get('mp_joint_right_5', right_hand_data.mp_joint_right_5))

        db.session.commit()
        flash('右手のデータが更新されました！', 'success')
        return redirect(url_for('edit_blueprint.edit_lefthand', object_id=object_id))

    return render_template('edit_righthand.html', right_hand_data=right_hand_data)

@edit_blueprint.route('/edit_lefthand/<string:object_id>', methods=['GET', 'POST'])
@login_required
def edit_lefthand(object_id):
    left_hand_data = LeftHandData.query.filter_by(object_id=object_id, user_id=current_user.id).first()

    if request.method == 'POST':
        left_hand_data.dip_joint_left_2 = int(request.form.get('dip_joint_left_2', left_hand_data.dip_joint_left_2))
        left_hand_data.dip_joint_left_3 = int(request.form.get('dip_joint_left_3', left_hand_data.dip_joint_left_3))
        left_hand_data.dip_joint_left_4 = int(request.form.get('dip_joint_left_4', left_hand_data.dip_joint_left_4))
        left_hand_data.dip_joint_left_5 = int(request.form.get('dip_joint_left_5', left_hand_data.dip_joint_left_5))
        left_hand_data.thumb_ip_joint_left = int(request.form.get('thumb_ip_joint_left', left_hand_data.thumb_ip_joint_left))
        left_hand_data.pip_joint_left_2 = int(request.form.get('pip_joint_left_2', left_hand_data.pip_joint_left_2))
        left_hand_data.pip_joint_left_3 = int(request.form.get('pip_joint_left_3', left_hand_data.pip_joint_left_3))
        left_hand_data.pip_joint_left_4 = int(request.form.get('pip_joint_left_4', left_hand_data.pip_joint_left_4))
        left_hand_data.pip_joint_left_5 = int(request.form.get('pip_joint_left_5', left_hand_data.pip_joint_left_5))
        left_hand_data.mp_joint_left_1 = int(request.form.get('mp_joint_left_1', left_hand_data.mp_joint_left_1))
        left_hand_data.mp_joint_left_2 = int(request.form.get('mp_joint_left_2', left_hand_data.mp_joint_left_2))
        left_hand_data.mp_joint_left_3 = int(request.form.get('mp_joint_left_3', left_hand_data.mp_joint_left_3))
        left_hand_data.mp_joint_left_4 = int(request.form.get('mp_joint_left_4', left_hand_data.mp_joint_left_4))
        left_hand_data.mp_joint_left_5 = int(request.form.get('mp_joint_left_5', left_hand_data.mp_joint_left_5))

        db.session.commit()
        flash('左手のデータが更新されました！', 'success')
        return redirect(url_for('edit_blueprint.edit_body', object_id=object_id))

    return render_template('edit_lefthand.html', left_hand_data=left_hand_data)

@edit_blueprint.route('/edit_body/<string:object_id>', methods=['GET', 'POST'])
@login_required
def edit_body(object_id):
    body_data = LargeJointData.query.filter_by(object_id=object_id, user_id=current_user.id).first()

    if request.method == 'POST':
        body_data.wrist_joint_hand_left = int(request.form.get('wrist_joint_hand_left', body_data.wrist_joint_hand_left))
        body_data.wrist_joint_hand_right = int(request.form.get('wrist_joint_hand_right', body_data.wrist_joint_hand_right))
        body_data.elbow_joint_left = int(request.form.get('elbow_joint_left', body_data.elbow_joint_left))
        body_data.elbow_joint_right = int(request.form.get('elbow_joint_right', body_data.elbow_joint_right))
        body_data.shoulder_joint_left = int(request.form.get('shoulder_joint_left', body_data.shoulder_joint_left))
        body_data.shoulder_joint_right = int(request.form.get('shoulder_joint_right', body_data.shoulder_joint_right))
        body_data.hip_joint_left = int(request.form.get('hip_joint_left', body_data.hip_joint_left))
        body_data.hip_joint_right = int(request.form.get('hip_joint_right', body_data.hip_joint_right))
        body_data.knee_joint_left = int(request.form.get('knee_joint_left', body_data.knee_joint_left))
        body_data.knee_joint_right = int(request.form.get('knee_joint_right', body_data.knee_joint_right))
        body_data.ankle_joint_left = int(request.form.get('ankle_joint_left', body_data.ankle_joint_left))
        body_data.ankle_joint_right = int(request.form.get('ankle_joint_right', body_data.ankle_joint_right))

        db.session.commit()
        flash('体全体のデータが更新されました！', 'success')
        return redirect(url_for('edit_blueprint.edit_foot', object_id=object_id))

    return render_template('edit_body.html', body_data=body_data)

@edit_blueprint.route('/edit_foot/<string:object_id>', methods=['GET', 'POST'])
@login_required
def edit_foot(object_id):
    foot_data = FootJointData.query.filter_by(object_id=object_id, user_id=current_user.id).first()

    if request.method == 'POST':
        foot_data.mtp_joint_left_1 = int(request.form.get('mtp_joint_left_1', foot_data.mtp_joint_left_1))
        foot_data.mtp_joint_left_2 = int(request.form.get('mtp_joint_left_2', foot_data.mtp_joint_left_2))
        foot_data.mtp_joint_left_3 = int(request.form.get('mtp_joint_left_3', foot_data.mtp_joint_left_3))
        foot_data.mtp_joint_left_4 = int(request.form.get('mtp_joint_left_4', foot_data.mtp_joint_left_4))
        foot_data.mtp_joint_left_5 = int(request.form.get('mtp_joint_left_5', foot_data.mtp_joint_left_5))
        foot_data.mtp_joint_right_1 = int(request.form.get('mtp_joint_right_1', foot_data.mtp_joint_right_1))
        foot_data.mtp_joint_right_2 = int(request.form.get('mtp_joint_right_2', foot_data.mtp_joint_right_2))
        foot_data.mtp_joint_right_3 = int(request.form.get('mtp_joint_right_3', foot_data.mtp_joint_right_3))
        foot_data.mtp_joint_right_4 = int(request.form.get('mtp_joint_right_4', foot_data.mtp_joint_right_4))
        foot_data.mtp_joint_right_5 = int(request.form.get('mtp_joint_right_5', foot_data.mtp_joint_right_5))
        foot_data.distal_joints = int(request.form.get('distal_joints', foot_data.distal_joints))
        foot_data.proximal_joints = int(request.form.get('proximal_joints', foot_data.proximal_joints))

        db.session.commit()
        flash('足のデータが更新されました！', 'success')
        return redirect(url_for('edit_blueprint.edit_labo_exam', object_id=object_id))

    return render_template('edit_foot.html', foot_data=foot_data)

@edit_blueprint.route('/edit_labo_exam/<string:object_id>', methods=['GET', 'POST'])
@login_required
def edit_labo_exam(object_id):
    criteria_data = Criteria.query.filter_by(object_id=object_id, user_id=current_user.id).first()

    if request.method == 'POST':
        criteria_data.crp = float(request.form.get('crp', criteria_data.crp))
        criteria_data.esr = int(request.form.get('esr', criteria_data.esr))
        criteria_data.rf = float(request.form.get('rf', criteria_data.rf))
        criteria_data.acpa = float(request.form.get('acpa', criteria_data.acpa))

        db.session.commit()
        flash('検査結果が更新されました！', 'success')
        return redirect(url_for('edit_blueprint.edit_handpicture', object_id=object_id))

    return render_template('edit_labo_exam.html', criteria_data=criteria_data)

@edit_blueprint.route('/edit_handpicture/<string:object_id>', methods=['GET', 'POST'])
@login_required
def edit_handpicture(object_id):
    hand_data = HandPicData.query.filter_by(object_id=object_id, user_id=current_user.id).first()

    if request.method == 'POST':
        right_hand = request.files.get('right_hand')
        left_hand = request.files.get('left_hand')
        if right_hand:
            now = datetime.datetime.now()
            dt_string = now.strftime("%Y%m%d_%H%M%S")
            right_filename = f"{current_user.email}_{dt_string}_right.jpg"
            right_dir = "apps/data/image_righthand"
            os.makedirs(right_dir, exist_ok=True)
            right_path = os.path.join(right_dir, right_filename)
            right_hand.save(right_path)
            hand_data.right_hand_path = right_path
            hand_data.right_hand_result = vit.detect_rheumatoid_arthritis(right_path, hand_data.left_hand_path)
        
        if left_hand:
            now = datetime.datetime.now()
            dt_string = now.strftime("%Y%m%d_%H%M%S")
            left_filename = f"{current_user.email}_{dt_string}_left.jpg"
            left_dir = "apps/data/image_lefthand"
            os.makedirs(left_dir, exist_ok=True)
            left_path = os.path.join(left_dir, left_filename)
            left_hand.save(left_path)
            hand_data.left_hand_path = left_path
            hand_data.left_hand_result = vit.detect_rheumatoid_arthritis(hand_data.right_hand_path, left_path)

        hand_data.result = vit.detect_rheumatoid_arthritis(hand_data.right_hand_path, hand_data.left_hand_path)

        db.session.commit()
        flash('手の画像データが更新されました！', 'success')
        return redirect(url_for('edit_blueprint.select_patient'))

    return render_template('edit_handpicture.html', hand_data=hand_data)
