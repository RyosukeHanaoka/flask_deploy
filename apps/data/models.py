from datetime import datetime
from apps.data.extensions import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = "user"    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
    
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

class BaseVisitData(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    pt_id = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    visit_number = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())

class Symptom(db.Model):
    __tablename__ = 'symptom'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pt_id = db.Column(db.String(50), nullable=False)
    visit_number = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String(10))
    birth_date = db.Column(db.Date)
    disease_duration = db.Column(db.Integer)
    morning_stiffness = db.Column(db.String(50))
    stiffness_duration = db.Column(db.Integer)
    pain_level = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
    six_weeks_duration = db.Column(db.String(3))

    def __init__(self, user_id, pt_id, visit_number, sex, birth_date, disease_duration,
                morning_stiffness, stiffness_duration, pain_level, six_weeks_duration):
        super().__init__()
        self.user_id = user_id
        self.pt_id = pt_id
        self.visit_number = visit_number
        self.sex = sex
        self.birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
        self.disease_duration = disease_duration
        self.morning_stiffness = morning_stiffness
        self.stiffness_duration = stiffness_duration
        self.pain_level = pain_level
        self.six_weeks_duration = six_weeks_duration

    def calculate_age(self, current_date=None):
        if current_date is None:
            current_date = datetime.today().date()
        
        age = current_date.year - self.birth_date.year
        
        if (current_date.month, current_date.day) < (self.birth_date.month, self.birth_date.day):
            age -= 1
        
        return age
      
