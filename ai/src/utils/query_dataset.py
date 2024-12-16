import random
import json
import os
from datetime import datetime

class QueryInputGenerator:
    def __init__(self):
        # Define device functions
        self.device_functions = {
            'Speaker': ['turnOn', 'turnOff', 'getJoke', 'getWeather', 'getNews', 'getTime', 'getReminder', 'getMusic'],
            'Light': ['turnOn', 'turnOff', 'setBrightness', 'setMode', 'setColor']
        }

        # Define available modes for Light
        self.light_modes = ['normal', 'night', 'reading', 'party']
        self.light_colors = ['red', 'green', 'blue', 'yellow', 'white']
        self.brightness_values = [i for i in range(1, 101)]  # Brightness from 1 to 100
        
        self.orders = ['latest', 'oldest', 'recent', 'most recent']
        
        self.number_words = {
            1: ['one', '1', 'single'],
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

    def random_pk(self):
        """Generates a random public key (hex string)"""
        return ''.join(random.choices('abcdef0123456789', k=130))

    def get_random_count(self):
        """Returns a count as a number, word, or 'all'"""
        count_type = random.choice(['none', 'number', 'all'])
        
        if count_type == 'none':
            return None
        elif count_type == 'all':
            return 'all'
        else:
            number = random.randint(1, 10)
            use_word = random.choice([True, False])
            return random.choice(self.number_words[number]) if use_word else str(number)

    def generate_conditions(self):
        """Generates random filter conditions for the query"""
        conditions = []
        to_address = self.random_pk() if random.choice([True, False]) else None
        from_or_by_address = self.random_pk() if random.choice([True, False]) else None
        device_type = random.choice(['Speaker', 'Light'])
        
        # Add address-related conditions (optional)
        if to_address:
            conditions.append(f"to {to_address}")
        if from_or_by_address:
            if random.choice([True, False]):
                conditions.append(f"from {from_or_by_address}")
            else:
                conditions.append(f"by {from_or_by_address}")
        
        # Add device-related conditions (Speaker or Light)
        if device_type == 'Speaker':
            conditions.append("device_type = 'Speaker'")
        else:
            conditions.append("device_type = 'Light'")

        # Fallback filter if no condition is generated
        if not conditions:
            fallback_filter = random.choice(['to', 'from', 'by', 'device_type'])
            if fallback_filter == 'to':
                conditions.append(f"to {self.random_pk()}")
            elif fallback_filter in ['from', 'by']:
                address = self.random_pk()
                conditions.append(f"{fallback_filter} {address}")
            else:
                conditions.append(f"device_type = '{device_type}'")
        
        return " ".join(conditions).strip()

    def generate_input(self):
        """Generates a random input command"""
        device_type = random.choice(['Speaker', 'Light'])
        function = random.choice(self.device_functions[device_type])
        count = self.get_random_count()
        order = random.choice(self.orders) if random.choice([True, False]) else None
        
        input_parts = ['Show']
        input_parts.append(function)
        if count is not None:
            input_parts.append(str(count))
        if order:
            input_parts.append(order)
        input_parts.append(self.generate_conditions())
        
        return " ".join(input_parts).strip(), count


class QueryOutputGenerator:
    def __init__(self):
        self.functions = QueryInputGenerator().device_functions

    def word_to_number(self, word, number_words):
        """Converts word representation of numbers to actual numbers"""
        if word is None or word == 'all':
            return word
        
        if str(word).isdigit():
            return str(word)
            
        for num, words in number_words.items():
            if word.lower() in [w.lower() for w in words]:
                return str(num)
        return word

    def generate_sql_query(self, input_text, count=None, number_words=None):
        """Generates SQL query based on input text and count"""
        base_query = "SELECT * FROM transactions"
        conditions = []

        # Handle device and function filtering
        if "to " in input_text:
            pk = input_text.split("to ")[-1].split()[0]
            conditions.append(f"user_id = '{pk}'")
        
        if "from " in input_text or "by " in input_text:
            device_pk = input_text.split("from ")[-1].split()[0] if "from " in input_text else input_text.split("by ")[-1].split()[0]
            conditions.append(f"device_id = '{device_pk}'")
        
        if any(func in input_text for func in self.functions['Speaker'] + self.functions['Light']):
            func_name = next(func for func in self.functions['Speaker'] + self.functions['Light'] if func in input_text)
            conditions.append(f"function = '{func_name}'")
        
        if conditions:
            base_query += " WHERE " + " AND ".join(conditions)
        
        # Handle ordering
        order_needed = False
        if any(word in input_text.lower() for word in ['latest', 'most recent', 'recent']):
            base_query += " ORDER BY timestamp DESC"
            order_needed = True
        elif "oldest" in input_text:
            base_query += " ORDER BY timestamp ASC"
            order_needed = True
        
        # Handle limit
        if count and count != 'all':
            count_num = self.word_to_number(count, number_words)
            if count_num and str(count_num).isdigit():
                base_query += f" LIMIT {count_num}"
        elif order_needed and not count:
            # If no count specified but has ordering keywords, limit to 1
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
            input_text, count = self.input_generator.generate_input()
            query = self.output_generator.generate_sql_query(
                input_text, 
                count, 
                self.input_generator.number_words
            )
            self.dataset["dataset"].append({
                "input": input_text,
                "output": query
            })

        return len(self.dataset["dataset"])

    def save_to_file(self, filepath="query_data.json"):
        """Saves the generated dataset to a JSON file"""
        with open(filepath, 'w') as json_file:
            json.dump(self.dataset, json_file, indent=4)


if __name__ == "__main__":
    # Generate dataset
    generator = QueryDatasetGenerator()
    num_samples = generator.generate_dataset(10000)
    
    # Save to JSON file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(current_dir, "..", "..", "data", "query_data.json")
    generator.save_to_file(filepath)
    
    print(f"Generated {num_samples} samples.")
