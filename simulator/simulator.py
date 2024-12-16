from datetime import datetime, timedelta
import random
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from devices.light import Light
from utils.user_pattern import user_patterns

class SmartHomeSimulator:
    def __init__(self):
        self.devices = {}  
        self.users = {}  
        self.logs = []
        
    def add_device(self, device_id, device_type, user_id):
        if device_type == 'light':
            self.devices[device_id] = Light(device_id, user_id)
        # 다른 기기 타입들도 비슷하게 추가
            
    def simulate(self, start_time, duration_hours):
        current_time = start_time
        end_time = start_time + timedelta(hours=duration_hours)
        
        while current_time < end_time:
            # 각 기기별로 상호작용 생성 여부 결정
            for device in self.devices.values():
                user_type = self.users[device.user_id]
                if self._should_interact(current_time, user_type):
                    interaction = device.generate_action(current_time)
                    self.logs.append(interaction)
            
            # 시간 진행 (1-5분 랜덤)
            current_time += timedelta(minutes=random.randint(1, 5))
            
    def _should_interact(self, time, user_type):
        pattern = user_patterns[user_type]
        
        # 활성 시간대 체크
        is_active_hour = any(start <= time.hour < end 
                           for start, end in pattern['active_hours'])
        
        # 요일별 확률 적용
        is_weekday = time.weekday() < 5
        prob = pattern['interaction_probability']['weekday' if is_weekday else 'weekend']
        
        return is_active_hour and random.random() < prob