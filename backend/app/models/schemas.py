from pydantic import BaseModel


class PredictionRequest(BaseModel):
    air_temperature: float
    process_temperature: float
    rotational_speed: float
    torque: float
    tool_wear: float


class PredictionResponse(BaseModel):
    prediction: int
    status: str
    failure_probability: float
    threshold: float
    model: str
    risk_level: str
    alert: str | None