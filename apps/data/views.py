from flask import Blueprint, abort, render_template, request, redirect, url_for, flash, current_app, jsonify, session
from flask_login import login_required, current_user
from .extensions import db
from sqlalchemy import func
import datetime
import os
from .models import HandPicData, RightHandData, LeftHandData, LargeJointData, FootJointData
from .models import Symptom, LabData, ScoreData
from .vit import Vit
#vit=Vit(model_checkpoint='/Users/hanaokaryousuke/flask/apps/data/model.pth')
data_blueprint = Blueprint('data_blueprint', __name__, template_folder='templates', static_folder='static')


@data_blueprint.route('/index', methods=['GET', 'POST'])
def index():
    lang = request.args.get('lang', 'ja')
    if lang == 'en':
        return render_template('index_en.html')
    else:
        return render_template('index.html')

@data_blueprint.route('/notice', methods=['GET', 'POST'])
def notice():
    if request.method == 'POST':
        return redirect(url_for('data.symptom'))
    return render_template('notice.html')

@data_blueprint.route('/notice_post_login', methods=['GET', 'POST'])
@login_required
def notice_post_login():
    if request.method == 'POST':
        return redirect(url_for('data.symptom'))
    return render_template('notice_post_login.html')

@data_blueprint.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        visit_number = int(request.form.get('visit_number'))
        pt_id=str(request.form.get('pt_id'))
        existing_record = Symptom.query.filter_by(pt_id=pt_id, visit_number=visit_number).first()        
        if existing_record:
                    return redirect(url_for('data_blueprint.error', 
                                            error_message='そのデータはすでに存在します。別の患者IDまたは来院回数を選択してください。'))
        else:
            session['pt_id'] = pt_id
            session['visit_number'] = visit_number
            return redirect(url_for('data_blueprint.symptom'))
    
    visit_numbers = range(1, 6)
    return render_template('dashboard.html', visit_numbers=visit_numbers)

@data_blueprint.route('/error')
def error():
    error_message = request.args.get('error_message', 'エラーが発生しました。')
    return render_template('error.html', error_message=error_message)

@data_blueprint.route('/value_defect')
def value_defect():
    error_message = request.args.get('error_message', 'エラーが発生しました。')
    return render_template('value_defect.html', error_message=error_message)

@data_blueprint.route('/symptom', methods=['GET', 'POST'])
@login_required
def symptom():
    if request.method == 'POST':
        errors = []

        # 必須フィールドのチェック
        required_fields = {
            'sex': '性別',
            'birth_date': '生年月日',
            'disease_duration': '罹病期間',
            'morning_stiffness': '朝のこわばりの有無',
            'six_weeks_duration': '6週間以上の症状持続',
            'stiffness_duration': 'こわばりの持続時間',
            'pain_level': '痛みのレベル'
        }

        for field, name in required_fields.items():
            if not request.form.get(field):
                errors.append(f'{name}が入力されていません。')

        # pt_idとvisit_numberのチェック
        if not session.get('pt_id'):
            errors.append('患者IDが設定されていません。')
        if not session.get('visit_number'):
            errors.append('来院回数が設定されていません。')

        if errors:
            error_message = "以下の項目が未入力です：" + ", ".join(errors)
            return render_template('value_defect.html', errors=errors, error_message=error_message)
            #return render_template('error.html', errors=errors, error_message=error_message)

        try:
            user = Symptom(
                sex=request.form.get('sex'),
                user_id=current_user.id,
                pt_id=session.get('pt_id'),
                visit_number=session.get('visit_number'),
                birth_date=request.form.get('birth_date'),
                disease_duration=int(request.form.get('disease_duration')),
                morning_stiffness=request.form.get('morning_stiffness'),
                six_weeks_duration=request.form.get('six_weeks_duration'),
                stiffness_duration=int(request.form.get('stiffness_duration')),
                pain_level=int(request.form.get('pain_level'))       
            )        
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('data_blueprint.righthand'))
        except Exception as e:
            db.session.rollback()
            error_message = 'データの保存中にエラーが発生しました。' + str(e)
            return render_template('error.html', error_message=error_message)

    years = range(1930, datetime.date.today().year + 1)
    months = range(1, 13)
    days = range(1, 32)
    stiffness_durations = [0, 5, 10, 15, 20, 30, 40, 50, 60, 120]

    return render_template('symptom.html', years=years, months=months, days=days, stiffness_durations=stiffness_durations)

