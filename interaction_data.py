import random
import time
import secrets
import csv
import os

def generate_random_hex(length=64):
    """Generate a random hex string of specified length"""
    return secrets.token_hex(length // 2)

def generate_public_key():
    """Generate a random public key starting with '04'"""
    return "04" + generate_random_hex(128)

def generate_raw_data():
    """Generate random raw data similar to the example"""
    parts = [
        "6337b0bdd7a7f41fc0dae95d2472ee28",
        "648d371c92a49eba91aad29c8e7a0845",
        "f227a163546181e9d87a60e660c73cc9",
        "983139404f4dcd9d12380e8368b652d3",
        "666565646261636b000000000000000000",
        generate_random_hex(64),
        generate_random_hex(32)
    ]
    return "".join(parts)

def generate_transaction_data(num_pks=6, base_timestamp=None):
    """
    Generate transaction data where each pk has one src_pk,
    and each src_pk has one transaction.
    
    Args:
        num_pks (int): Number of different pks
        base_timestamp (int): Starting timestamp (optional)
    """
    if base_timestamp is None:
        base_timestamp = int(time.time())
    
    function_names = ["setup", "on", "off", "feedback", "getStatus", "mute", "volumeUp", "volumeDown"]
    result = []
    current_timestamp = base_timestamp
    
    # CSV 저장을 위한 데이터 준비
    csv_data = []
    
    # CSV 헤더 추가
    csv_data.append(["pk", "src_pk", "raw_data", "timestamp", "func_name"])
    
    # 각 pk에 대해
    for _ in range(num_pks):
        main_pk = generate_public_key()  # Generate a new pk for each entry
        src_pk = generate_public_key()   # Each pk gets a single src_pk
        
        # 각 src_pk마다 1개의 트랜잭션 생성
        csv_data.append((
            main_pk,      # pk
            src_pk,       # src_pk
            generate_raw_data(),  # raw_data
            str(current_timestamp),  # timestamp
            random.choice(function_names)  # func_name 랜덤 선택
        ))
        current_timestamp += 1
    
    return csv_data

def save_to_csv(data, filename='interaction_data.csv'):
    """Save data to CSV file"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(current_dir, filename)
    
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)
    
    print(f"Data saved to {filepath}")

# 실행 코드
if __name__ == "__main__":
    base_timestamp = 1733045250
    transactions = generate_transaction_data(
        num_pks=100000,
        base_timestamp=base_timestamp
    )
    
    # CSV 파일로 저장
    save_to_csv(transactions)
