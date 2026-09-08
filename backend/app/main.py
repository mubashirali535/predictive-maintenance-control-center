from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.predict import router as predict_router
from backend.app.api.machine import router as machine_router
from backend.app.api.history import router as history_router
from backend.app.api.simulation import router as simulation_router
from backend.app.api.websocket import router as websocket_router


app = FastAPI(
    title="Predictive Maintenance Control Center",
    description="AI-powered predictive maintenance monitoring system",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(predict_router)
app.include_router(machine_router)
app.include_router(history_router)
app.include_router(simulation_router)
app.include_router(websocket_router)

@app.get("/")
def root():
    return {
        "message": "Predictive Maintenance Control Center API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }