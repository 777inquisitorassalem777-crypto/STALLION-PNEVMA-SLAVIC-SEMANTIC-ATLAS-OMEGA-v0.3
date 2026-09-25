from stallion.models import MissionRequest, MissionType
from stallion.planner import MissionPlanner


def test_non_simulated_requires_authority():
    plan = MissionPlanner().plan(
        MissionRequest(MissionType.INSPECTION, "inspect", simulated=False, human_authorized=False)
    )
    assert plan.status.value == "blocked"


def test_simulated_allowed():
    plan = MissionPlanner().plan(
        MissionRequest(MissionType.INSPECTION, "inspect", simulated=True)
    )
    assert plan.status.value == "approved"
