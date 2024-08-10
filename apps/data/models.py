from datetime import datetime
from apps.data.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    #idを患者特定に使用するときは、email="####"にする。idをid=-1からidに変更する。
    def __init__(self, email, password):
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        return str(self.id)
    
    def __repr__(self):
        return '<User {}>'.format(self.email)

class Symptom(db.Model):
    __tablename__ = 'symptom'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sex = db.Column(db.String(10))
    birth_year = db.Column(db.Integer)
    birth_month = db.Column(db.Integer)
    birth_day = db.Column(db.Integer)
    onset_year = db.Column(db.Integer)
    onset_month = db.Column(db.Integer)
    onset_day = db.Column(db.Integer)
    morning_stiffness = db.Column(db.String(50))
    stiffness_duration = db.Column(db.Integer)
    pain_level = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    six_weeks_duration = db.Column(db.String(10))

    def __init__(self, user_id, sex, birth_year, birth_month, birth_day, onset_year, onset_month, onset_day,
                 morning_stiffness, stiffness_duration, pain_level, six_weeks_duration):
        self.user_id = user_id
        self.sex = sex
        self.birth_year = birth_year
        self.birth_month = birth_month
        self.birth_day = birth_day
        self.onset_year = onset_year
        self.onset_month = onset_month
        self.onset_day = onset_day
        self.morning_stiffness = morning_stiffness
        self.stiffness_duration = stiffness_duration
        self.pain_level = pain_level
        self.six_weeks_duration = six_weeks_duration

    def calculate_age(self, current_year, current_month, current_day):
        age = current_year - self.birth_year
        if (current_month, current_day) < (self.birth_month, self.birth_day):
            age -= 1
        return age    
    
    def calculate_duration(self, current_year, current_month, current_day):
        onset_date = datetime(self.onset_year, self.onset_month, self.onset_day)
        current_date = datetime(current_year, current_month, current_day)
        duration = (current_date - onset_date).days
        return duration

    def calculate_six_weeks_duration(self, current_year, current_month, current_day):
        onset_date = datetime(self.onset_year, self.onset_month, self.onset_day)
        current_date = datetime(current_year, current_month, current_day)
        duration = (current_date - onset_date).days
        six_weeks_duration = duration // 7
        return six_weeks_duration

class Criteria(db.Model):
    __tablename__ = 'criteria'
    
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
    duration_score = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, email, crp, esr, rf, acpa):
        self.user_id = user_id
        self.email = email
        self.crp = crp
        self.esr = esr
        self.rf = rf
        self.acpa = acpa
    
    def distal_joints(self, joint_entry):
        distal_joints = sum(
            [getattr(joint_entry, f"pip_joint_left_{i}", 0) for i in range(2, 6)] + \
            [getattr(joint_entry, f"pip_joint_right_{i}", 0) for i in range(2, 6)] + \
            [getattr(joint_entry, f"mtp_joint_left_{i}", 0) for i in range(1, 6)] + \
            [getattr(joint_entry, f"mtp_joint_right_{i}", 0) for i in range(1, 6)] + \
            [getattr(joint_entry, "thumb_ip_joint_left", 0), getattr(joint_entry, "thumb_ip_joint_right", 0)] + \
            [getattr(joint_entry, "wrist_joint_hand_left", 0), getattr(joint_entry, "wrist_joint_hand_right", 0)]
        )
        return distal_joints

    def proximal_joints(self, joint_entry):
        proximal_joints = sum(
            [getattr(joint_entry, f"{joint}", 0) for joint in [
                "elbow_joint_left", "shoulder_joint_left",
                "elbow_joint_right", "shoulder_joint_right",
                "hip_joint_left", "hip_joint_right",
                "knee_joint_left", "knee_joint_right",
                "ankle_joint_left", "ankle_joint_right"
            ]]
        )
        return proximal_joints    

    def calculate_joint_score(self, proximal_joints, distal_joints):
        if distal_joints == 0:
            return 1 if proximal_joints != 0 else 0
        elif proximal_joints + distal_joints >= 11:
            return 5
        elif distal_joints <= 3:
            return 2 if proximal_joints + distal_joints < 10 else 3
        return 0

    def calculate_immunology_score(self):
        if self.rf >= 45 or self.acpa >= 13.5:
            return 2
        elif self.rf >= 15 or self.acpa >= 4.5:
            return 1
        return 0

    def calculate_inflammation_score(self, sex):
        if self.crp > 0.3:
            return 1
        elif (sex == 0 and self.esr > 10) or (sex == 1 and self.esr > 15):
            return 1
        return 0
        
    def calculate_duration_score(self, six_weeks_duration):
        return 1 if six_weeks_duration == 1 else 0
        
    def calculate_total_score(self, inflammation_score, joint_score, six_weeks_duration):
        return self.calculate_immunology_score() + inflammation_score + joint_score + self.calculate_duration_score(six_weeks_duration)