@data_blueprint.route('/righthand', methods=['GET', 'POST'])
@login_required
def righthand():
    if request.method == 'POST':
        print(request.form)
        data=request.form
        pt_id = session.get('pt_id')
        joint_entry = RightHandData(
            pt_id = pt_id,
            user_id=current_user.id,
            visit_number = session.get('visit_number'),
            dip_joint_right_2=int(data.get('dip_joint_right_2', 0)),
            dip_joint_right_3=int(data.get('dip_joint_right_3', 0)),
            dip_joint_right_4=int(data.get('dip_joint_right_4', 0)),
            dip_joint_right_5=int(data.get('dip_joint_right_5', 0)),
            thumb_ip_joint_right=int(data.get('thumb_ip_joint_right', 0)),
            pip_joint_right_2=int(data.get('pip_joint_right_2', 0)),
            pip_joint_right_3=int(data.get('pip_joint_right_3', 0)),
            pip_joint_right_4=int(data.get('pip_joint_right_4', 0)),
            pip_joint_right_5=int(data.get('pip_joint_right_5', 0)),
            mp_joint_right_1=int(data.get('mp_joint_right_1', 0)),
            mp_joint_right_2=int(data.get('mp_joint_right_2', 0)),
            mp_joint_right_3=int(data.get('mp_joint_right_3', 0)),
            mp_joint_right_4=int(data.get('mp_joint_right_4', 0)),
            mp_joint_right_5=int(data.get('mp_joint_right_5', 0)),
        )
        db.session.add(joint_entry)
        db.session.commit()

        return redirect(url_for('data_blueprint.lefthand'))
    return render_template('righthand.html')

@data_blueprint.route('/lefthand', methods=['GET', 'POST'])
@login_required
def lefthand():
    if request.method == 'POST':
        data=request.form
        pt_id = session.get('pt_id')
        joint_entry = LeftHandData(
            pt_id = pt_id,
            user_id=current_user.id,
            visit_number = session.get('visit_number'),
            dip_joint_left_2=int(data.get('dip_joint_left_2', 0)),
            dip_joint_left_3=int(data.get('dip_joint_left_3', 0)),
            dip_joint_left_4=int(data.get('dip_joint_left_4', 0)),
            dip_joint_left_5=int(data.get('dip_joint_left_5', 0)),
            thumb_ip_joint_left=int(data.get('thumb_ip_joint_left', 0)),
            pip_joint_left_2=int(data.get('pip_joint_left_2', 0)),
            pip_joint_left_3=int(data.get('pip_joint_left_3', 0)),
            pip_joint_left_4=int(data.get('pip_joint_left_4', 0)),
            pip_joint_left_5=int(data.get('pip_joint_left_5', 0)),
            mp_joint_left_1=int(data.get('mp_joint_left_1', 0)),
            mp_joint_left_2=int(data.get('mp_joint_left_2', 0)),
            mp_joint_left_3=int(data.get('mp_joint_left_3', 0)),
            mp_joint_left_4=int(data.get('mp_joint_left_4', 0)),
            mp_joint_left_5=int(data.get('mp_joint_left_5', 0)),
        )
        db.session.add(joint_entry)
        db.session.commit()

        return redirect(url_for('data_blueprint.body'))
    return render_template('lefthand.html')

@data_blueprint.route('/body', methods=['GET', 'POST'])
@login_required
def body():
    if request.method == 'POST':
        data=request.form
        pt_id = session.get('pt_id')
        joint_entry = LargeJointData(
            pt_id = pt_id,
            user_id=current_user.id,
            visit_number = session.get('visit_number'),
            wrist_joint_hand_left=int(data.get('wrist_joint_hand_left', 0)),
            wrist_joint_hand_right=int(data.get('wrist_joint_hand_right', 0)),
            elbow_joint_left=int(data.get('elbow_joint_left', 0)),
            elbow_joint_right=int(data.get('elbow_joint_right', 0)),
            shoulder_joint_left=int(data.get('shoulder_joint_left', 0)),
            shoulder_joint_right=int(data.get('shoulder_joint_right', 0)),
            hip_joint_left=int(data.get('hip_joint_left', 0)),
            hip_joint_right=int(data.get('hip_joint_right', 0)),
            knee_joint_left=int(data.get('knee_joint_left', 0)),
            knee_joint_right=int(data.get('knee_joint_right', 0)),
            ankle_joint_left=int(data.get('ankle_joint_left', 0)),
            ankle_joint_right=int(data.get('ankle_joint_right', 0)),
            sternoclavicular_joint_left=int(data.get('sternoclavicular_joint_left', 0)),
            sternoclavicular_joint_right=int(data.get('sternoclavicular_joint_right', 0)),
            acromioclavicular_joint_left=int(data.get('acromioclavicular_joint_left', 0)),
            acromioclavicular_joint_right=int(data.get('acromioclavicular_joint_right', 0)),
            temporomandibular_joint_left=int(data.get('temporomandibular_joint_left', 0)),
            temporomandibular_joint_right=int(data.get('temporomandibular_joint_right', 0))
        )
        db.session.add(joint_entry)
        db.session.commit()

        return redirect(url_for('data_blueprint.foot'))
    return render_template('body.html')

