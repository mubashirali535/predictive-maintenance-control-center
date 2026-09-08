from fastapi import APIRouter

from backend.app.services.state_service import state_service


router = APIRouter()


@router.get("/history")
def get_history():
    return state_service.get_history()