class HandData(db.Model):
    __tablename__ = 'hand_data'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    right_hand_path = db.Column(db.String(255), nullable=False)
    left_hand_path = db.Column(db.String(255), nullable=False)

    def __init__(self, user_id, datetime, right_hand_path, left_hand_path):
        self.user_id = user_id
        self.datetime = datetime
        self.right_hand_path = right_hand_path
        self.left_hand_path = left_hand_path

class JointData(db.Model):
    __tablename__ = 'joint_data'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    dip_joint_left_2 = db.Column(db.Integer)
    dip_joint_left_3 = db.Column(db.Integer)
    dip_joint_left_4 = db.Column(db.Integer)
    dip_joint_left_5 = db.Column(db.Integer)
    dip_joint_right_2 = db.Column(db.Integer)
    dip_joint_right_3 = db.Column(db.Integer)
    dip_joint_right_4 = db.Column(db.Integer)
    dip_joint_right_5 = db.Column(db.Integer)
    thumb_ip_joint_left = db.Column(db.Integer)
    thumb_ip_joint_right = db.Column(db.Integer)
    pip_joint_left_2 = db.Column(db.Integer)
    pip_joint_left_3 = db.Column(db.Integer)
    pip_joint_left_4 = db.Column(db.Integer)
    pip_joint_left_5 = db.Column(db.Integer)
    pip_joint_right_2 = db.Column(db.Integer)
    pip_joint_right_3 = db.Column(db.Integer)
    pip_joint_right_4 = db.Column(db.Integer)
    pip_joint_right_5 = db.Column(db.Integer)
    mp_joint_left_1 = db.Column(db.Integer)
    mp_joint_left_2 = db.Column(db.Integer)
    mp_joint_left_3 = db.Column(db.Integer)
    mp_joint_left_4 = db.Column(db.Integer)
    mp_joint_left_5 = db.Column(db.Integer)
    mp_joint_right_1 = db.Column(db.Integer)
    mp_joint_right_2 = db.Column(db.Integer)
    mp_joint_right_3 = db.Column(db.Integer)
    mp_joint_right_4 = db.Column(db.Integer)
    mp_joint_right_5 = db.Column(db.Integer)
    wrist_joint_hand_left = db.Column(db.Integer)
    wrist_joint_hand_right = db.Column(db.Integer)
    elbow_joint_left = db.Column(db.Integer)
    elbow_joint_right = db.Column(db.Integer)
    shoulder_joint_left = db.Column(db.Integer)
    shoulder_joint_right = db.Column(db.Integer)
    hip_joint_left = db.Column(db.Integer)
    hip_joint_right = db.Column(db.Integer)
    knee_joint_left = db.Column(db.Integer)
    knee_joint_right = db.Column(db.Integer)
    ankle_joint_left = db.Column(db.Integer)
    ankle_joint_right = db.Column(db.Integer)
    mtp_joint_left_1 = db.Column(db.Integer)
    mtp_joint_left_2 = db.Column(db.Integer)
    mtp_joint_left_3 = db.Column(db.Integer)
    mtp_joint_left_4 = db.Column(db.Integer)
    mtp_joint_left_5 = db.Column(db.Integer)
    mtp_joint_right_1 = db.Column(db.Integer)
    mtp_joint_right_2 = db.Column(db.Integer)
    mtp_joint_right_3 = db.Column(db.Integer)
    mtp_joint_right_4 = db.Column(db.Integer)
    mtp_joint_right_5 = db.Column(db.Integer)
    distal_joints = db.Column(db.Integer)
    proximal_joints = db.Column(db.Integer)

    def __init__(self, user_id, dip_joint_left_2, dip_joint_left_3, dip_joint_left_4, dip_joint_left_5, dip_joint_right_2, dip_joint_right_3, dip_joint_right_4, dip_joint_right_5, thumb_ip_joint_left, thumb_ip_joint_right, pip_joint_left_2, pip_joint_left_3, pip_joint_left_4, pip_joint_left_5, pip_joint_right_2, pip_joint_right_3, pip_joint_right_4, pip_joint_right_5, mp_joint_left_1, mp_joint_left_2, mp_joint_left_3, mp_joint_left_4, mp_joint_left_5, mp_joint_right_1, mp_joint_right_2, mp_joint_right_3, mp_joint_right_4, mp_joint_right_5, wrist_joint_hand_left, wrist_joint_hand_right, elbow_joint_left, elbow_joint_right, shoulder_joint_left, shoulder_joint_right, hip_joint_left, hip_joint_right, knee_joint_left, knee_joint_right, ankle_joint_left, ankle_joint_right, mtp_joint_left_1, mtp_joint_left_2, mtp_joint_left_3, mtp_joint_left_4, mtp_joint_left_5, mtp_joint_right_1, mtp_joint_right_2, mtp_joint_right_3, mtp_joint_right_4, mtp_joint_right_5, distal_joints, proximal_joints):
        self.user_id = user_id
        self.dip_joint_left_2 = dip_joint_left_2
        self.dip_joint_left_3 = dip_joint_left_3
        self.dip_joint_left_4 = dip_joint_left_4
        self.dip_joint_left_5 = dip_joint_left_5
        self.dip_joint_right_2 = dip_joint_right_2
        self.dip_joint_right_3 = dip_joint_right_3
        self.dip_joint_right_4 = dip_joint_right_4
        self.dip_joint_right_5 = dip_joint_right_5
        self.thumb_ip_joint_left = thumb_ip_joint_left
        self.thumb_ip_joint_right = thumb_ip_joint_right
        self.pip_joint_left_2 = pip_joint_left_2
        self.pip_joint_left_3 = pip_joint_left_3
        self.pip_joint_left_4 = pip_joint_left_4
        self.pip_joint_left_5 = pip_joint_left_5
        self.pip_joint_right_2 = pip_joint_right_2
        self.pip_joint_right_3 = pip_joint_right_3
        self.pip_joint_right_4 = pip_joint_right_4
        self.pip_joint_right_5 = pip_joint_right_5
        self.mp_joint_left_1 = mp_joint_left_1
        self.mp_joint_left_2 = mp_joint_left_2
        self.mp_joint_left_3 = mp_joint_left_3
        self.mp_joint_left_4 = mp_joint_left_4
        self.mp_joint_left_5 = mp_joint_left_5
        self.mp_joint_right_1 = mp_joint_right_1
        self.mp_joint_right_2 = mp_joint_right_2
        self.mp_joint_right_3 = mp_joint_right_3
        self.mp_joint_right_4 = mp_joint_right_4
        self.mp_joint_right_5 = mp_joint_right_5
        self.wrist_joint_hand_left = wrist_joint_hand_left
        self.wrist_joint_hand_right = wrist_joint_hand_right
        self.elbow_joint_left = elbow_joint_left
        self.elbow_joint_right = elbow_joint_right
        self.shoulder_joint_left = shoulder_joint_left
        self.shoulder_joint_right = shoulder_joint_right
        self.hip_joint_left = hip_joint_left
        self.hip_joint_right = hip_joint_right
        self.knee_joint_left = knee_joint_left
        self.knee_joint_right = knee_joint_right
        self.ankle_joint_left = ankle_joint_left
        self.ankle_joint_right = ankle_joint_right
        self.mtp_joint_left_1 = mtp_joint_left_1
        self.mtp_joint_left_2 = mtp_joint_left_2
        self.mtp_joint_left_3 = mtp_joint_left_3
        self.mtp_joint_left_4 = mtp_joint_left_4
        self.mtp_joint_left_5 = mtp_joint_left_5
        self.mtp_joint_right_1 = mtp_joint_right_1
        self.mtp_joint_right_2 = mtp_joint_right_2
        self.mtp_joint_right_3 = mtp_joint_right_3
        self.mtp_joint_right_4 = mtp_joint_right_4
        self.mtp_joint_right_5 = mtp_joint_right_5
        self.distal_joints = distal_joints
        self.proximal_joints = proximal_joints
