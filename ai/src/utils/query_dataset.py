import random
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple

class IoTQueryGenerator:
    def __init__(self):
        self.device_types = ['Speaker', 'Light']
        self.functions = {
            'Speaker': ['turnOn', 'turnOff', 'getTime', 'getNews', 'getWeather'],
            'Light': ['turnOn', 'turnOff', 'setColor', 'setMode', 'setBrightness']
        }
        
        self.parameters = {
            'Light': {
                'mode': ['normal', 'night', 'reading', 'party'],
                'color': ['red', 'white', 'blue', 'green', 'yellow'],
                'brightness': ['0', '25', '50', '75', '100']
            }
        }
        
        self.superlatives = {
            'most recent': 'DESC',
            'latest': 'DESC',
            'last': 'DESC',
            'newest': 'DESC',
            'oldest': 'ASC',
            'first': 'ASC',
            'earliest': 'ASC'
        }

        self.time_ranges = ['hour', 'day', 'date', 'month', 'year']
        
        self.query_patterns = [
            # Previous patterns remain the same...
            
            # Time-based Analysis Patterns
            {
                'templates': [
                    "Show me hourly usage patterns for {device_type}",
                    "What are the peak hours for {device_type}",
                    "Display activity distribution by hour for {device_type}",
                    "When is {device_type} used most frequently",
                    "Give me hour-by-hour analysis of {device_type}",
                    "How does {device_type} usage vary throughout the day"
                ],
                'sql_type': 'time_stats',
                'time_grouping': 'hour',
                'sql_conditions': ['device_type']
            },
            {
                'templates': [
                    "Show me daily trends for {function}",
                    "What's the daily pattern of {function} usage",
                    "Analyze {function} usage by day",
                    "Display day-by-day breakdown of {function}",
                    "How often is {function} used each day",
                    "Get daily statistics for {function}"
                ],
                'sql_type': 'time_stats',
                'time_grouping': 'date',
                'sql_conditions': ['function']
            },
            {
                'templates': [
                    "Show monthly usage trends for {device_type}",
                    "How does {device_type} usage vary by month",
                    "Give me month-by-month analysis of {device_type}",
                    "Display monthly patterns for {device_type}",
                    "What's the monthly usage distribution of {device_type}"
                ],
                'sql_type': 'time_stats',
                'time_grouping': 'month',
                'sql_conditions': ['device_type']
            },
            {
                'templates': [
                    "Show me usage patterns by time of day for {function}",
                    "When do people use {function} most",
                    "What time of day is {function} most active",
                    "Display hourly distribution of {function} usage",
                    "Analyze peak times for {function}"
                ],
                'sql_type': 'time_stats',
                'time_grouping': 'hour',
                'sql_conditions': ['function']
            }
        ]

    def generate_time_stats_query(self, pattern: Dict, components: Dict) -> str:
        conditions = [f"{cond} = '{components[cond]}'" for cond in pattern['sql_conditions']]
        time_grouping = pattern['time_grouping']
        
        # Define time extraction based on grouping
        time_extracts = {
            'hour': "HOUR(timestamp)",
            'date': "DATE(timestamp)",
            'month': "DATE_FORMAT(timestamp, '%Y-%m')",
            'year': "YEAR(timestamp)"
        }
        
        time_extract = time_extracts[time_grouping]
        
        sql_query = f"""SELECT 
                        {time_extract} as {time_grouping},
                        COUNT(*) as count,
                        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() as percentage
                    FROM transactions"""
        
        if conditions:
            sql_query += " WHERE " + " AND ".join(conditions)
        
        sql_query += f" GROUP BY {time_extract} ORDER BY {time_grouping}"
        
        return sql_query

    def generate_query_pair(self) -> Dict:
        pattern = random.choice(self.query_patterns)
        
        components = {
            'device_type': random.choice(self.device_types),
            'device_id': self.random_hex_id(),
            'user_id': self.random_hex_id(),
            'function': random.choice(self.functions[random.choice(self.device_types)])
        }
        
        if pattern.get('has_superlative'):
            components['superlative'] = random.choice(list(self.superlatives.keys()))
            order = self.superlatives[components['superlative']]
        else:
            order = pattern.get('order', 'DESC')
        
        input_query = random.choice(pattern['templates']).format(**components)
        
        if pattern.get('sql_type') == 'time_stats':
            sql_query = self.generate_time_stats_query(pattern, components)
        elif pattern.get('sql_type') == 'stats':
            sql_query = self.generate_stats_query(pattern, components)
        else:
            conditions = [f"{cond} = '{components[cond]}'" for cond in pattern['sql_conditions']]
            
            sql_query = "SELECT * FROM transactions"
            if conditions:
                sql_query += " WHERE " + " AND ".join(conditions)
            
            sql_query += f" ORDER BY timestamp {order}"
            
            if pattern.get('has_superlative'):
                sql_query += " LIMIT 1"
        
        return {
            "input": input_query,
            "output": sql_query
        }
    
    def random_hex_id(self) -> str:
        return ''.join(random.choices('abcdef0123456789', k=128))

    def generate_stats_query(self, pattern: Dict, components: Dict) -> str:
        conditions = [f"{cond} = '{components[cond]}'" for cond in pattern['sql_conditions']]
        group_by = pattern['group_by']
        
        sql_query = f"""SELECT value as {group_by}, 
                        COUNT(*) as count, 
                        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() as percentage
                    FROM transactions"""
        
        if conditions:
            sql_query += " WHERE " + " AND ".join(conditions)
        
        sql_query += f" GROUP BY value ORDER BY count DESC"
        
        return sql_query

class DatasetGenerator:

    def __init__(self):
        self.generator = IoTQueryGenerator()
        self.dataset = {"dataset": []}

    def generate_dataset(self, n: int = 1000) -> None:
        for _ in range(n):
            query_pair = self.generator.generate_query_pair()
            self.dataset["dataset"].append(query_pair)

    def save_dataset(self, filepath: str = "query_dataset.json"):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.dataset, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    # 1. 제너레이터 생성
    generator = DatasetGenerator()
    
    # 2. 데이터셋 생성 (예: 1000개 샘플)
    generator.generate_dataset(10000)
    
    # 3. 현재 디렉토리에 저장
    current_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(current_dir, "query_dataset.json")
    generator.save_dataset(filepath)
    
    # 4. 확인을 위한 출력
    print(f"Dataset saved to: {filepath}")
    print("\nSample entries:")
    for i, sample in enumerate(generator.dataset["dataset"][:3], 1):
        print(f"\nSample {i}:")
        print("Input:", sample["input"])
        print("Output:", sample["output"])