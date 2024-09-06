from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from apps.data.models import Symptom, RightHandData, LeftHandData, LargeJointData, FootJointData, LabData, HandPicData
from apps.data.extensions import db
from datetime import datetime
import os
from apps.data.vit import Vit
from . import edit_blueprint

vit = Vit(model_checkpoint='/Users/hanaokaryousuke/flask/apps/data/model.pth')

@edit_blueprint.route('/panel', methods=['GET', 'POST'])
@login_required
def panel():
    pt_ids = db.session.query(Symptom.pt_id).filter_by(user_id=current_user.id).distinct().all()
    pt_ids = [pt_id[0] for pt_id in pt_ids]
    visit_numbers = db.session.query(Symptom.visit_number).filter_by(user_id=current_user.id).distinct().order_by(Symptom.visit_number).all()
    visit_numbers = [visit[0] for visit in visit_numbers]
    
    if request.method == 'POST':
        selected_pt_id = request.form.get('pt_id')
        selected_visit_number = request.form.get('visit_number')
        
        # 選択されたpt_idとvisit_numberに合致するデータが存在するか確認
        existing_data = Symptom.query.filter_by(
            user_id=current_user.id,
            pt_id=selected_pt_id,
            visit_number=selected_visit_number
        ).first()
        
        if existing_data:
            session['pt_id'] = selected_pt_id
            session['visit_number'] = selected_visit_number
            return redirect(url_for('edit_blueprint.edit_symptom', pt_id=selected_pt_id, visit_number=selected_visit_number))
        else:
            error_message = f"患者ID {selected_pt_id} の来院回数 {selected_visit_number} のデータは存在しません。別の組み合わせを選択してください。"
            return redirect(url_for('edit_blueprint.error', error_message=error_message))
    return render_template('panel.html', pt_ids=pt_ids, visit_numbers=visit_numbers)

@edit_blueprint.route('/error')
@login_required
def error():
    error_message = request.args.get('error_message', 'エラーが発生しました。')
    return render_template('error.html', error_message=error_message)

@edit_blueprint.route('/edit_symptom/<int:pt_id>', methods=['GET', 'POST'])
@login_required
def edit_symptom(pt_id):
    symptom = Symptom.query.filter_by(user_id=current_user.id, pt_id=pt_id).order_by(Symptom.created_at.desc()).first_or_404()
    
    if request.method == 'POST':
        symptom.sex = request.form.get('sex', '')
        symptom.pt_id=session.get('pt_id')
        symptom.visit_number=session.get('visit_number')
        symptom.disease_duration = int(request.form.get('disease_duration', 0))
        symptom.morning_stiffness = request.form.get('morning_stiffness', '')
        symptom.six_weeks_duration = request.form.get('six_weeks_duration', '')
        symptom.stiffness_duration = int(request.form.get('stiffness_duration', 0))
        symptom.pain_level = int(request.form.get('pain_level', 0))
        
        db.session.commit()
        flash('症状データが更新されました。', 'success')
        return redirect(url_for('edit_blueprint.edit_righthand', pt_id=pt_id))

    stiffness_durations = [0, 5, 10, 15, 20, 30, 40, 50, 60, 120]

    return render_template('edit_symptom.html', symptom=symptom, stiffness_durations=stiffness_durations, pt_id=pt_id)
    

@edit_blueprint.route('/edit_righthand/<pt_id>', methods=['GET', 'POST'])
@login_required
def edit_righthand(pt_id):
    righthand = RightHandData.query.filter_by(user_id=current_user.id, pt_id=pt_id).order_by(RightHandData.created_at.desc()).first_or_404()
    
    if request.method == 'POST':
        for field in righthand.__table__.columns:
            if field.name in request.form:
                setattr(righthand, field.name, int(request.form.get(field.name, 0)))
        
        db.session.commit()
        flash('右手データが更新されました。', 'success')
        return redirect(url_for('edit_blueprint.edit_lefthand', pt_id=pt_id))

    return render_template('edit_righthand.html', righthand=righthand)

