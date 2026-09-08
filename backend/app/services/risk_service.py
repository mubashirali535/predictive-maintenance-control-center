WARNING_THRESHOLD = 0.30
CRITICAL_THRESHOLD = 0.70


def evaluate_risk(failure_probability: float) -> dict:
    if failure_probability >= CRITICAL_THRESHOLD:
        risk_level = "CRITICAL"
        alert = "Critical machine failure risk detected"

    elif failure_probability >= WARNING_THRESHOLD:
        risk_level = "WARNING"
        alert = "Machine failure risk requires attention"

    else:
        risk_level = "NORMAL"
        alert = None

    return {
        "risk_level": risk_level,
        "alert": alert
    }