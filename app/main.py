from fastapi import FastAPI
from app.database import supabase # 방금 만든 DB 연결 객체 불러오기

app = FastAPI(title="문화 정류장 API")

# 1. 서버가 잘 켜졌는지 확인하는 기본 창구
@app.get("/")
def read_root():
    return {"message": "문화 정류장 백엔드 서버가 정상 작동 중입니다!"}

# 2. Supabase DB 연결이 잘 되었는지 확인하는 테스트 창구
@app.get("/test-db")
def test_db_connection():
    try:
        # supabase에 아무 요청이나 보내서 에러가 안 나는지 확인 (예: stops 테이블 조회)
        # 당장 stops 테이블이 없어도 연결 자체는 확인 가능합니다.
        response = supabase.table("stops").select("*").limit(1).execute()
        return {"status": "success", "message": "Supabase 연결 성공!"}
    except Exception as e:
        return {"status": "error", "message": f"DB 연결 실패: {str(e)}"}