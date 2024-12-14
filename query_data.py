import random
import json
import os
import re

class TransactionFilterDatasetGenerator:
    def __init__(self):
        self.commands = ['Fetch', 'Get', 'Query', 'Load', 'Read', 'Pull', 'Show', 'List']
        self.orders = ['latest', 'oldest', 'recent', 'earliest', 'most recent', 'last']
        self.functions = ["setup", "on", "off", "feedback", "getStatus", "mute", "volumeUp", "volumeDown"]
        self.transaction_words = ['', 'transaction', 'transactions', 'txn', 'txns']
        self.number_words = {
            1: ['one', '1'],
            2: ['two', '2'],
            3: ['three', '3'],
            4: ['four', '4'],
            5: ['five', '5'],
            6: ['six', '6'],
            7: ['seven', '7'],
            8: ['eight', '8'],
            9: ['nine', '9'],
            10: ['ten', '10']
        }
        self.dataset = {"dataset": []}
    
    def get_random_count(self):
        """숫자나 단어로 된 카운트 반환"""
        if random.choice([True, False]):  # 숫자를 사용할지 단어를 사용할지 결정
            number = random.randint(1, 10)
            choices = [None, random.choice(self.number_words[number])]
            return random.choice(choices)
        return 'all'
    
    def word_to_number(self, word):
        """숫자 단어를 숫자로 변환"""
        if word is None or word == 'all':
            return word
        
        if str(word).isdigit():
            return word
            
        for num, words in self.number_words.items():
            if word.lower() in [w.lower() for w in words]:
                return str(num)
        return word
    
    def random_pk(self):
        return ''.join(random.choices('abcdef0123456789', k=130))

    def random_timestamp(self):
        return str(random.randint(1730780906, 1800000000))
    
    def generate_input(self):
        command = random.choice(self.commands)
        transaction_word = random.choice(self.transaction_words)
        count = self.get_random_count() 
        order = random.choice(self.orders) if random.choice([True, False]) else None
        
        conditions = self.generate_conditions()

        input_parts = [command]
        if count is not None:
            input_parts.append(str(count))
        if order:
            input_parts.append(order)
        if transaction_word:
            input_parts.append(transaction_word)
        input_parts.append(conditions)

        return " ".join(input_parts).strip(), count
    
    def generate_conditions(self):
        """조건을 생성"""
        conditions = []
        to_address = self.random_pk() if random.choice([True, False]) else None
        from_or_by_address = self.random_pk() if random.choice([True, False]) else None
        func = random.choice(self.functions) if random.choice([True, False]) else None
        timestamp = random.choice([f"after {self.random_timestamp()}", f"before {self.random_timestamp()}"]) if random.choice([True, False]) else None
        
        if to_address:
            conditions.append(f"to {to_address}")
        if from_or_by_address:
            if random.choice([True, False]):
                conditions.append(f"from {from_or_by_address}")
            else:
                conditions.append(f"by {from_or_by_address}")
        if func:
            conditions.append(f"{func}")
        if timestamp:
            conditions.append(timestamp)

        if not conditions:
            fallback_filter = random.choice(['to', 'from', 'by', 'func', 'timestamp'])
            if fallback_filter == 'to':
                address = self.random_pk()
                conditions.append(f"to {address}")
            elif fallback_filter == 'from' or 'by':
                address = self.random_pk()
                if random.choice([True, False]):
                    conditions.append(f"from {address}")
                else:
                    conditions.append(f"by {address}")
            elif fallback_filter == 'func':
                func = random.choice(self.functions)
                conditions.append(f"{func}")
            elif fallback_filter == 'timestamp':
                timestamp = self.random_timestamp()
                conditions.append(random.choice([f"after {timestamp}", f"before {timestamp}"]))
        
        return " AND ".join(conditions).strip()

    def generate_sql_query(self, input_text):
        """입력 텍스트를 바탕으로 SQL 쿼리 생성"""
        query = "SELECT * FROM transactions WHERE "
        conditions = []

        # pk, src_pk, func_name, timestamp 필터링
        if "to " in input_text:
            pk = input_text.split("to ")[-1].split()[0]
            conditions.append(f"pk = '{pk}'")
        
        if "from " in input_text or "by " in input_text:
            src_pk = input_text.split("from ")[-1].split()[0] if "from " in input_text else input_text.split("by ")[-1].split()[0]
            conditions.append(f"src_pk = '{src_pk}'")
        
        if any(func in input_text for func in self.functions):
            func_name = next(func for func in self.functions if func in input_text)
            func_name = func_name.replace(' function', '')
            conditions.append(f"func_name = '{func_name}'")

        # timestamp 처리
        if "after " in input_text:
            timestamp = input_text.split("after ")[-1].split()[0]
            conditions.append(f"timestamp > {timestamp}")
        elif "before " in input_text:
            timestamp = input_text.split("before ")[-1].split()[0]
            conditions.append(f"timestamp < {timestamp}")
        elif "between " in input_text:
            match = re.search(r"between (\d+) and (\d+)", input_text)
            if match:
                start_time, end_time = match.groups()
                conditions.append(f"timestamp BETWEEN {start_time} AND {end_time}")
        
        # 조건들을 추가한 후, 최종 쿼리 생성
        if conditions:
            query += " AND ".join(conditions)
        
        # order 처리
        if "latest" in input_text or "most recent" in input_text:
            query += " ORDER BY timestamp DESC"
        elif "oldest" in input_text or "earliest" in input_text:
            query += " ORDER BY timestamp ASC"
        
        return query
    
    def generate_dataset(self, n=10):
        for _ in range(n):
            input_text, count = self.generate_input()
            query = self.generate_sql_query(input_text)
            self.dataset["dataset"].append({"input": input_text, "output": query})

        return len(self.dataset["dataset"])

# Dataset 생성
generator = TransactionFilterDatasetGenerator()
dataset = generator.generate_dataset(10000)

# 파일 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(current_dir, "query_data.json")

# JSON 파일로 저장
with open(filepath, 'w') as json_file:
    json.dump(generator.dataset, json_file, indent=4)

print(f"Generated {len(generator.dataset['dataset'])} samples.")
