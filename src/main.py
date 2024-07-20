from fastapi import FastAPI
from config import settings

app = FastAPI()


@app.get("/v1/status")
async def get_status():
    print(settings.DATABASE_URL)
