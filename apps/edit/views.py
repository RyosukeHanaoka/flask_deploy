from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from apps.data.models import Symptom
from apps.data.extensions import db

# Blueprintの定義
edit_blueprint = Blueprint('edit_blueprint', __name__, template_folder='templates', static_folder='static')

# サインイン中の医師が入力した患者のobject_idを取得する補助関数
def get_user_patient_object_ids():
    object_ids = db.session.query(Symptom.object_id).filter_by(user_id=current_user.id).distinct().all()
    return [obj_id[0] for obj_id in object_ids]  # クエリ結果のタプルからobject_idを抽出

# ダッシュボード表示（患者のobject_id一覧表示）
@edit_blueprint.route('/dashboard', methods=['GET', 'POST'])
@login_required
def select_patient():
    object_ids = get_user_patient_object_ids()
    
    """if request.method == 'POST':
        selected_object_id = request.form.get('object_id')
        # ここで選択されたobject_idを使って編集画面などにリダイレクトする
        return redirect(url_for('edit_blueprint.edit_patient', object_id=selected_object_id))"""
    
    return render_template('dashboard.html', object_ids=object_ids)

# 患者データの編集ページ
@edit_blueprint.route('/edit_patient/<object_id>', methods=['GET', 'POST'])
@login_required
def edit_patient(object_id):
    # ここでobject_idを使って編集ページを表示する
    # 患者データを取得し、編集フォームにプリロードします。
    symptom = Symptom.query.filter_by(object_id=object_id, user_id=current_user.id).first()
    if request.method == 'POST':
        # フォームのデータを使って患者情報を更新
        pass
    
    return render_template('edit_patient.html', symptom=symptom)
