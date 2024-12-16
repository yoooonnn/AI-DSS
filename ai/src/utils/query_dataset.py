import random
import json
import os
from datetime import datetime

class QueryInputGenerator:
    def __init__(self):
        self.device_functions = {
            'Speaker': ['turnOn', 'turnOff', 'getJoke', 'getWeather', 'getNews', 'getTime', 'getReminder', 'getMusic'],
            'Light': ['turnOn', 'turnOff', 'setBrightness', 'setMode', 'setColor']
        }
        
        self.light_modes = ['normal', 'night', 'reading', 'party']
        self.light_colors = ['red', 'green', 'blue', 'yellow', 'white']
        self.brightness_values = [i for i in range(1, 101)]
        
        # Order related keywords
        self.orders = ['latest', 'most recent', 'last', 'oldest', 'first']
        self.desc_orders = ['latest', 'most recent', 'last']  # 내림차순(최신순)
        self.asc_orders = ['oldest', 'first']  # 오름차순(과거순)

    def random_pk(self):
        return ''.join(random.choices('abcdef0123456789', k=130))

    def generate_conditions(self):
        conditions = [
            'from_by_hex',
            'to_hex',
            'function',
            'device_type',
            'count',
            'order'
        ]
        
        num_conditions = random.randint(1, len(conditions))
        selected_conditions = random.sample(conditions, num_conditions)
        
        query_parts = []
        device = None
        has_count = False
        has_order = False
        
        for condition in selected_conditions:
            if condition == 'from_by_hex':
                hex_from = self.random_pk()
                use_from = random.choice([True, False])
                query_parts.append(f"{'from' if use_from else 'by'} {hex_from}")
            
            elif condition == 'to_hex':
                hex_to = self.random_pk()
                query_parts.append(f"to {hex_to}")
            
            elif condition == 'function':
                if not device:
                    device = random.choice(['Speaker', 'Light'])
                function = random.choice(self.device_functions[device])
                query_parts.append(f"{function}")
            
            elif condition == 'device_type':
                if not device:
                    device = random.choice(['Speaker', 'Light'])
                query_parts.append(f"{device.lower()} transactions")
            
            elif condition == 'count':
                has_count = True
                count_type = random.choice(['all', None])
                if count_type == 'all':
                    query_parts.insert(0, count_type)
            
            elif condition == 'order':
                has_order = True
                order = random.choice(self.orders)
                query_parts.append(order)
        
        # Add order info to return value
        order_info = {
            'has_order': has_order,
            'has_count': has_count
        }
        
        return " ".join(query_parts).strip(), order_info

    def generate_input(self):
        conditions, order_info = self.generate_conditions()
        
        # Extract count if exists
        count = None
        if conditions.startswith('all '):
            count = 'all'
            conditions = conditions[4:]

        # Build final query
        query = f"Show {conditions}"
        
        # Determine if we need to set LIMIT 1
        needs_limit_1 = False
        
        # If query has order keywords but no 'all' count, set LIMIT 1
        if any(order in query.lower() for order in self.orders) and count != 'all':
            needs_limit_1 = True
        
        # If no explicit order in query, add default DESC order
        order_type = None
        if any(order in query.lower() for order in self.desc_orders):
            order_type = 'DESC'
        elif any(order in query.lower() for order in self.asc_orders):
            order_type = 'ASC'
        else:
            order_type = 'DESC'  # 기본값
        
        return query.strip(), count, order_type, needs_limit_1

class QueryOutputGenerator:
    def __init__(self):
        self.functions = QueryInputGenerator().device_functions

    def generate_sql_query(self, input_text, count=None, order_type='DESC', needs_limit_1=False):
        """Generates SQL query based on input text and parameters"""
        base_query = "SELECT * FROM transactions"
        conditions = []

        # Handle device and function filtering
        if "to " in input_text:
            pk = input_text.split("to ")[-1].split()[0]
            conditions.append(f"user_id = '{pk}'")
        
        if "from " in input_text or "by " in input_text:
            # Handle both 'from' and 'by' cases
            if "from " in input_text:
                device_pk = input_text.split("from ")[-1].split()[0]
            else:
                device_pk = input_text.split("by ")[-1].split()[0]
            conditions.append(f"device_id = '{device_pk}'")
        
        # Function filtering
        if any(func in input_text for func in self.functions['Speaker'] + self.functions['Light']):
            func_name = next(func for func in self.functions['Speaker'] + self.functions['Light'] if func in input_text)
            conditions.append(f"function = '{func_name}'")
        
        # Device type filtering
        if "speaker" in input_text.lower():
            conditions.append("device_type = 'Speaker'")
        elif "light" in input_text.lower():
            conditions.append("device_type = 'Light'")
        
        # Add WHERE clause if conditions exist
        if conditions:
            base_query += " WHERE " + " AND ".join(conditions)
        
        # Add ORDER BY
        base_query += f" ORDER BY timestamp {order_type}"
        
        # Handle LIMIT
        if count == 'all':
            # No LIMIT when 'all' is specified
            pass
        elif needs_limit_1:
            base_query += " LIMIT 1"
        
        return base_query

class QueryDatasetGenerator:
    def __init__(self):
        self.input_generator = QueryInputGenerator()
        self.output_generator = QueryOutputGenerator()
        self.dataset = {"dataset": []}

    def generate_dataset(self, n=10):
        """Generates n samples of input-query pairs"""
        for _ in range(n):
            # Get input query and parameters
            input_text, count, order_type, needs_limit_1 = self.input_generator.generate_input()
            
            # Generate SQL query
            query = self.output_generator.generate_sql_query(
                input_text,
                count,
                order_type,
                needs_limit_1
            )
            
            # Add to dataset with all parameters for reference
            self.dataset["dataset"].append({
                "input": input_text,
                "parameters": {
                    "count": count,
                    "order_type": order_type,
                    "needs_limit_1": needs_limit_1
                },
                "output": query
            })

        return len(self.dataset["dataset"])

    def save_to_file(self, filepath="query_data.json"):
        """Saves the generated dataset to a JSON file"""
        with open(filepath, 'w', encoding='utf-8') as json_file:
            json.dump(self.dataset, json_file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    # Generate dataset
    generator = QueryDatasetGenerator()
    num_samples = generator.generate_dataset(10000)
    
    # Save to JSON file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(current_dir, "..", "..", "data", "query_data.json")
    generator.save_to_file(filepath)
    
    print(f"Generated {num_samples} samples.")
