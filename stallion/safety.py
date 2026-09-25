from __future__ import annotations
from dataclasses import dataclass
from .models import MissionRequest, MissionType


@dataclass(frozen=True)
class SafetyDecision:
    allowed: bool
    reason: str
    risk: float


class SafetyPolicy:
    ALLOWED = {
        MissionType.INSPECTION,
        MissionType.SEARCH,
        MissionType.RESCUE,
        MissionType.TRANSPORT,
        MissionType.MEDICAL_SUPPORT,
        MissionType.ENGINEERING_INSPECTION,
    }

    def check(self, request: MissionRequest) -> SafetyDecision:
        if request.mission not in self.ALLOWED:
            return SafetyDecision(False, "mission not in safe research profile", 1.0)

        if not request.objective.strip():
            return SafetyDecision(False, "empty objective", 0.5)

        if not request.simulated and not request.human_authorized:
            return SafetyDecision(False, "human authorization required for non-simulation execution", 0.9)

        return SafetyDecision(True, "mission accepted", 0.15 if request.mission != MissionType.RESCUE else 0.30)
