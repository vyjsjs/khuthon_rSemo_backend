from fastapi import FastAPI
from app.routers import users, artists, stations, checkins, matches, events

app = FastAPI(title="문화 정류장 API")

app.include_router(users.router)
app.include_router(artists.router)
app.include_router(stations.router)
app.include_router(checkins.router)
app.include_router(matches.router)
app.include_router(events.router)


@app.get("/")
def read_root():
    return {"message": "문화 정류장 백엔드 서버가 정상 작동 중입니다!"}
