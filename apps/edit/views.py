from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from apps.data.models import Symptom, RightHandData, LeftHandData, LargeJointData, FootJointData, Criteria, HandPicData
from apps.data.extensions import db
from datetime import datetime
import os
from apps.data.vit import Vit
from . import edit_blueprint

vit = Vit(model_checkpoint='/Users/hanaokaryousuke/flask/apps/data/model.pth')

@edit_blueprint.route('/test')
def test():
    return "Edit blueprint is working!"

@edit_blueprint.route('/examination')
def examination():
    return render_template('examination.html')

@edit_blueprint.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    object_ids = db.session.query(Symptom.object_id).filter_by(user_id=current_user.id).distinct().all()
    object_ids = [obj_id[0] for obj_id in object_ids]
    
    if request.method == 'POST':
        selected_object_id = request.form.get('object_id')
        return redirect(url_for('edit_blueprint.edit_symptom', object_id=selected_object_id))
    
    return render_template('dashboard.html', object_ids=object_ids)

@edit_blueprint.route('/edit_symptom/<int:object_id>', methods=['GET', 'POST'])
@login_required
def edit_symptom(object_id):
    symptom = Symptom.query.filter_by(user_id=current_user.id, object_id=object_id).order_by(Symptom.created_at.desc()).first_or_404()
    
    if request.method == 'POST':
        symptom.sex = request.form.get('sex', '')
        symptom.birth_year = int(request.form.get('birth_year', 0))
        symptom.birth_month = int(request.form.get('birth_month', 0))
        symptom.birth_day = int(request.form.get('birth_day', 0))
        symptom.onset_year = int(request.form.get('onset_year', 0))
        symptom.onset_month = int(request.form.get('onset_month', 0))
        symptom.onset_day = int(request.form.get('onset_day', 0))
        symptom.morning_stiffness = request.form.get('morning_stiffness', '')
        symptom.six_weeks_duration = request.form.get('six_weeks_duration', '')
        symptom.stiffness_duration = int(request.form.get('stiffness_duration', 0))
        symptom.pain_level = int(request.form.get('pain_level', 0))
        
        db.session.commit()
        flash('症状データが更新されました。', 'success')
        return redirect(url_for('edit_blueprint.edit_righthand', object_id=object_id))

    years = range(1920, datetime.now().year + 1)
    months = range(1, 13)
    days = range(1, 32)
    stiffness_durations = [0, 5, 10, 15, 20, 30, 40, 50, 60, 120]

    return render_template('edit_symptom.html', symptom=symptom, years=years, months=months, days=days, stiffness_durations=stiffness_durations)

@edit_blueprint.route('/edit_righthand/<object_id>', methods=['GET', 'POST'])
@login_required
def edit_righthand(object_id):
    righthand = RightHandData.query.filter_by(user_id=current_user.id, object_id=object_id).order_by(RightHandData.created_at.desc()).first_or_404()
    
    if request.method == 'POST':
        for field in righthand.__table__.columns:
            if field.name in request.form:
                setattr(righthand, field.name, int(request.form.get(field.name, 0)))
        
        db.session.commit()
        flash('右手データが更新されました。', 'success')
        return redirect(url_for('edit_blueprint.edit_lefthand', object_id=object_id))

    return render_template('edit_righthand.html', righthand=righthand)

@edit_blueprint.route('/edit_lefthand/<object_id>', methods=['GET', 'POST'])
@login_required
def edit_lefthand(object_id):
    lefthand = LeftHandData.query.filter_by(user_id=current_user.id, object_id=object_id).order_by(LeftHandData.created_at.desc()).first_or_404()
    
    if request.method == 'POST':
        for field in lefthand.__table__.columns:
            if field.name in request.form:
                setattr(lefthand, field.name, int(request.form.get(field.name, 0)))
        
        db.session.commit()
        flash('左手データが更新されました。', 'success')
        return redirect(url_for('edit_blueprint.edit_body', object_id=object_id))

    return render_template('edit_lefthand.html', lefthand=lefthand)

