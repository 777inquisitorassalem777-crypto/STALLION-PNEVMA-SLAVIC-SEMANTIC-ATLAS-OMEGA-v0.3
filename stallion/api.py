from __future__ import annotations
from time import time
from fastapi import FastAPI
from pydantic import BaseModel, Field
from .models import SensorFrame, MissionRequest, MissionType
from .runtime import StallionRuntime

app = FastAPI(title="STALLION–PNEVMA Ω", version="1.1.0")
runtime = StallionRuntime()


class CycleInput(BaseModel):
    query: str = "ведун и волхв"
    mission: MissionType = MissionType.INSPECTION
    objective: str = "inspect a simulated environment"
    simulated: bool = True
    human_authorized: bool = False
    objects: list[str] = []
    thermal_alerts: list[str] = []
    localization_confidence: float = Field(1.0, ge=0, le=1)
    imu_stable: bool = True
    battery_level: float = Field(1.0, ge=0, le=1)


@app.get("/health")
def health():
    return {"status": "ok", "version": "1.1.0"}


@app.get("/status")
def status():
    return runtime.status()


@app.get("/architecture")
def architecture():
    return {
        "layers": [
            "sensor/perception",
            "PNEVMA semantic layer",
            "Slavic semantic atlas",
            "hypothesis reasoning",
            "Dharma symbolic integration",
            "immutable constitution",
            "mission planner",
            "simulation executor",
            "provenance/telemetry",
        ]
    }


@app.get("/semantic/atlas")
def semantic_atlas():
    return runtime.atlas.export()


@app.get("/semantic/graph")
def semantic_graph():
    return runtime.atlas.graph()


@app.post("/simulate/cycle")
def simulate_cycle(req: CycleInput):
    sensor = SensorFrame(
        timestamp=time(),
        objects=req.objects,
        thermal_alerts=req.thermal_alerts,
        localization_confidence=req.localization_confidence,
        imu_stable=req.imu_stable,
        battery_level=req.battery_level,
    )
    mission = MissionRequest(
        req.mission,
        req.objective,
        req.human_authorized,
        req.simulated,
    )
    return runtime.cycle(sensor, mission, req.query)
