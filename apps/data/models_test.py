from models import User, Symptom, Criteria

"""symptom=Symptom(
    0,
    "male",
    1983,
    12,
    7,
    2023,
    4,
    5,
    "yes",
    30,
    10,
    1,
)

print(symptom.calculate_age(2024,7,26))
print(symptom.calculate_duration(2024,7,26))
print(symptom.calculate_six_weeks_duration(2024,7,26))
"""
criteria=Criteria(
    0,
    "hanaoka@kamituga-hp.or.jp",
    3.34,
    45,
    478,
    3499   
)
joint_entry={"pip_joint_right_2": [1]}
class Data:
    def __init__(self):
        self.pip_joint_right_2 = 1
joint_entry = Data()

distal_joints = (
            [getattr(joint_entry, f"pip_joint_left_{i}", 0) for i in range(2, 6)] + \
            [getattr(joint_entry, f"pip_joint_right_{i}", 0) for i in range(2, 6)] + \
            [getattr(joint_entry, f"mtp_joint_left_{i}", 0) for i in range(1, 6)] + \
            [getattr(joint_entry, f"mtp_joint_right_{i}", 0) for i in range(1, 6)] + \
            [getattr(joint_entry, "thumb_ip_joint_left", 0), getattr(joint_entry, "thumb_ip_joint_right", 0)] + \
            [getattr(joint_entry, "wrist_joint_hand_left", 0), getattr(joint_entry, "wrist_joint_hand_right", 0)]
        )
print(criteria.distal_joints(joint_entry))
#print(distal_joints)
import unittest
from datetime import datetime
from flask import Flask
from extensions import db
from models import User, Symptom, Criteria, HandData, JointData  # ここでモジュール名を適切に変更してください

class YourTestClass(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(self.app)

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_model(self):
        with self.app.app_context():
            user = User(email='test@example.com', password='password')
            db.session.add(user)
            db.session.commit()
            
            self.assertEqual(user.email, 'test@example.com')
            self.assertTrue(user.check_password('password'))

    def test_symptom_model(self):
        with self.app.app_context():
            user = User(email='test2@example.com', password='password')
            db.session.add(user)
            db.session.commit()

            symptom = Symptom(user_id=user.id, sex='female', birth_year=1990, birth_month=1, birth_day=1, 
                              disease_duration=2, morning_stiffness='yes', 
                              stiffness_duration=30, pain_level=5, six_weeks_duration=6)
            db.session.add(symptom)
            db.session.commit()

            self.assertEqual(symptom.sex, 'female')
            self.assertEqual(symptom.calculate_age(2023, 1, 1), 33)
            self.assertEqual(symptom.calculate_duration(2023, 1, 1), (datetime(2023, 1, 1) - datetime(2020, 1, 1)).days)

    def test_criteria_model(self):
        with self.app.app_context():
            user = User(email='test3@example.com', password='password')
            db.session.add(user)
            db.session.commit()

            criteria = Criteria(user_id=user.id, email='test3@example.com', crp=0.4, esr=20, rf=50, acpa=15)
            criteria.immunology_score = criteria.calculate_immunology_score()
            criteria.inflammation_score = criteria.calculate_inflammation_score(sex=1)
            criteria.joint_score = 3
            criteria.duration_score = 1
            criteria.total_score = criteria.calculate_total_score(criteria.inflammation_score, criteria.joint_score, 1)
            db.session.add(criteria)
            db.session.commit()

            self.assertEqual(criteria.email, 'test3@example.com')
            self.assertEqual(criteria.calculate_immunology_score(), 2)
            self.assertEqual(criteria.calculate_inflammation_score(sex=1), 1)

    def test_hand_data_model(self):
        with self.app.app_context():
            user = User(email='test4@example.com', password='password')
            db.session.add(user)
            db.session.commit()

            hand_data = HandData(user_id=user.id, datetime=datetime.now(), right_hand_path='/path/right', left_hand_path='/path/left')
            db.session.add(hand_data)
            db.session.commit()

            self.assertEqual(hand_data.right_hand_path, '/path/right')

    def test_joint_data_model(self):
        with self.app.app_context():
            user = User(email='test5@example.com', password='password')
            db.session.add(user)
            db.session.commit()

            joint_data = JointData(user_id=user.id, dip_joint_left_2=1, dip_joint_left_3=1, dip_joint_left_4=1, 
                                   dip_joint_left_5=1, dip_joint_right_2=1, dip_joint_right_3=1, dip_joint_right_4=1, 
                                   dip_joint_right_5=1, thumb_ip_joint_left=1, thumb_ip_joint_right=1, pip_joint_left_2=1, 
                                   pip_joint_left_3=1, pip_joint_left_4=1, pip_joint_left_5=1, pip_joint_right_2=1, 
                                   pip_joint_right_3=1, pip_joint_right_4=1, pip_joint_right_5=1, mp_joint_left_1=1, 
                                   mp_joint_left_2=1, mp_joint_left_3=1, mp_joint_left_4=1, mp_joint_left_5=1, mp_joint_right_1=1, 
                                   mp_joint_right_2=1, mp_joint_right_3=1, mp_joint_right_4=1, mp_joint_right_5=1, 
                                   wrist_joint_hand_left=1, wrist_joint_hand_right=1, elbow_joint_left=1, elbow_joint_right=1, 
                                   shoulder_joint_left=1, shoulder_joint_right=1, hip_joint_left=1, hip_joint_right=1, 
                                   knee_joint_left=1, knee_joint_right=1, ankle_joint_left=1, ankle_joint_right=1, 
                                   mtp_joint_left_1=1, mtp_joint_left_2=1, mtp_joint_left_3=1, mtp_joint_left_4=1, 
                                   mtp_joint_left_5=1, mtp_joint_right_1=1, mtp_joint_right_2=1, mtp_joint_right_3=1, 
                                   mtp_joint_right_4=1, mtp_joint_right_5=1, distal_joints=10, proximal_joints=10)
            db.session.add(joint_data)
            db.session.commit()

            self.assertEqual(joint_data.distal_joints, 10)
            self.assertEqual(joint_data.proximal_joints, 10)

if __name__ == '__main__':
    unittest.main()