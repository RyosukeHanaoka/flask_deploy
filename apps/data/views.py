from flask import Blueprint, abort, render_template, request, redirect, url_for, flash, current_app, jsonify, session
from flask_login import login_required, current_user
from .extensions import db
import datetime
import os
from .models import HandPicData, RightHandData, LeftHandData, LargeJointData, FootJointData
from .models import Symptom, Criteria
from .vit import Vit
vit=Vit(model_checkpoint='/Users/hanaokaryousuke/flask/apps/data/model.pth')
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

@data_blueprint.route('/symptom', methods=['GET', 'POST'])
@login_required
def symptom():
    if request.method == 'POST':
        user = Symptom(
            user_id=current_user.id,
            sex=request.form.get('sex', ''),
            object_id=request.form.get('object_id', ''),
            birth_year=int(request.form.get('birth_year', 0)),
            birth_month=int(request.form.get('birth_month', 0)),
            birth_day=int(request.form.get('birth_day', 0)),
            disease_duration=int(request.form.get('disease_duration', 0)),
            morning_stiffness=request.form.get('morning_stiffness', ''),
            six_weeks_duration=request.form.get('six_weeks_duration', ''),
            stiffness_duration=int(request.form.get('stiffness_duration', 0)),
            pain_level=int(request.form.get('pain_level', 0))       
        )
        
        db.session.add(user)
        db.session.commit()
        session['object_id'] = request.form.get('object_id', '')
        return redirect(url_for('data_blueprint.righthand'))

    years = range(1920, datetime.date.today().year + 1)
    months = range(1, 13)
    days = range(1, 32)
    stiffness_durations = [0, 5, 10, 15, 20, 30, 40, 50, 60, 120]

    return render_template('symptom.html' , years=years, months=months, days=days, stiffness_durations=stiffness_durations)

@data_blueprint.route('/righthand', methods=['GET', 'POST'])
@login_required
def righthand():
    if request.method == 'POST':
        print(request.form)
        data=request.form
        object_id = session.get('object_id')
            # セッションから検出結果を取得
        joint_entry = RightHandData(
            user_id=current_user.id,
            object_id = object_id,
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
#@login_required
def lefthand():
    if request.method == 'POST':
        data=request.form
        object_id = session.get('object_id')
        joint_entry = LeftHandData(
            user_id=current_user.id,
            object_id = object_id,
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
        object_id = session.get('object_id')
        joint_entry = LargeJointData(
            user_id=current_user.id,
            object_id = object_id,
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
        object_id = session.get('object_id')
        joint_entry = FootJointData(
            user_id=current_user.id,
            object_id = object_id,
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
        # フォームからデータを取得
        crp = float(request.form['crp'])
        esr = int(request.form['esr'])
        rf = float(request.form['rf'])
        acpa = float(request.form['acpa'])
        object_id = session.get('object_id')
    
        # データベースに保存
        labo_data = Criteria(
            user_id=current_user.id,
            object_id = object_id,
            email=current_user.email,
            crp=crp,
            esr=esr,
            rf=rf,
            acpa=acpa
        )
        db.session.add(labo_data)
        db.session.commit()

        return redirect(url_for('data_blueprint.handpicture'))

    return render_template('labo_exam.html') 

@data_blueprint.route('/handpicture', methods=['GET', 'POST'])
@login_required
def handpicture():
    if request.method == 'POST':
        object_id = session.get('object_id')
        #フォームから送信されたファイルのうち、right_handという名前のファイルを取得
        right_hand = request.files.get('right_hand')
        #フォームから送信されたファイルのうち、left_handという名前のファイルを取得
        left_hand = request.files.get('left_hand')
        #右手または左手のファイルが送信されていない場合にTrueとなる条件式
        if not right_hand or not left_hand:
            #HTTP 400エラーを返し、エラーメッセージを提供
            abort(400, description="Missing 'right_hand' or 'left_hand' file in request")
        #現在の日時を取得
        now = datetime.datetime.now()
        
        #日時を文字列に変換
        dt_string = now.strftime("%Y%m%d_%H%M%S")
        #ユーザーのメールアドレスと日時を組み合わせてファイル名を生成
        right_filename = f"{current_user.email}_{dt_string}_right.jpg"
        left_filename = f"{current_user.email}_{dt_string}_left.jpg"

        # 画像を保存するディレクトリ
        right_dir = "data/pictures/image_righthand"
        left_dir = "data/pictures/image_lefthand"

        # ディレクトリが存在しない場合は作成
        os.makedirs(right_dir, exist_ok=True)
        os.makedirs(left_dir, exist_ok=True)

        # 保存するファイルのパス
        right_path = os.path.join(right_dir, right_filename)
        left_path = os.path.join(left_dir, left_filename)

        # ファイルを保存
        right_hand.save(right_path)
        left_hand.save(left_path)

                #モデル（ここではvit）を使ってリウマチ関節炎の検出を行い、その結果を取得
        result = vit.detect_rheumatoid_arthritis(right_path, left_path)
        right_hand_result = vit.detect_rheumatoid_arthritis(right_path, left_path)
        left_hand_result = vit.detect_rheumatoid_arthritis(right_path, left_path)

        #右手と左手の画像のパス、現在のユーザーID、日時を含む新しいHandDataオブジェクトを作成
        hand_data = HandPicData(
            user_id=current_user.id,
            object_id = object_id,
            datetime=now,
            right_hand_path=right_path,
            left_hand_path=left_path,
            right_hand_result=right_hand_result,  # 右手の結果
            left_hand_result=left_hand_result,  # 左手の結果
            result=result  # 全体の結果
        )
        #データベースセッションに新しいHandDataオブジェクトを追加
        db.session.add(hand_data)
        #データベースに変更をコミット（保存）
        db.session.commit()

        #検出結果をセッションに保存
        session['result'] = result
        #/ptresultエンドポイントにリダイレクト
        return redirect(url_for('data_blueprint.ptresult'))
    #GETリクエストが送信された場合、handpicture.htmlテンプレートをレンダリングして返す
    return render_template('handpicture.html')


@data_blueprint.route('/ptresult', methods=['GET', 'POST'])
@login_required
def ptresult():
    # セッションから検出結果を取得
    result = session.get('result')
    #セッションに結果が保存されていない場合、HTTP 400エラーを返す
    if result is None:
        abort(400, description="結果が見つかりません")
    
    # 結果を表示する
    return render_template('ptresult.html', result=result)