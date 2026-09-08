import asyncio
import pandas as pd

from backend.app.services.prediction_service import predict_failure
from backend.app.services.websocket_manager import websocket_manager


DATASET_PATH = "backend/data/ai4i2020.csv"


class SimulationService:
    def __init__(self):
        self.simulation_task = None
        self.stop_event = asyncio.Event()
        self.current_row = 0
        self.data = pd.read_csv(DATASET_PATH)
    async def reset(self):
        if self.is_running():
            await self.stop()

        self.current_row = 0


    def is_running(self):
        return (
            self.simulation_task is not None
            and not self.simulation_task.done()
        )

    async def start(self):
        if self.is_running():
            return False

        self.stop_event.clear()

        self.simulation_task = asyncio.create_task(
            self._run_simulation()
        )

        return True

    async def stop(self):
        if not self.is_running():
            return False

        self.stop_event.set()

        await self.simulation_task

        self.simulation_task = None

        return True

    async def _run_simulation(self):
        try:
            while (
                not self.stop_event.is_set()
                and self.current_row < len(self.data)
            ):
                row = self.data.iloc[self.current_row]

                prediction = predict_failure(
                    air_temperature=row["Air temperature [K]"],
                    process_temperature=row["Process temperature [K]"],
                    rotational_speed=row["Rotational speed [rpm]"],
                    torque=row["Torque [Nm]"],
                    tool_wear=row["Tool wear [min]"],
                )

                machine_event = {
                    "row": self.current_row,
                    "sensor_data": {
                        "air_temperature": float(row["Air temperature [K]"]),
                        "process_temperature": float(row["Process temperature [K]"]),
                        "rotational_speed": float(row["Rotational speed [rpm]"]),
                        "torque": float(row["Torque [Nm]"]),
                        "tool_wear": float(row["Tool wear [min]"]),
                    },
                    "prediction": prediction,
                }

                print("BROADCASTING:", machine_event)

                await websocket_manager.broadcast(machine_event)

                print(
                    f"Row {self.current_row}: "
                    f"Prediction={prediction['prediction']}, "
                    f"Risk={prediction['risk_level']}, "
                    f"Probability={prediction['failure_probability']:.2f}"
                )

                self.current_row += 1

                await asyncio.sleep(1)

            if self.current_row >= len(self.data):
                print("Simulation completed: dataset finished.")

        except Exception as error:
            print(f"Simulation error: {error}")

        finally:
            self.simulation_task = None
simulation_service = SimulationService()