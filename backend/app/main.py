from fastapi import FastAPI

app = FastAPI(
    title="Predictive Maintenance Control Center",
    description="AI-powered predictive maintenance monitoring system",
    version="0.1.0",
)


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