from __future__ import annotations
from dataclasses import dataclass, field, asdict
from enum import Enum
from time import time
from typing import Any


class MissionType(str, Enum):
    INSPECTION = "inspection"
    SEARCH = "search"
    RESCUE = "rescue"
    TRANSPORT = "transport"
    MEDICAL_SUPPORT = "medical_support"
    ENGINEERING_INSPECTION = "engineering_inspection"


class DecisionStatus(str, Enum):
    PROPOSED = "proposed"
    APPROVED = "approved"
    BLOCKED = "blocked"


class EvidenceStatus(str, Enum):
    FACT = "fact"
    HYPOTHESIS = "hypothesis"
    INTERPRETATION = "interpretation"
    DISPUTED = "disputed"


@dataclass
class SensorFrame:
    timestamp: float
    objects: list[str] = field(default_factory=list)
    thermal_alerts: list[str] = field(default_factory=list)
    localization_confidence: float = 1.0
    imu_stable: bool = True
    battery_level: float = 1.0


@dataclass
class SemanticResult:
    query: str
    terms: list[str]
    roles: list[str]
    interpretation: str
    evidence_status: EvidenceStatus
    confidence: float
    provenance: list[str]


@dataclass
class MissionRequest:
    mission: MissionType
    objective: str
    human_authorized: bool = False
    simulated: bool = True
    constraints: dict[str, Any] = field(default_factory=dict)


@dataclass
class MissionPlan:
    mission: MissionType
    steps: list[str]
    risk: float
    status: DecisionStatus
    reason: str
    created_at: float = field(default_factory=time)

    def to_dict(self):
        d = asdict(self)
        d["mission"] = self.mission.value
        d["status"] = self.status.value
        return d


@dataclass
class Hypothesis:
    name: str
    probability: float
    evidence: list[str]
    state: str = "unmeasured"


@dataclass
class TelemetryEvent:
    topic: str
    payload: dict[str, Any]
    timestamp: float = field(default_factory=time)
