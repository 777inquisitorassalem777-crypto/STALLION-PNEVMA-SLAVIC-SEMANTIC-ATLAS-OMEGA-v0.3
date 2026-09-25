from __future__ import annotations
from dataclasses import dataclass
import math


@dataclass(frozen=True)
class HypothesisState:
    rescue: float
    inspection: float
    transport: float

    def normalized(self):
        total = self.rescue + self.inspection + self.transport
        if total <= 0:
            return HypothesisState(1/3, 1/3, 1/3)
        return HypothesisState(
            self.rescue / total,
            self.inspection / total,
            self.transport / total,
        )


class QuantumInspiredReasoner:
    """
    Classical probabilistic analogue.

    It uses normalized hypothesis weights before evidence selection.
    It does NOT simulate quantum mechanics and does not claim physical
    quantum effects in cognition.
    """

    def infer(self, semantic_confidence: float, emergency_signal: float) -> HypothesisState:
        rescue = 0.25 + 0.65 * emergency_signal
        inspection = 0.45 + 0.25 * semantic_confidence
        transport = 0.30
        return HypothesisState(rescue, inspection, transport).normalized()
