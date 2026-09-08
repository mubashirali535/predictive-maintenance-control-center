from fastapi import APIRouter

from backend.app.services.state_service import state_service


router = APIRouter()


@router.get("/machine/status")
def get_machine_status():
    return state_service.get_current_state()