@data_blueprint.route('/foot', methods=['GET', 'POST'])
@login_required
def foot():
    if request.method == 'POST':
        data=request.form
        pt_id = session.get('pt_id')
        joint_entry = FootJointData(
            pt_id = pt_id,
            user_id=current_user.id,
            visit_number = session.get('visit_number'),
            mtp_joint_left_1=int(data.get('mtp_joint_left_1', 0)),
            mtp_joint_left_2=int(data.get('mtp_joint_left_2', 0)),
            mtp_joint_left_3=int(data.get('mtp_joint_left_3', 0)),
            mtp_joint_left_4=int(data.get('mtp_joint_left_4', 0)),
            mtp_joint_left_5=int(data.get('mtp_joint_left_5', 0)),
            mtp_joint_right_1=int(data.get('mtp_joint_right_1', 0)),
            mtp_joint_right_2=int(data.get('mtp_joint_right_2', 0)),
            mtp_joint_right_3=int(data.get('mtp_joint_right_3', 0)),
            mtp_joint_right_4=int(data.get('mtp_joint_right_4', 0)),
            mtp_joint_right_5=int(data.get('mtp_joint_right_5', 0)),
            distal_joints=int(data.get('distal_joints', 0)),
            proximal_joints=int(data.get('proximal_joints', 0))
        )
        db.session.add(joint_entry)
        db.session.commit()

        return redirect(url_for('data_blueprint.labo_exam'))
    return render_template('foot.html')

@data_blueprint.route('/labo_exam', methods=['GET', 'POST'])
@login_required
def labo_exam():
    if request.method == 'POST':
        try:
            # フォームからデータを取得
            user_id = current_user.id
            pt_id = session.get('pt_id')
            visit_number = session.get('visit_number')
            crp = float(request.form['crp'])
            esr = int(request.form['esr'])
            rf = float(request.form['rf'])
            acpa = float(request.form['acpa'])
        
            # データベースに保存
            labo_data = LabData(
                pt_id=pt_id,
                user_id=user_id,
                visit_number=visit_number,
                crp=crp,
                esr=esr,
                rf=rf,
                acpa=acpa,
            )
            db.session.add(labo_data)
            db.session.commit()

            return redirect(url_for('data_blueprint.handpicture'))
        except Exception as e:
            # エラーハンドリング
            db.session.rollback()
            error_message = f'データの保存中にエラーが発生しました: {str(e)}'
            return redirect(url_for('data_blueprint.labo_defect', error_message=error_message))

    # GETリクエストの場合
    return render_template('labo_exam.html')

@data_blueprint.route('/labo_defect')
def labo_defect():
    error_message = request.args.get('error_message', 'エラーが発生しました。')
    return render_template('labo_defect.html', error_message=error_message)

#以下は本番環境でハイブリッドアーキテクチャを使用する場合に使用するコード
import requests  # 自宅PCにHTTPリクエストを送信するために必要
PREDICTION_SERVER_URL = 'http://58.90.145.44:51015/predict'