class HandPicData(db.Model):
    __tablename__ = 'hand_data'    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pt_id = db.Column(db.String(50), nullable=False)
    visit_number = db.Column(db.Integer, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    right_hand_path = db.Column(db.String(255), nullable=False)
    left_hand_path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
    right_hand_result= db.Column(db.Float)
    left_hand_result= db.Column(db.Float)
    result= db.Column(db.Float)

    def __init__(self, user_id, pt_id, visit_number, datetime, right_hand_path, left_hand_path, right_hand_result, left_hand_result, result):
        self.user_id=user_id
        self.pt_id = pt_id
        self.visit_number = visit_number
        self.datetime = datetime
        self.right_hand_path = right_hand_path
        self.left_hand_path = left_hand_path
        self.right_hand_result = right_hand_result
        self.left_hand_result = left_hand_result
        self.result = result
class RightHandData(db.Model):
    __tablename__ = 'righthand_data'   
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pt_id = db.Column(db.String(50), nullable=False)
    visit_number = db.Column(db.Integer, nullable=False)
    dip_joint_right_2 = db.Column(db.Integer)
    dip_joint_right_3 = db.Column(db.Integer)
    dip_joint_right_4 = db.Column(db.Integer)
    dip_joint_right_5 = db.Column(db.Integer)
    thumb_ip_joint_right = db.Column(db.Integer)
    pip_joint_right_2 = db.Column(db.Integer)
    pip_joint_right_3 = db.Column(db.Integer)
    pip_joint_right_4 = db.Column(db.Integer)
    pip_joint_right_5 = db.Column(db.Integer)
    mp_joint_right_1 = db.Column(db.Integer)
    mp_joint_right_2 = db.Column(db.Integer)
    mp_joint_right_3 = db.Column(db.Integer)
    mp_joint_right_4 = db.Column(db.Integer)
    mp_joint_right_5 = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    def __init__(self, user_id, pt_id, visit_number, dip_joint_right_2, dip_joint_right_3, dip_joint_right_4, dip_joint_right_5, thumb_ip_joint_right, pip_joint_right_2, pip_joint_right_3, pip_joint_right_4, pip_joint_right_5, mp_joint_right_1, mp_joint_right_2, mp_joint_right_3, mp_joint_right_4, mp_joint_right_5):
        self.user_id=user_id
        self.pt_id = pt_id
        self.visit_number = visit_number
        self.dip_joint_right_2 = dip_joint_right_2
        self.dip_joint_right_3 = dip_joint_right_3
        self.dip_joint_right_4 = dip_joint_right_4
        self.dip_joint_right_5 = dip_joint_right_5
        self.thumb_ip_joint_right = thumb_ip_joint_right
        self.pip_joint_right_2 = pip_joint_right_2
        self.pip_joint_right_3 = pip_joint_right_3
        self.pip_joint_right_4 = pip_joint_right_4
        self.pip_joint_right_5 = pip_joint_right_5
        self.mp_joint_right_1 = mp_joint_right_1
        self.mp_joint_right_2 = mp_joint_right_2
        self.mp_joint_right_3 = mp_joint_right_3
        self.mp_joint_right_4 = mp_joint_right_4
        self.mp_joint_right_5 = mp_joint_right_5
class LeftHandData(db.Model):
    __tablename__ = 'lefthand_data'    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pt_id = db.Column(db.String(50), nullable=False)
    visit_number = db.Column(db.Integer, nullable=False)
    dip_joint_left_2 = db.Column(db.Integer)
    dip_joint_left_3 = db.Column(db.Integer)
    dip_joint_left_4 = db.Column(db.Integer)
    dip_joint_left_5 = db.Column(db.Integer)
    thumb_ip_joint_left = db.Column(db.Integer)
    pip_joint_left_2 = db.Column(db.Integer)
    pip_joint_left_3 = db.Column(db.Integer)
    pip_joint_left_4 = db.Column(db.Integer)
    pip_joint_left_5 = db.Column(db.Integer)
    mp_joint_left_1 = db.Column(db.Integer)
    mp_joint_left_2 = db.Column(db.Integer)
    mp_joint_left_3 = db.Column(db.Integer)
    mp_joint_left_4 = db.Column(db.Integer)
    mp_joint_left_5 = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    def __init__(self, user_id, pt_id, visit_number, dip_joint_left_2, dip_joint_left_3, dip_joint_left_4, dip_joint_left_5, thumb_ip_joint_left, pip_joint_left_2, pip_joint_left_3, pip_joint_left_4, pip_joint_left_5, mp_joint_left_1, mp_joint_left_2, mp_joint_left_3, mp_joint_left_4, mp_joint_left_5):
        self.user_id=user_id
        self.pt_id = pt_id
        self.visit_number = visit_number
        self.dip_joint_left_2 = dip_joint_left_2
        self.dip_joint_left_3 = dip_joint_left_3
        self.dip_joint_left_4 = dip_joint_left_4
        self.dip_joint_left_5 = dip_joint_left_5
        self.thumb_ip_joint_left = thumb_ip_joint_left
        self.pip_joint_left_2 = pip_joint_left_2
        self.pip_joint_left_3 = pip_joint_left_3
        self.pip_joint_left_4 = pip_joint_left_4
        self.pip_joint_left_5 = pip_joint_left_5
        self.mp_joint_left_1 = mp_joint_left_1
        self.mp_joint_left_2 = mp_joint_left_2
        self.mp_joint_left_3 = mp_joint_left_3
        self.mp_joint_left_4 = mp_joint_left_4
        self.mp_joint_left_5 = mp_joint_left_5
class LargeJointData(db.Model):
    __tablename__ = 'largejoint_data'    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pt_id = db.Column(db.String(50), nullable=False)
    visit_number = db.Column(db.Integer, nullable=False)
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
    sternoclavicular_joint_right = db.Column(db.Integer)
    sternoclavicular_joint_left = db.Column(db.Integer)
    acromioclavicular_joint_right = db.Column(db.Integer)
    acromioclavicular_joint_left = db.Column(db.Integer)
    temporomandibular_joint_right = db.Column(db.Integer)
    temporomandibular_joint_left = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    def __init__(self, user_id, pt_id, visit_number, wrist_joint_hand_left, wrist_joint_hand_right, elbow_joint_left, elbow_joint_right, shoulder_joint_left, shoulder_joint_right, hip_joint_left, hip_joint_right, knee_joint_left, knee_joint_right, ankle_joint_left, ankle_joint_right, sternoclavicular_joint_right, sternoclavicular_joint_left, acromioclavicular_joint_right, acromioclavicular_joint_left, temporomandibular_joint_right, temporomandibular_joint_left):  
        self.user_id=user_id
        self.pt_id = pt_id
        self.visit_number = visit_number
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
        self.sternoclavicular_joint_right = sternoclavicular_joint_right
        self.sternoclavicular_joint_left = sternoclavicular_joint_left
        self.acromioclavicular_joint_right = acromioclavicular_joint_right
        self.acromioclavicular_joint_left = acromioclavicular_joint_left
        self.temporomandibular_joint_right = temporomandibular_joint_right
        self.temporomandibular_joint_left = temporomandibular_joint_left
class FootJointData(db.Model):
    __tablename__ = 'footjoint_data'   
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pt_id = db.Column(db.String(50), nullable=False)
    visit_number = db.Column(db.Integer, nullable=False)
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
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    def __init__(self, user_id, pt_id, visit_number, mtp_joint_left_1, mtp_joint_left_2, mtp_joint_left_3, mtp_joint_left_4, mtp_joint_left_5, mtp_joint_right_1, mtp_joint_right_2, mtp_joint_right_3, mtp_joint_right_4, mtp_joint_right_5, distal_joints, proximal_joints):
        self.user_id=user_id
        self.pt_id = pt_id
        self.visit_number = visit_number
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

class LabData(db.Model):
    __tablename__ = 'lab_data'    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pt_id = db.Column(db.String(50), nullable=False)
    visit_number = db.Column(db.Integer, nullable=False)
    crp = db.Column(db.Float)
    esr = db.Column(db.Integer)
    rf = db.Column(db.Float)
    acpa = db.Column(db.Float)

    def __init__(self, user_id, pt_id, visit_number, crp, esr, rf, acpa):
        self.user_id=user_id
        self.pt_id = pt_id
        self.visit_number = visit_number
        self.crp = crp
        self.esr = esr
        self.rf = rf
        self.acpa = acpa
class ScoreData(db.Model):
    __tablename__ = 'score_data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pt_id = db.Column(db.String(50), nullable=False)
    visit_number = db.Column(db.Integer, nullable=False)
    distal_joints = db.Column(db.Integer)
    proximal_joints = db.Column(db.Integer)
    other_proximal_joints = db.Column(db.Integer)
    immunology_score = db.Column(db.Integer, nullable=False)
    inflammation_score = db.Column(db.Integer, nullable=False)
    joint_score = db.Column(db.Integer, nullable=False)
    total_score = db.Column(db.Integer, nullable=False)
    duration_score = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    def __init__(self, user_id, pt_id, visit_number, distal_joints, proximal_joints, other_proximal_joints, immunology_score, 
                 inflammation_score, joint_score, duration_score, total_score):
        self.user_id = user_id
        self.pt_id = pt_id
        self.visit_number = visit_number
        self.distal_joints = distal_joints
        self.proximal_joints = proximal_joints
        self.other_proximal_joints = other_proximal_joints
        self.immunology_score = immunology_score
        self.inflammation_score = inflammation_score
        self.joint_score = joint_score
        self.duration_score = duration_score
        self.total_score = total_score

    def calculate_total_score(self):
        return self.joint_score + self.inflammation_score + self.immunology_score + self.duration_score