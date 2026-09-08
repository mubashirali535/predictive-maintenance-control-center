
from fastapi import APIRouter

from backend.app.services.simulation_service import simulation_service
from backend.app.services.state_service import state_service


router = APIRouter()


@router.post("/simulation/start")
async def start_simulation():
    started = await simulation_service.start()

    return {
        "started": started,
        "running": simulation_service.is_running()
    }


@router.post("/simulation/stop")
async def stop_simulation():
    stopped = await simulation_service.stop()

    return {
        "stopped": stopped,
        "running": simulation_service.is_running()
    }

@router.post("/simulation/reset")
async def reset_simulation():
    await simulation_service.reset()
    state_service.reset()

    return {
        "message": "Simulation state reset successfully",
        "running": simulation_service.is_running()
    }