@data_blueprint.route('/handpicture', methods=['GET', 'POST'])
@login_required
def handpicture():
    if request.method == 'POST':
        pt_id = session.get('pt_id')

        # フォームから送信されたファイルの取得
        right_hand = request.files.get('right_hand')
        left_hand = request.files.get('left_hand')
        if not right_hand or not left_hand:
            abort(400, description="Missing 'right_hand' or 'left_hand' file in request")

        now = datetime.datetime.now()
        dt_string = now.strftime("%Y%m%d_%H%M%S")
        right_filename = f"{current_user.email}_{dt_string}_right.jpg"
        left_filename = f"{current_user.email}_{dt_string}_left.jpg"

        right_dir = "data/pictures/image_righthand"
        left_dir = "data/pictures/image_lefthand"
        os.makedirs(right_dir, exist_ok=True)
        os.makedirs(left_dir, exist_ok=True)

        right_path = os.path.join(right_dir, right_filename)
        left_path = os.path.join(left_dir, left_filename)

        # 画像ファイルの保存
        right_hand.save(right_path)
        left_hand.save(left_path)

        # 自宅PCのサーバーにPOSTリクエストで画像を送信
        with open(right_path, 'rb') as rf, open(left_path, 'rb') as lf:
            files = {
                'right_hand': rf,
                'left_hand': lf
            }
            try:
                response = requests.post(PREDICTION_SERVER_URL, files=files)
                response.raise_for_status()  # エラーがあれば例外を発生させる
            except requests.exceptions.RequestException as e:
                flash(f'Prediction server error: {e}', 'danger')
                return redirect(url_for('data_blueprint.handpicture'))

        # 自宅PCからの推論結果を取得
        results = response.json()
        right_hand_result = results.get('right_hand_result')
        left_hand_result = results.get('left_hand_result')
        result = results.get('result')

        hand_data = HandPicData(
            user_id=current_user.id,
            pt_id=pt_id,
            visit_number=session.get('visit_number'),
            datetime=now,
            right_hand_path=right_path,
            left_hand_path=left_path,
            right_hand_result=right_hand_result,
            left_hand_result=left_hand_result,
            result=result
        )
        db.session.add(hand_data)
        db.session.commit()

        session['result'] = result
        return redirect(url_for('data_blueprint.scoring'))

    return render_template('handpicture.html')

@data_blueprint.route('/ptresult', methods=['GET', 'POST'])
@login_required
def ptresult():
    # セッションから検出結果を取得
    result = session.get('result')
    result = round(result, 2)
    #セッションに結果が保存されていない場合、HTTP 400エラーを返す
    if result is None:
        abort(400, description="結果が見つかりません")
    
    # 結果を表示する
    return render_template('ptresult.html', result=result)

