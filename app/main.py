from fastapi import FastAPI

from app.api.routes.analyze import router as analyze_router

app = FastAPI(title="AgentResume API", version="0.1.0")

app.include_router(analyze_router)


@app.get("/")
def root():
    return {"message": "AgentResume API is running"}