from fastapi import FastAPI

from app.database import Base, engine
from app.routers.tasks import router as tasks_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Planner API",
    description="Simple API for Personal Task Planner",
    version="0.2.0"
)


@app.get("/")
def root():
    return {"message": "Planner API is running"}


app.include_router(tasks_router)
