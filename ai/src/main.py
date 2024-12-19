# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any, Union
import uvicorn
import os
import sys
from datetime import datetime
import pandas as pd
import json

# 프로젝트 루트 경로 설정
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(PROJECT_ROOT)

from utils.sql_assistant import SQLAssistant

app = FastAPI(
    title="AI SQL Query API",
    description="Natural language to SQL query conversion and execution API",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB 설정
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "iotlogs",
    "port": 3306
}

# 요청 모델
class QueryRequest(BaseModel):
    query: str
    execute: bool = True

# 응답 모델
class QueryResponse(BaseModel):
    sql: Optional[str] = None
    results: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: str = datetime.now().isoformat()

# SQLAssistant 인스턴스 저장
sql_assistant: Optional[SQLAssistant] = None

def get_sql_assistant() -> SQLAssistant:
    """SQLAssistant 인스턴스를 가져오거나 생성"""
    global sql_assistant
    if sql_assistant is None:
        print("Initializing SQL Assistant...")
        sql_assistant = SQLAssistant(**DB_CONFIG)
    return sql_assistant

def convert_dataframe_to_dict(df: pd.DataFrame) -> Dict[str, Any]:
    """DataFrame을 JSON 직렬화 가능한 딕셔너리로 변환"""
    if df is None:
        return None
        
    return {
        "columns": list(df.columns),
        "data": json.loads(df.to_json(orient="records", date_format="iso")),
        "total_rows": len(df),
        "preview": df.head().to_dict(orient="records")
    }

@app.post("/api/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """자연어 쿼리를 처리하고 SQL을 실행"""
    try:
        assistant = get_sql_assistant()
        
        # 쿼리 처리 및 실행
        sql, results = assistant.process_query(request.query, request.execute)
        
        if sql is None:
            raise HTTPException(
                status_code=500,
                detail="Failed to process query"
            )
        
        # DataFrame 결과를 딕셔너리로 변환
        formatted_results = None
        if isinstance(results, pd.DataFrame):
            formatted_results = convert_dataframe_to_dict(results)
            
        return QueryResponse(
            sql=sql,
            results=formatted_results
        )
    
    except Exception as e:
        return QueryResponse(
            error=str(e)
        )

@app.get("/api/health")
async def health_check():
    """API 상태 확인"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.on_event("startup")
async def startup_event():
    """애플리케이션 시작 시 실행"""
    try:
        get_sql_assistant()
    except Exception as e:
        print(f"Failed to initialize SQL Assistant: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """애플리케이션 종료 시 실행"""
    global sql_assistant
    if sql_assistant:
        sql_assistant.close()
        sql_assistant = None

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )