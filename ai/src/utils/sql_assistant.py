
# ai/src/utils/sql_assistant.py
from config.model_config import ModelConfig
from trainer.sql_trainer import SQLTrainer
from utils.sql_executor import SQLExecutor

class SQLAssistant:
    """자연어를 SQL로 변환하고 실행을 관리하는 클래스"""
    
    def __init__(self, db_path):
        """SQL 어시스턴트 초기화"""
        # AI 모델 초기화
        print("Loading model...")
        self.config = ModelConfig()
        self.trainer = SQLTrainer(self.config)
        self.trainer.load_model(self.config.output_dir)
        
        # SQL 실행기 초기화
        print("Connecting to database...")
        self.executor = SQLExecutor(db_path)
    
    def process_query(self, text_input, execute=True):
        """자연어 쿼리 처리 및 실행"""
        try:
            # SQL 쿼리 생성
            sql_query = self.trainer.generate_sql(text_input)
            print("\nGenerated SQL Query:")
            print("-" * 50)
            print(sql_query)
            print("-" * 50)
            
            # SQL 실행 (요청된 경우)
            if execute:
                result = self.executor.execute_query(sql_query)
                if result is not None:
                    print("\nQuery Result:")
                    print("-" * 50)
                    print(result)
                    print("-" * 50)
                return sql_query, result
            
            return sql_query, None
            
        except Exception as e:
            print(f"Error processing query: {str(e)}")
            return None, None
    
    def close(self):
        """리소스 정리"""
        if self.executor:
            self.executor.close()