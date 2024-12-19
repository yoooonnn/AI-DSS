# ai/src/inference.py
import os
import sys

# 프로젝트 루트 경로 설정
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(PROJECT_ROOT)

from utils.sql_assistant import SQLAssistant

def main():
    # MySQL 연결 정보 설정
    db_config = {
        "host": "localhost",  # MySQL 호스트
        "user": "root",       # 사용자 이름
        "password": "",  # 비밀번호
        "database": "iotlogs",  # 데이터베이스 이름
        "port": 3306          # 포트
    }

    try:
        assistant = SQLAssistant(**db_config)
        
        # 인터페이스 시작
        print("\nSQL Translation and Execution Interface")
        print("Enter 'quit' or 'exit' to end the session")
        print("Add '!no-exec' at the end of your query to only see the SQL without executing it")
        print("-" * 50)
        while True:
            # 사용자 입력 처리
            user_input = input("\nEnter your query in natural language: ").strip()
            
            if user_input.lower() in ['quit', 'exit']:
                print("Ending session...")
                break
            
            if not user_input:
                print("Please enter a valid query")
                continue
            
            # 실행 여부 확인
            execute = True
            if user_input.endswith('!no-exec'):
                user_input = user_input[:-8].strip()
                execute = False
            
            # 쿼리 처리
            assistant.process_query(user_input, execute)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        raise
    
    finally:
        if 'assistant' in locals():
            assistant.close()

if __name__ == "__main__":
    main()