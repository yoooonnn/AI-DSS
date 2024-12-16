# ai/src/utils/sql_executor.py
import pandas as pd
import sqlite3
import os

class SQLExecutor:
    """SQL 쿼리를 직접 실행하는 클래스"""
    
    def __init__(self, db_path):
        """SQLite DB로 연결 초기화"""
        self.db_path = db_path
        
        try:
            # SQLite 데이터베이스에 연결
            self.conn = sqlite3.connect(self.db_path)
            print(f"Connected to SQLite database at {self.db_path}")
            
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
        print(f"Connection to database {self.db_path} closed.")
