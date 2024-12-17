import pandas as pd
import pymysql

class SQLExecutor:
    """SQL 쿼리를 직접 실행하는 클래스 (MySQL 전용)"""
    
    def __init__(self, host, user, password, database, port=3306):
        """MySQL 데이터베이스 연결 초기화"""
        try:
            self.conn = pymysql.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=port,
                cursorclass=pymysql.cursors.DictCursor
            )
            print(f"Connected to MySQL database '{database}' at {host}:{port}")
        except Exception as e:
            print(f"Error initializing MySQL database: {str(e)}")
            raise
    
    def execute_query(self, query):
        """SQL 쿼리 실행"""
        try:
            df = pd.read_sql_query(query, self.conn)
            return df
        except Exception as e:
            print(f"Error executing query: {str(e)}")
            return None
    
    def close(self):
        """데이터베이스 연결 종료"""
        if self.conn:
            self.conn.close()
            print("MySQL database connection closed.")
