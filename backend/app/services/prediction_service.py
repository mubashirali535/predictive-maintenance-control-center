import joblib
import pandas as pd
from pathlib import Path

from backend.app.services.risk_service import evaluate_risk
from backend.app.services.state_service import state_service


MODEL_PATH = (
    Path(__file__).resolve().parent.parent
    / "ml"
    / "model"
    / "random_forest.pkl"
)

METADATA_PATH = (
    Path(__file__).resolve().parent.parent
    / "ml"
    / "model"
    / "model_metadata.pkl"
)


model = joblib.load(MODEL_PATH)
metadata = joblib.load(METADATA_PATH)


def predict_failure(
    air_temperature,
    process_temperature,
    rotational_speed,
    torque,
    tool_wear,
):
    data = pd.DataFrame([{
        "Air temperature [K]": air_temperature,
        "Process temperature [K]": process_temperature,
        "Rotational speed [rpm]": rotational_speed,
        "Torque [Nm]": torque,
        "Tool wear [min]": tool_wear,
    }])

    probability = model.predict_proba(data)[0][1]

    threshold = metadata["classification_threshold"]

    prediction = int(probability >= threshold)

    status = "Failure Risk" if prediction == 1 else "Normal"

    risk = evaluate_risk(probability)

    state = {
        "prediction": prediction,
        "status": status,
        "failure_probability": probability,
        "threshold": threshold,
        "model": metadata["model_name"],
        "risk_level": risk["risk_level"],
        "alert": risk["alert"],
    }

    state_service.update(state)

    return state