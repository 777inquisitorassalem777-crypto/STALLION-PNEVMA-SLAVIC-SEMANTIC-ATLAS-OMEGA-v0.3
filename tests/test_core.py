import time
from stallion.models import SensorFrame, MissionRequest, MissionType
from stallion.runtime import StallionRuntime
from stallion.constitution import ImmutableConstitution
from stallion.quantum_inspired import QuantumInspiredReasoner


def test_constitution():
    c = ImmutableConstitution()
    assert c.verify().valid
    ok, _ = c.gate({"simulation": True, "harmful_autonomous_action": False})
    assert ok


def test_harmful_gate():
    c = ImmutableConstitution()
    ok, _ = c.gate({"simulation": True, "harmful_autonomous_action": True})
    assert not ok


def test_hypotheses_normalize():
    h = QuantumInspiredReasoner().infer(.8, .9)
    assert abs((h.rescue + h.inspection + h.transport) - 1.0) < 1e-9


def test_runtime():
    rt = StallionRuntime()
    result = rt.cycle(
        SensorFrame(time.time(), objects=["person_in_need"], battery_level=.8),
        MissionRequest(MissionType.RESCUE, "safe simulation", simulated=True),
        "ведун и волхв",
    )
    assert result["constitution"]["valid"]
    assert result["mission"]["status"] == "approved"
    assert rt.ledger.verify()
