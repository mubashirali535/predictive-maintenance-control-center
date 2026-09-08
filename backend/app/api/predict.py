from fastapi import APIRouter

from backend.app.models.schemas import PredictionRequest, PredictionResponse
from backend.app.services.prediction_service import predict_failure


router = APIRouter()


@router.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    return predict_failure(
        air_temperature=request.air_temperature,
        process_temperature=request.process_temperature,
        rotational_speed=request.rotational_speed,
        torque=request.torque,
        tool_wear=request.tool_wear,
    )