@edit_blueprint.route('/edit_body/<object_id>', methods=['GET', 'POST'])
@login_required
def edit_body(object_id):
    body = LargeJointData.query.filter_by(user_id=current_user.id, object_id=object_id).order_by(LargeJointData.created_at.desc()).first_or_404()
    
    if request.method == 'POST':
        for field in body.__table__.columns:
            if field.name in request.form:
                setattr(body, field.name, int(request.form.get(field.name, 0)))
        
        db.session.commit()
        flash('体のデータが更新されました。', 'success')
        return redirect(url_for('edit_blueprint.edit_foot', object_id=object_id))

    return render_template('edit_body.html', body=body)

@edit_blueprint.route('/edit_foot/<object_id>', methods=['GET', 'POST'])
@login_required
def edit_foot(object_id):
    foot = FootJointData.query.filter_by(user_id=current_user.id, object_id=object_id).order_by(FootJointData.created_at.desc()).first_or_404()
    
    if request.method == 'POST':
        for field in foot.__table__.columns:
            if field.name in request.form:
                setattr(foot, field.name, int(request.form.get(field.name, 0)))
        
        db.session.commit()
        flash('足のデータが更新されました。', 'success')
        return redirect(url_for('edit_blueprint.edit_labo_exam', object_id=object_id))

    return render_template('edit_foot.html', foot=foot)

@edit_blueprint.route('/edit_labo_exam/<object_id>', methods=['GET', 'POST'])
@login_required
def edit_labo_exam(object_id):
    labo_exam = Criteria.query.filter_by(user_id=current_user.id, object_id=object_id).order_by(Criteria.created_at.desc()).first_or_404()
    
    if request.method == 'POST':
        labo_exam.crp = float(request.form['crp'])
        labo_exam.esr = int(request.form['esr'])
        labo_exam.rf = float(request.form['rf'])
        labo_exam.acpa = float(request.form['acpa'])
        
        db.session.commit()
        flash('検査結果が更新されました。', 'success')
        return redirect(url_for('edit_blueprint.edit_handpicture', object_id=object_id))

    return render_template('edit_labo_exam.html', labo_exam=labo_exam)

@edit_blueprint.route('/edit_handpicture/<object_id>', methods=['GET', 'POST'])
@login_required
def edit_handpicture(object_id):
    handpic = HandPicData.query.filter_by(user_id=current_user.id, object_id=object_id).order_by(HandPicData.created_at.desc()).first_or_404()
    
    if request.method == 'POST':
        right_hand = request.files.get('right_hand')
        left_hand = request.files.get('left_hand')
        
        if right_hand and left_hand:
            now = datetime.now()
            dt_string = now.strftime("%Y%m%d_%H%M%S")
            
            right_filename = f"{current_user.email}_{dt_string}_right.jpg"
            left_filename = f"{current_user.email}_{dt_string}_left.jpg"

            right_dir = "data/pictures/image_righthand"
            left_dir = "data/pictures/image_lefthand"

            os.makedirs(right_dir, exist_ok=True)
            os.makedirs(left_dir, exist_ok=True)

            right_path = os.path.join(right_dir, right_filename)
            left_path = os.path.join(left_dir, left_filename)

            right_hand.save(right_path)
            left_hand.save(left_path)

            result = vit.detect_rheumatoid_arthritis(right_path, left_path)
            right_hand_result = vit.detect_rheumatoid_arthritis(right_path, left_path)
            left_hand_result = vit.detect_rheumatoid_arthritis(right_path, left_path)

            handpic.datetime = now
            handpic.right_hand_path = right_path
            handpic.left_hand_path = left_path
            handpic.right_hand_result = right_hand_result
            handpic.left_hand_result = left_hand_result
            handpic.result = result

            db.session.commit()
            flash('手の写真が更新されました。', 'success')
            return redirect(url_for('edit_blueprint.edit_complete', object_id=object_id))
        else:
            flash('右手と左手の写真を両方アップロードしてください。', 'error')

    return render_template('edit_handpicture.html', handpic=handpic)

@edit_blueprint.route('/edit_complete/<object_id>')
@login_required
def complete(object_id):
    return render_template('edit_complete.html', object_id=object_id)