@data_blueprint.route('/scoring', methods=['GET', 'POST'])
@login_required
def scoring():
    try:
        pt_id = session.get('pt_id')
        visit_number = session.get('visit_number')
        if pt_id is None or visit_number is None:
            raise ValueError("Patient ID or Visit Number not found in session")

        def get_latest_sum(model, pt_id, *columns):
            subq = db.session.query(
                func.max(model.created_at).label('max_date')
            ).filter(model.pt_id == pt_id).subquery()

            return db.session.query(
                func.coalesce(sum(column for column in columns), 0)
            ).filter(
                model.pt_id == pt_id,
                model.visit_number == visit_number
            ).scalar()

        # distal_jointsの計算（前回の改善を維持）
        distal_joints = (
            get_latest_sum(RightHandData, pt_id,
                           RightHandData.thumb_ip_joint_right,
                           RightHandData.pip_joint_right_2,
                           RightHandData.pip_joint_right_3,
                           RightHandData.pip_joint_right_4,
                           RightHandData.pip_joint_right_5,
                           RightHandData.mp_joint_right_1,
                           RightHandData.mp_joint_right_2,
                           RightHandData.mp_joint_right_3,
                           RightHandData.mp_joint_right_4,
                           RightHandData.mp_joint_right_5) +
            get_latest_sum(LeftHandData, pt_id,
                           LeftHandData.thumb_ip_joint_left,
                           LeftHandData.pip_joint_left_2,
                           LeftHandData.pip_joint_left_3,
                           LeftHandData.pip_joint_left_4,
                           LeftHandData.pip_joint_left_5,
                           LeftHandData.mp_joint_left_1,
                           LeftHandData.mp_joint_left_2,
                           LeftHandData.mp_joint_left_3,
                           LeftHandData.mp_joint_left_4,
                           LeftHandData.mp_joint_left_5) +
            get_latest_sum(LargeJointData, pt_id,
                           LargeJointData.wrist_joint_hand_left,
                           LargeJointData.wrist_joint_hand_right) +
            get_latest_sum(FootJointData, pt_id,
                           FootJointData.mtp_joint_left_1,
                           FootJointData.mtp_joint_left_2,
                           FootJointData.mtp_joint_left_3,
                           FootJointData.mtp_joint_left_4,
                           FootJointData.mtp_joint_left_5,
                           FootJointData.mtp_joint_right_1,
                           FootJointData.mtp_joint_right_2,
                           FootJointData.mtp_joint_right_3,
                           FootJointData.mtp_joint_right_4,
                           FootJointData.mtp_joint_right_5)
        )

        # proximal_jointsの計算
        proximal_joints = get_latest_sum(LargeJointData, pt_id,
                                         LargeJointData.elbow_joint_left,
                                         LargeJointData.elbow_joint_right,
                                         LargeJointData.shoulder_joint_left,
                                         LargeJointData.shoulder_joint_right,
                                         LargeJointData.hip_joint_left,
                                         LargeJointData.hip_joint_right,
                                         LargeJointData.knee_joint_left,
                                         LargeJointData.knee_joint_right,
                                         LargeJointData.ankle_joint_left,
                                         LargeJointData.ankle_joint_right)
        
        other_proximal_joints = get_latest_sum(LargeJointData, pt_id, 
                                               LargeJointData.sternoclavicular_joint_left,
                                               LargeJointData.sternoclavicular_joint_right,
                                               LargeJointData.acromioclavicular_joint_left,
                                               LargeJointData.acromioclavicular_joint_right,
                                               LargeJointData.temporomandibular_joint_left, 
                                               LargeJointData.temporomandibular_joint_right)

        print(f"Total distal_joints: {distal_joints}")  # デバッグ用出力
        print(f"Total proximal_joints: {proximal_joints}")  # デバッグ用出力
        print(f"Total other_proximal_joints: {other_proximal_joints}")  # デバッグ用出力

        # joint_scoreの計算（変更なし）
        if distal_joints == 0:
            if proximal_joints <= 1:
                joint_score = 0
            else:
                joint_score = 1
        else:
            if proximal_joints + distal_joints + other_proximal_joints>= 11:
                joint_score = 5
            else:
                if distal_joints <= 3:
                    joint_score = 2
                else: 
                    if distal_joints <= 10:
                        joint_score = 3
                    else:
                        joint_score = 5

        # LabDataとSymptomデータを取得
        lab_data = LabData.query.filter_by(pt_id=pt_id, visit_number=visit_number).first()
        symptom = Symptom.query.filter_by(pt_id=pt_id, visit_number=visit_number).first()

        if not lab_data or not symptom:
            raise ValueError("Required lab data or symptom data not found")

        # inflammation_scoreを計算
        if lab_data.crp > 0.3:
            inflammation_score = 1
        elif (symptom.sex == "male" and lab_data.esr > 10) or (symptom.sex == "female" and lab_data.esr > 15):
            inflammation_score = 1
        else:
            inflammation_score = 0

        # immunology_scoreを計算
        if lab_data.rf >= 45 or lab_data.acpa >= 13.5:
            immunology_score = 2
        elif lab_data.rf >= 15 or lab_data.acpa >= 4.5:
            immunology_score = 1
        else:
            immunology_score = 0

        # duration_scoreを計算
        if symptom.six_weeks_duration=="yes":
            duration_score = 1
        else:
            duration_score = 0

        # total_scoreを計算
        total_score = joint_score + inflammation_score + immunology_score + duration_score

        # ScoreDataに結果を保存
        score_data = ScoreData(
            user_id=current_user.id,
            pt_id=pt_id,
            visit_number=visit_number,
            distal_joints=distal_joints,
            proximal_joints=proximal_joints,
            other_proximal_joints=other_proximal_joints,
            joint_score=joint_score,
            inflammation_score=inflammation_score,
            immunology_score=immunology_score,
            duration_score=duration_score,
            total_score=total_score
        )

        db.session.add(score_data)
        db.session.commit()

        return render_template('scoring.html', score_data=score_data, total_score=total_score, immunology_score=immunology_score, inflammation_score=inflammation_score, joint_score=joint_score, duration_score=duration_score)

    except Exception as e:
        db.session.rollback()  # ロールバックしてトランザクションをキャンセル
        current_app.logger.error(f"Error during scoring process: {str(e)}")
        return jsonify({"error": "An error occurred during the scoring process.", "details": str(e)}), 500

@data_blueprint.route('/finished', methods=['GET', 'POST'])
@login_required
def finished():
    return render_template('finished.html')
