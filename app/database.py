import os
from dotenv import load_dotenv
from supabase import create_client, Client

# .env 파일의 내용을 불러옵니다.
load_dotenv()

# 환경 변수에서 URL과 Key를 가져옵니다.
URL = os.environ.get("SUPABASE_URL")
KEY = os.environ.get("SUPABASE_KEY")

# 어디서든 이 supabase 객체를 불러와서 DB를 조작할 수 있습니다.
supabase: Client = create_client(URL, KEY)