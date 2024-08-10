from flask import Blueprint, abort, render_template, request, redirect, url_for, flash, current_app, jsonify, session
from flask_login import login_required, current_user
from .models import JointData
from .extensions import db
import datetime
import os
from .models import HandData
from .models import Criteria
from .models import Symptom, Criteria
from PIL import Image
from .detr import Detr
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
            birth_year=int(request.form.get('birth_year', 0)),
            birth_month=int(request.form.get('birth_month', 0)),
            birth_day=int(request.form.get('birth_day', 0)),
            onset_year=int(request.form.get('onset_year', 0)),
            onset_month=int(request.form.get('onset_month', 0)),
            onset_day=int(request.form.get('onset_day', 0)),
            morning_stiffness=request.form.get('morning_stiffness', ''),
            six_weeks_duration=request.form.get('six_weeks_duration', ''),
            stiffness_duration=int(request.form.get('stiffness_duration', 0)),
            pain_level=int(request.form.get('pain_level', 0))       
        )
        
        db.session.add(user)
        db.session.commit()
        flash('登録が完了しました！', 'success')
        return redirect(url_for('data.righthand'))

    years = range(1920, datetime.date.today().year + 1)
    months = range(1, 13)
    days = range(1, 32)
    stiffness_durations = [0, 5, 10, 15, 20, 30, 40, 50, 60, 120]

    return render_template('symptom.html' , years=years, months=months, days=days, stiffness_durations=stiffness_durations)

@data_blueprint.route('/righthand', methods=['GET', 'POST'])
@login_required
def righthand():
    if request.method == 'POST':
        data=request.form
        joint_entry = JointData(
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
        joint_entry = JointData(
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
        joint_entry = JointData(
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
        joint_entry = JointData(
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

        return redirect(url_for('data_blueprint.handpicture'))
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
    
        # データベースに保存
        labo_data = Criteria(
            user_id=current_user.id,
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
        #フォームから送信されたファイルのうち、right_handという名前のファイルを取得
        right_hand = request.files.get('right_hand')
        #フォームから送信されたファイルのうち、left_handという名前のファイルを取得
        left_hand = request.files.get('left_hand')
        #右手または左手のファイルが送信されていない場合にTrueとなる条件式
        if not right_hand or not left_hand:
            #HTTP 400エラーを返し、エラーメッセージを提供
            abort(400, description="Missing 'right_hand' or 'left_hand' file in request")
        #現在の日時を取得
        now = datetime.now()
        #日時を文字列に変換
        dt_string = now.strftime("%Y%m%d_%H%M%S")
        #ユーザーのメールアドレスと日時を組み合わせてファイル名を生成
        right_filename = f"{current_user.email}_{dt_string}_right.jpg"
        #画像を保存するディレクトリへのパスを生成
        right_path = os.path.join("apps/data/image_righthand", right_filename)
        #右手の画像を指定したパスに保存
        right_hand.save(right_path)
        #ユーザーのメールアドレスと日時を組み合わせてファイル名を生成
        left_filename = f"{current_user.email}_{dt_string}_left.jpg"
        #画像を保存するディレクトリへのパスを生成
        left_path = os.path.join("apps/data/image_lefthand", left_filename)
        #左手の画像を指定したパスに保存
        left_hand.save(left_path)

        #右手と左手の画像のパス、現在のユーザーID、日時を含む新しいHandDataオブジェクトを作成
        hand_data = HandData(
            user_id=current_user.id,
            datetime=now,
            right_hand_path=right_path,
            left_hand_path=left_path
        )
        #データベースセッションに新しいHandDataオブジェクトを追加
        db.session.add(hand_data)
        #データベースに変更をコミット（保存）
        db.session.commit()
        #モデル（ここではvit）を使ってリウマチ関節炎の検出を行い、その結果を取得
        result = vit.detect_rheumatoid_arthritis(right_path, left_path)
        #検出結果をセッションに保存
        session['result'] = result
        #/ptresultエンドポイントにリダイレクト
        return redirect(url_for('data_blueprint.ptresult'))
    #GETリクエストが送信された場合、handpicture.htmlテンプレートをレンダリングして返す
    return render_template('handpicture.html')


@data_blueprint.route('/ptresult', methods=['GET', 'POST'])
@login_required
def result():
    # セッションから検出結果を取得
    result = session.get('result')
    #セッションに結果が保存されていない場合、HTTP 400エラーを返す
    if result is None:
        abort(400, description="結果が見つかりません")
    
    # 結果を表示する
    return render_template('ptresult.html', result=result)


"""
@data_blueprint.route('/x_ray', methods=['GET', 'POST'])
#@login_required
def x_ray():
    if request.method == 'POST':
        upload_type = request.form['upload_type']

        if upload_type == 'camera':
            # ディスプレイ画面上の画像をスマートフォンで撮影する場合
            right_hand = request.files['right_hand']
            left_hand = request.files['left_hand']

            # 画像を保存するフォルダのパスを指定
            save_folder = 'apps/data/x_ray'

            # 右手のX線画像を保存
            right_filename = f"{current_user.email}_right_xray.jpg"
            right_path = os.path.join(save_folder, right_filename)
            right_hand.save(right_path)

            # 左手のX線画像を保存
            left_filename = f"{current_user.email}_left_xray.jpg"
            left_path = os.path.join(save_folder, left_filename)
            left_hand.save(left_path)

        elif upload_type == 'dicom':
            # DICOMファイルをアップロードする場合
            dicom_type = request.form['dicom_type']

            if dicom_type == 'combined':
                # 両手が同時に撮影された画像を取り込む
                dicom_file = request.files['dicom_file']

                # 画像を保存するフォルダのパスを指定
                save_folder = 'apps/data/x_ray_dcm'

                # DICOMファイルを保存
                filename = f"{current_user.email}_combined.dcm"
                path = os.path.join(save_folder, filename)
                dicom_file.save(path)

            elif dicom_type == 'separate':
                # 左右の手のX線を別々に取り込む
                right_dicom = request.files['right_dicom']
                left_dicom = request.files['left_dicom']

                # 画像を保存するフォルダのパスを指定
                save_folder = 'apps/data/x_ray_dcm'

                # 右手のDICOMファイルを保存
                right_filename = f"{current_user.email}_right.dcm"
                right_path = os.path.join(save_folder, right_filename)
                right_dicom.save(right_path)

                # 左手のDICOMファイルを保存
                left_filename = f"{current_user.email}_left.dcm"
                left_path = os.path.join(save_folder, left_filename)
                left_dicom.save(left_path)

        return redirect(url_for('data_blueprint.drresult'))

    return render_template('x_ray.html')"""


