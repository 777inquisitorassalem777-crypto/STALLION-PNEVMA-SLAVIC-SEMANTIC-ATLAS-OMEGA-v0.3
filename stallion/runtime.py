from __future__ import annotations
from dataclasses import asdict
from time import time
from .models import SensorFrame, MissionRequest
from .semantic import SemanticAtlas
from .constitution import ImmutableConstitution
from .dharma import DharmaSpirit, DharmaFlesh, TantraPath
from .quantum_inspired import QuantumInspiredReasoner
from .planner import MissionPlanner
from .provenance import ProvenanceLedger


class StallionRuntime:
    def __init__(self):
        self.atlas = SemanticAtlas()
        self.constitution = ImmutableConstitution()
        self.spirit = DharmaSpirit()
        self.flesh = DharmaFlesh()
        self.tantra = TantraPath()
        self.reasoner = QuantumInspiredReasoner()
        self.planner = MissionPlanner(constitution=self.constitution)
        self.ledger = ProvenanceLedger()

    def cycle(self, sensor: SensorFrame, mission: MissionRequest, query: str):
        semantic = self.atlas.analyze(query)

        uncertainty = 1.0 - semantic.confidence
        spirit = self.spirit.evaluate(uncertainty, semantic.confidence)
        flesh = self.flesh.evaluate(
            sensor.battery_level,
            sensor.localization_confidence,
            sensor.imu_stable,
        )
        integration = self.tantra.integrate(spirit, flesh)

        emergency_signal = min(
            1.0,
            0.5 * len(sensor.thermal_alerts) +
            0.5 * (1.0 if "person_in_need" in sensor.objects else 0.0)
        )
        hypotheses = self.reasoner.infer(semantic.confidence, emergency_signal)

        plan = self.planner.plan(mission)
        if not sensor.imu_stable or sensor.battery_level < 0.10:
            plan.status = type(plan.status).BLOCKED
            plan.reason = "physical readiness gate blocked execution"

        result = {
            "timestamp": time(),
            "semantic": asdict(semantic),
            "dharma": asdict(integration),
            "hypotheses": asdict(hypotheses),
            "mission": plan.to_dict(),
            "constitution": asdict(self.constitution.verify()),
            "sensor": asdict(sensor),
        }

        self.ledger.append(
            "runtime_cycle",
            result,
            "stallion-pnevma-runtime",
            evidence_status="interpretation",
        )
        return result

    def status(self):
        return {
            "version": "1.1.0",
            "constitution_valid": self.constitution.verify().valid,
            "provenance_records": len(self.ledger.records),
            "provenance_valid": self.ledger.verify(),
            "semantic_terms": list(self.atlas.export()),
            "execution_profile": "simulation-first",
        }
