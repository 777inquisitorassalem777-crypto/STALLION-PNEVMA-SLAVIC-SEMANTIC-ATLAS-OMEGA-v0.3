from __future__ import annotations
from .models import MissionRequest, MissionPlan, DecisionStatus
from .safety import SafetyPolicy
from .constitution import ImmutableConstitution


class MissionPlanner:
    def __init__(self, safety=None, constitution=None):
        self.safety = safety or SafetyPolicy()
        self.constitution = constitution or ImmutableConstitution()

    def plan(self, request: MissionRequest) -> MissionPlan:
        gate = self.safety.check(request)

        constitutional_ok, constitutional_reason = self.constitution.gate({
            "simulation": request.simulated,
            "human_authorized": request.human_authorized,
            "harmful_autonomous_action": False,
        })

        if not gate.allowed or not constitutional_ok:
            return MissionPlan(
                request.mission, [], max(gate.risk, 0.9),
                DecisionStatus.BLOCKED,
                gate.reason if not gate.allowed else constitutional_reason,
            )

        steps = [
            "validate sensor and integrity state",
            "construct semantic context",
            "evaluate uncertainty and competing hypotheses",
            "select bounded mission plan",
            "execute simulation step",
            "verify result",
            "append telemetry and provenance",
        ]
        return MissionPlan(
            request.mission, steps, gate.risk,
            DecisionStatus.APPROVED,
            f"{gate.reason}; {constitutional_reason}",
        )
