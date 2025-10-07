from fastapi import FastAPI
from api.routes import user_api, media_api

app = FastAPI()

app.include_router(user_api.router)
app.include_router(media_api.router)

@app.get("/health-check")
async def health_check():
    return {"status": "ok"}

if __name__ == '__main__':
    import uvicorn
    import os
    from dotenv import load_dotenv

    load_dotenv()

    port = int(os.getenv("PORT", 8000))
    # Set "reload" to "True" if "uvloop" is installed
    # "uvloop" only works on Linux or Mac...
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)