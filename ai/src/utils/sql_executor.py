# ai/src/utils/sql_executor.py
import pandas as pd
import sqlite3
import os

class SQLExecutor:
    """SQL 쿼리를 직접 실행하는 클래스"""
    
    def __init__(self, csv_path):
        """CSV 데이터를 SQLite DB로 변환하고 연결 초기화"""
        self.db_path = csv_path.replace('.csv', '.db')
        
        try:
            # CSV 데이터 읽기
            df = pd.read_csv(csv_path)
            
            # SQLite 데이터베이스 생성 및 연결
            self.conn = sqlite3.connect(self.db_path)
            
            # CSV 데이터를 SQLite 테이블로 변환
            df.to_sql('transactions', self.conn, if_exists='replace', index=False)
            print(f"Loaded {len(df)} records into SQLite database")
            
        except Exception as e:
            print(f"Error initializing database: {str(e)}")
            raise
    
    def execute_query(self, query):
        """SQL 쿼리 직접 실행"""
        try:
            return pd.read_sql_query(query, self.conn)
        except Exception as e:
            print(f"Error executing query: {str(e)}")
            return None
    
    def close(self):
        """데이터베이스 연결 종료"""
        if self.conn:
            self.conn.close()
        # 임시 DB 파일 삭제
        if os.path.exists(self.db_path):
            os.remove(self.db_path)