@edit_blueprint.route('/edit_lefthand/<pt_id>', methods=['GET', 'POST'])
@login_required
def edit_lefthand(pt_id):
    lefthand = LeftHandData.query.filter_by(user_id=current_user.id, pt_id=pt_id).order_by(LeftHandData.created_at.desc()).first_or_404()
    
    if request.method == 'POST':
        for field in lefthand.__table__.columns:
            if field.name in request.form:
                setattr(lefthand, field.name, int(request.form.get(field.name, 0)))
        
        db.session.commit()
        flash('左手データが更新されました。', 'success')
        return redirect(url_for('edit_blueprint.edit_body', pt_id=pt_id))

    return render_template('edit_lefthand.html', lefthand=lefthand)

@edit_blueprint.route('/edit_body/<pt_id>', methods=['GET', 'POST'])
@login_required
def edit_body(pt_id):
    body = LargeJointData.query.filter_by(user_id=current_user.id, pt_id=pt_id).order_by(LargeJointData.created_at.desc()).first_or_404()
    
    if request.method == 'POST':
        for field in body.__table__.columns:
            if field.name in request.form:
                setattr(body, field.name, int(request.form.get(field.name, 0)))
        
        db.session.commit()
        flash('体のデータが更新されました。', 'success')
        return redirect(url_for('edit_blueprint.edit_foot', pt_id=pt_id))

    return render_template('edit_body.html', body=body)

@edit_blueprint.route('/edit_foot/<pt_id>', methods=['GET', 'POST'])
@login_required
def edit_foot(pt_id):
    foot = FootJointData.query.filter_by(user_id=current_user.id, pt_id=pt_id).order_by(FootJointData.created_at.desc()).first_or_404()
    
    if request.method == 'POST':
        for field in foot.__table__.columns:
            if field.name in request.form:
                setattr(foot, field.name, int(request.form.get(field.name, 0)))
        
        db.session.commit()
        flash('足のデータが更新されました。', 'success')
        return redirect(url_for('edit_blueprint.edit_labo_exam', pt_id=pt_id))

    return render_template('edit_foot.html', foot=foot)

@edit_blueprint.route('/edit_labo_exam/<pt_id>', methods=['GET', 'POST'])
@login_required
def edit_labo_exam(pt_id):
    labo_exam = LabData.query.filter_by(user_id=current_user.id, pt_id=pt_id).order_by(LabData.created_at.desc()).first_or_404()
    
    if request.method == 'POST':
        labo_exam.crp = float(request.form['crp'])
        labo_exam.esr = int(request.form['esr'])
        labo_exam.rf = float(request.form['rf'])
        labo_exam.acpa = float(request.form['acpa'])
        
        db.session.commit()
        flash('検査結果が更新されました。', 'success')
        return redirect(url_for('edit_blueprint.edit_handpicture', pt_id=pt_id))

    return render_template('edit_labo_exam.html', labo_exam=labo_exam)

@edit_blueprint.route('/edit_handpicture/<pt_id>', methods=['GET', 'POST'])
@login_required
def edit_handpicture(pt_id):
    handpicture = HandPicData.query.filter_by(user_id=current_user.id, pt_id=pt_id).order_by(HandPicData.created_at.desc()).first_or_404()
    
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

            handpicture.datetime = now
            handpicture.right_hand_path = right_path
            handpicture.left_hand_path = left_path
            handpicture.right_hand_result = right_hand_result
            handpicture.left_hand_result = left_hand_result
            handpicture.result = result

            db.session.commit()
            flash('手の写真が更新されました。', 'success')
            return redirect(url_for('edit_blueprint.edit_complete', pt_id=pt_id))
        else:
            flash('右手と左手の写真を両方アップロードしてください。', 'error')

    return render_template('edit_handpicture.html', handpicture=handpicture)

@edit_blueprint.route('/edit_complete/<pt_id>')
@login_required
def complete(pt_id):
    return render_template('edit_complete.html', pt_id=pt_id)