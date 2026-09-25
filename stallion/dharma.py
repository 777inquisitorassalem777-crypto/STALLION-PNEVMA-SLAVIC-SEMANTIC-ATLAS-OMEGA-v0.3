from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class DharmaState:
    spirit_alignment: float
    flesh_stability: float
    integration: float


class DharmaSpirit:
    """Symbolic model of reflection, values and epistemic restraint."""

    def evaluate(self, uncertainty: float, coherence: float) -> float:
        return max(0.0, min(1.0, 0.6 * coherence + 0.4 * (1.0 - uncertainty)))


class DharmaFlesh:
    """Engineering model: physical stability, energy and actuator readiness."""

    def evaluate(self, battery: float, localization: float, imu_stable: bool) -> float:
        stability = 1.0 if imu_stable else 0.0
        return max(0.0, min(1.0, 0.45 * battery + 0.35 * localization + 0.20 * stability))


class TantraPath:
    """
    Symbolic synthesis layer.

    'Tantra' is represented here as integration of informational and physical
    state; it is not implemented as a supernatural mechanism.
    """

    def integrate(self, spirit: float, flesh: float) -> DharmaState:
        integration = (spirit * flesh) ** 0.5
        return DharmaState(spirit, flesh, integration)
