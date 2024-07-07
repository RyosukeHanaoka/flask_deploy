from .extensions import db

class JointData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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

