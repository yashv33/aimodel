from fastapi import FastAPI
from app.routes.report import router as report_router

app = FastAPI(title="AI Lab Report Generator")

app.include_router(report_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the AI Lab Report Generator!"}
