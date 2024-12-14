import random
import pandas as pd
from datetime import datetime, timedelta

# 기기 종류와 각 기기별 Interaction Types 및 상태 정보 정의
devices = ['Fridge', 'Vacuum', 'Air Conditioner', 'TV', 'Smart Light', 'Smart Plug', 'Smart Lock', 'Smart Scale', 'Smart Hub', 'Smart Coffee Machine', 'Smart Security Camera']

interaction_types = {
    'Fridge': {
        'powered on': ['temperature change', 'door open', 'door close'],
        'powered off': []
    },
    'Vacuum': {
        'cleaning': ['stop cleaning'],
        'idle': ['start cleaning', 'battery check'],
        'battery low': [],
        'powered off': []
    },
    'Air Conditioner': {
        'powered on': ['temperature change', 'mode change', 'fan speed change'],
        'powered off': []
    },
    'TV': {
        'on': ['volume change', 'channel change', 'mute'],
        'off': []
    },
    'Smart Light': {
        'on': ['brightness change', 'color change', 'mode change'],
        'off': []
    },
    'Smart Plug': {
        'on': ['turn off', 'check power consumption'],
        'off': ['turn on', 'check power consumption']
    },
    'Smart Lock': {
        'locked': ['unlock', 'check status'],
        'unlocked': ['lock', 'check status'],
        'locking in progress': ['lock', 'check status'],
    },
    'Smart Scale': {
        'measuring': ['measure weight', 'check BMI'],
        'idle': ['check BMI'],
    },
    'Smart Hub': {
        'connected': ['check device status', 'add new device'],
        'disconnected': ['reconnect', 'check device status'],
    },
    'Smart Coffee Machine': {
        'brewing': ['stop brewing', 'check coffee level'],
        'idle': ['start brewing', 'check coffee level'],
    },
    'Smart Security Camera': {
        'recording': ['stop recording', 'rotate camera'],
        'idle': ['start recording', 'rotate camera'],
    }
}

device_status = {
    'Fridge': ['powered on', 'powered off'],
    'Vacuum': ['cleaning', 'idle', 'battery low', 'powered off'],
    'Air Conditioner': ['powered on', 'powered off'],
    'TV': ['on', 'off'],
    'Smart Light': ['on', 'off'],
    'Smart Plug': ['on', 'off'],
    'Smart Lock': ['locked', 'unlocked', 'locking in progress'],
    'Smart Scale': ['measuring', 'idle'],
    'Smart Hub': ['connected', 'disconnected'],
    'Smart Coffee Machine': ['brewing', 'idle'],
    'Smart Security Camera': ['recording', 'idle'],
}

# 디바이스별 고유 ID 접두사 설정
device_id_prefixes = {
    'Fridge': 'F00', 
    'Vacuum': 'V00', 
    'Air Conditioner': 'AC0', 
    'TV': 'T00', 
    'Smart Light': 'SL0', 
    'Smart Plug': 'SP0', 
    'Smart Lock': 'SLK', 
    'Smart Scale': 'SS0', 
    'Smart Hub': 'SH0', 
    'Smart Coffee Machine': 'SCM', 
    'Smart Security Camera': 'SSC'
}

# 랜덤 4자리 디바이스 ID 생성 (접두사 + 4자리 랜덤 숫자)
def generate_device_id(device):
    prefix = device_id_prefixes[device]
    random_suffix = ''.join(random.choices('0123456789', k=4))  # 4자리 랜덤 숫자
    return prefix + random_suffix

# 빈 데이터프레임 생성
data = []

for i in range(10000):  # 10000개의 데이터 생성
    device = random.choice(devices)  # 랜덤으로 기기 선택
    device_id = generate_device_id(device)
    status = random.choice(device_status[device])  # 선택된 기기의 상태 중 하나 선택
    
    # 상태에 맞는 상호작용이 있을 경우만 선택
    possible_interactions = interaction_types[device].get(status, [])
    if possible_interactions:
        interaction_type = random.choice(possible_interactions)  # 상태에 맞는 상호작용 선택
        timestamp = datetime.now() - timedelta(minutes=random.randint(1, 60))
        user_id = random.randint(1, 9)  # 사용자 ID는 1~9 중 랜덤 선택
        
        data.append({
            'User ID': user_id,
            'Device ID': device_id,
            'Device': device,
            'Interaction Type': interaction_type,
            'Status': status,
            'Timestamp': timestamp.strftime("%Y-%m-%d %H:%M:%S")
        })

df = pd.DataFrame(data)

# 결과를 CSV 파일로 저장
df.to_csv('interaction_data.csv', index=False)

# 결과 출력
print("CSV 파일로 저장 완료. 'interaction_data_with_user.csv' 파일을 확인하세요.")
