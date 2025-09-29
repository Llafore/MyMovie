from fastapi import FastAPI
from backend.routes import user_api, media_api

import uvicorn

app = FastAPI()

app.include_router(user_api.router)
app.include_router(media_api.router)

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)