from datetime import datetime
from .extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    def __init__(self):
        #テーブル名を指定
        __tablename__ = "user"
        #ユーザーのID (主キー)
        self.id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        #ユーザーのメールアドレス (一意制約、非Null制約)
        self.email = db.Column(db.String(120), unique=True, nullable=False)
        #ハッシュ化されたパスワード
        self.password_hash = db.Column(db.String(128))
        #ユーザーが作成された日時
        self.created_at = db.Column(db.DateTime, default=datetime.now)
        #ユーザーが最後に更新された日時
        self.updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
        #与えられたパスワードをハッシュ化してpassword_hash属性に設定
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        #与えられたパスワードが、保存されているハッシュ値と一致するかチェック
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        #ユーザーIDを文字列として返す (Flask-Loginで必要)
    def get_id(self):
        return str(self.id)
        #ユーザーを表す文字列表現を返す
    def __repr__(self):
        return '<User {}>'.format(self.email)

class Symptom(db.Model):
    def __init__(self):
        self.id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        self.user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        self.sex = db.Column(db.String(10))
        self.birth_year = db.Column(db.Integer)
        self.birth_month = db.Column(db.Integer)
        self.birth_day = db.Column(db.Integer)
        self.onset_year = db.Column(db.Integer)
        self.onset_month = db.Column(db.Integer)
        self.onset_day = db.Column(db.Integer)
        self.morning_stiffness = db.Column(db.String(50))
        self.stiffness_duration = db.Column(db.Integer)
        self.pain_level = db.Column(db.Integer)
        self.created_at = db.Column(db.DateTime, default=datetime.now)
        self.updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
        self.six_weeks_duration = db.Column(db.Integer)

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

from datetime import datetime
from .extensions import db

class Criteria(db.Model):
    def __init__(self):
        self.id = db.Column(db.Integer, primary_key=True)
        self.user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        self.email = db.Column(db.String(120), nullable=False)
        self.crp = db.Column(db.Float, nullable=False)
        self.esr = db.Column(db.Integer, nullable=False)
        self.rf = db.Column(db.Float, nullable=False)
        self.acpa = db.Column(db.Float, nullable=False)
        self.immunology_score = db.Column(db.Integer, nullable=False)
        self.inflammation_score = db.Column(db.Integer, nullable=False)
        self.joint_score = db.Column(db.Integer, nullable=False)
        self.total_score = db.Column(db.Integer, nullable=False)
        self.duration_score = db.Column(db.Integer, nullable=False)

        # distal_joints と proximal_joints の計算と保存
    def distal_joints(self, joint_entry):
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

    def proximal_joints(self, joint_entry):
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

    def joint_score(self, proximal_joints, distal_joints):
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

    def immunology_score(self, rf, acpa):
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

    def inflammation_score(self, crp, esr, sex):
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
        
    def duration_score(self, six_weeks_duration):
        six_weeks_duration = 0  # 持続期間スコアの初期値を設定
        # 持続期間によってスコアを返す
        if six_weeks_duration == 1:
            return 1
        else:
            return 0
        
    def total_score(self, inflammation_score, joint_score):
        def duration_score(six_weeks_duration):
            six_weeks_duration = 0  # 持続期間スコアの初期値を設定
            # 持続期間によってスコアを返す
            if six_weeks_duration == 1:
                return 1
            else:
                return 0
    
        total_score = self.immunology_score() + inflammation_score + joint_score + duration_score
        return total_score
    
class HandData(db.Model):
    def __init__(self):
        self.id = db.Column(db.Integer, primary_key=True)
        self.user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        self.datetime = db.Column(db.DateTime, nullable=False)
        self.right_hand_path = db.Column(db.String(255), nullable=False)
        self.left_hand_path = db.Column(db.String(255), nullable=False)

class JointData(db.Model):
    def __init__(self):
        self.id = db.Column(db.Integer, primary_key=True)
        self.dip_joint_left_2 = db.Column(db.Integer)
        self.dip_joint_left_3 = db.Column(db.Integer)
        self.dip_joint_left_4 = db.Column(db.Integer)
        self.dip_joint_left_5 = db.Column(db.Integer)
        self.dip_joint_right_2 = db.Column(db.Integer)
        self.dip_joint_right_3 = db.Column(db.Integer)
        self.dip_joint_right_4 = db.Column(db.Integer)
        self.dip_joint_right_5 = db.Column(db.Integer)
        self.thumb_ip_joint_left = db.Column(db.Integer)
        self.thumb_ip_joint_right = db.Column(db.Integer)
        self.pip_joint_left_2 = db.Column(db.Integer)
        self.pip_joint_left_3 = db.Column(db.Integer)
        self.pip_joint_left_4 = db.Column(db.Integer)
        self.pip_joint_left_5 = db.Column(db.Integer)
        self.pip_joint_right_2 = db.Column(db.Integer)
        self.pip_joint_right_3 = db.Column(db.Integer)
        self.pip_joint_right_4 = db.Column(db.Integer)
        self.pip_joint_right_5 = db.Column(db.Integer)
        self.mp_joint_left_1 = db.Column(db.Integer)
        self.mp_joint_left_2 = db.Column(db.Integer)
        self.mp_joint_left_3 = db.Column(db.Integer)
        self.mp_joint_left_4 = db.Column(db.Integer)
        self.mp_joint_left_5 = db.Column(db.Integer)
        self.mp_joint_right_1 = db.Column(db.Integer)
        self.mp_joint_right_2 = db.Column(db.Integer)
        self.mp_joint_right_3 = db.Column(db.Integer)
        self.mp_joint_right_4 = db.Column(db.Integer)
        self.mp_joint_right_5 = db.Column(db.Integer)
        self.wrist_joint_hand_left = db.Column(db.Integer)
        self.wrist_joint_hand_right = db.Column(db.Integer)
        self.elbow_joint_left = db.Column(db.Integer)
        self.elbow_joint_right = db.Column(db.Integer)
        self.shoulder_joint_left = db.Column(db.Integer)
        self.shoulder_joint_right = db.Column(db.Integer)
        self.hip_joint_left = db.Column(db.Integer)
        self.hip_joint_right = db.Column(db.Integer)
        self.knee_joint_left = db.Column(db.Integer)
        self.knee_joint_right = db.Column(db.Integer)
        self.ankle_joint_left = db.Column(db.Integer)
        self.ankle_joint_right = db.Column(db.Integer)
        self.mtp_joint_left_1 = db.Column(db.Integer)
        self.mtp_joint_left_2 = db.Column(db.Integer)
        self.mtp_joint_left_3 = db.Column(db.Integer)
        self.mtp_joint_left_4 = db.Column(db.Integer)
        self.mtp_joint_left_5 = db.Column(db.Integer)
        self.mtp_joint_right_1 = db.Column(db.Integer)
        self.mtp_joint_right_2 = db.Column(db.Integer)
        self.mtp_joint_right_3 = db.Column(db.Integer)
        self.mtp_joint_right_4 = db.Column(db.Integer)
        self.mtp_joint_right_5 = db.Column(db.Integer)
        self.distal_joints = db.Column(db.Integer)
        self.proximal_joints = db.Column(db.Integer)

