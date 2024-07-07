from datetime import datetime
from .extensions import db
from .models import Symptom

class Labo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    crp = db.Column(db.Float, nullable=False)
    esr = db.Column(db.Integer, nullable=False)
    rf = db.Column(db.Float, nullable=False)
    acpa = db.Column(db.Float, nullable=False)
    immunology_score = db.Column(db.Integer, nullable=False)
    inflammation_score = db.Column(db.Integer, nullable=False)
    joint_score = db.Column(db.Integer, nullable=False)
    total_score = db.Column(db.Integer, nullable=False)

        # distal_joints と proximal_joints の計算と保存
def distal_joints(joint_entry):
    distal_joints = sum(
        [getattr(joint_entry, f"pip_joint_left_{i}", 0) for i in range(2, 6)] + \
        [getattr(joint_entry, f"pip_joint_right_{i}", 0) for i in range(2, 6)]+ \
        [getattr(joint_entry, f"mtp_joint_left_{i}", 0) for i in range(1, 6)]+ \
        [getattr(joint_entry, f"mtp_joint_right_{i}", 0) for i in range(1, 6)]+ \
        getattr(joint_entry, "thumb_ip_joint_left", 0) + \
        getattr(joint_entry, "thumb_ip_joint_right", 0)+ \
        getattr(joint_entry, "hand_wrist_joint_left", 0) + \
        getattr(joint_entry, "hand_wrist_joint_right", 0))
    return distal_joints

def proximal_joints(joint_entry):
    proximal_joints = sum(
        getattr(joint_entry, f"elbow_joint_left", 0), 
        getattr(joint_entry, f"shoulder_joint_left", 0),
        getattr(joint_entry, f"elbow_joint_right", 0),
        getattr(joint_entry, f"shoulder_joint_right", 0),
        getattr(joint_entry, f"hip_joint_left", 0),
        getattr(joint_entry, f"hip_joint_right", 0),
        getattr(joint_entry, f"knee_joint_left", 0),
        getattr(joint_entry, f"knee_joint_right", 0),
        getattr(joint_entry, f"ankle_joint_left", 0),
        getattr(joint_entry, f"ankle_joint_right", 0)
    )
    return proximal_joints    

def joint_score(proximal_joints, distal_joints):
    joint_score = 0  # 関節スコアの初期値を設定
    # "distal_joints"が0のときの条件
    if distal_joints == 0:
        if proximal_joints == 0:
            return 0
        else:
            return 1
        # distal_jointsが0より大きい数のときの条件
    else:
        # proximal_joints + distal_jointsの合計が11以上の場合
        if proximal_joints + distal_joints >= 11:
            return 5
        # proximal_joints + distal_jointsの合計が10未満の場合
        elif proximal_joints + distal_joints < 10:
        # distal_jointsが3以下の場合
            if distal_joints <= 3:
                return 2
        # distal_jointsが4以上の場合
            else:
                return 3

def immunology_score(rf, acpa):
    immunology_score = 0  # 免疫学的スコアの初期値を設定
    # 最初の条件群
    if rf >= 45:
        return 2
    elif acpa >= 13.5:
        return 2
    elif rf >= 15:
        return 1
    elif acpa >= 4.5:
        return 1
    else:
        return 0

def inflammation_score(crp, esr, sex):
    imflammation_score = 0  # 炎症スコアの初期値を設定
    # crpとesrの値によってスコアを返す
    if crp > 0.3:
        return 1
    elif sex == 0:
        if esr > 10:
            return 1
        else:
            return 0
    elif sex == 1:
        if esr > 15:
            return 1
        return 0
    
def duration_score(six_weeks_duration):
    six_weeks_duration = 0  # 持続期間スコアの初期値を設定
    # 持続期間によってスコアを返す
    if six_weeks_duration == 1:
        return 1
    else:
        return 0
    
def total_score(immunology_score, inflammation_score, joint_score):
    total_score = immunology_score + inflammation_score + joint_score + duration_score
    return total_score