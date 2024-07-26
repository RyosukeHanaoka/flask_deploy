import pandas as pd
from sqlalchemy import create_engine

# データベースパス
db_path = '/Users/hanaokaryousuke/flask/apps/instance/app.db'
engine = create_engine(f'sqlite:///{db_path}')

# SQLクエリを実行してデータを取得
query = "SELECT * FROM table_name"  # 必要に応じてテーブル名を変更してください
data = pd.read_sql(query, engine)

# データの確認
#print(data.head())

# 独立変数と従属変数の分割
X = data.drop(columns=['ra', 'id', 'timestamp'])  # 'ra', 'id', 'timestamp' 列を削除して独立変数を取得
y = data['ra']  # 'ra' 列を従属変数として取得

from sklearn.model_selection import train_test_split

# 訓練データとテストデータの分割
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from sklearn.preprocessing import StandardScaler

# 標準化
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# ロジスティック回帰モデルの初期化とトレーニング
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train_scaled, y_train)

# テストデータでの評価
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
print(f'Test Accuracy: {accuracy:.2f}')

import joblib

# モデルとスケーラーの保存
joblib.dump(model, 'logistic_regression_model.pkl')
joblib.dump(scaler, 'scaler.pkl')

# モデルとスケーラーの読み込み
model = joblib.load('logistic_regression_model.pkl')
scaler = joblib.load('scaler.pkl')

# 新しいデータの読み込みと前処理（例として新しいデータフレーム new_data と仮定）
new_data = pd.read_sql("SELECT * FROM new_data_table", engine)  # 必要に応じてテーブル名を変更してください
"""new_data = pd.DataFrame({
    'age': [45],
    'gender': [1],
    'duration': [200],
    'stiffness_duration': [],
    'dip_joint_right_2': [0],
    'dip_joint_right_3': [0],
    'dip_joint_right_4': [0],
    'dip_joint_right_5': [0],
    'dip_joint_left_2': [0],
    'dip_joint_left_3': [0],
    'dip_joint_left_4': [0],
    'dip_joint_left_5': [0],
    'pip_joint_right_2': [0],
    'pip_joint_right_3': [0],
    'pip_joint_right_4': [0],
    'pip_joint_right_5': [0],
    'pip_joint_left_2': [0],
    'pip_joint_left_3': [0],
    'pip_joint_left_4': [0],
    'pip_joint_left_5': [0],
    'mp_joint_right_1': [0],
    'mp_joint_right_2': [0],
    'mp_joint_right_3': [1],
    'mp_joint_right_4': [0],
    'mp_joint_right_5': [0],
    'mp_joint_left_1': [0],
    'mp_joint_left_2': [0],
    'mp_joint_left_3': [0],
    'mp_joint_left_4': [0],
    'mp_joint_left_5': [0],
    'thumb_ip_joint_right': [0],
    'thumb_ip_joint_left': [0],
    'wrist_joint_hand_right': [0],
    'wrist_joint_hand_left': [0],
    'elbow_joint_right': [0],
    'elbow_joint_left': [0],
    'shoulder_joint_right': [0],
    'shoulder_joint_left': [0],
    'hip_joint_right': [0],
    'hip_joint_left': [0],
    'knee_joint_right': [0],
    'knee_joint_left': [0],
    'ankle_joint_right': [0],
    'ankle_joint_left': [1],
    'mtp_joint_right_1': [0],
    'mtp_joint_right_2': [1],
    'mtp_joint_right_3': [0],
    'mtp_joint_right_4': [0],
    'mtp_joint_right_5': [0],
    'mtp_joint_left_1': [0],
    'mtp_joint_left_2': [0],
    'mtp_joint_left_3': [1],
    'mtp_joint_left_4': [0],
    'mtp_joint_left_5': [0],
})"""

# 必要な場合、列を正しい順序に並べ替え
new_data = new_data[X.columns]

# 新しいデータの標準化
new_data_scaled = scaler.transform(new_data)

# 予測
new_pred = model.predict(new_data_scaled)
print(f'Predicted RA: {new_pred[0]}')
