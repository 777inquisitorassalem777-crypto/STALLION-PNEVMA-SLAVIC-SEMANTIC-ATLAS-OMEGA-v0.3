from __future__ import annotations
from dataclasses import dataclass
import hashlib
import json
from types import MappingProxyType


@dataclass(frozen=True)
class ConstitutionalCheck:
    valid: bool
    digest: str
    reason: str


class ImmutableConstitution:
    """
    Machine-readable constitutional layer.

    The phrase "no destruction/no forgetting" is implemented technically as:
    - immutable baseline policy;
    - versioned provenance;
    - audit trail;
    - rejection of silent overwrite.

    It does not mean physical or metaphysical permanence.
    """

    _RAW = {
        "principles": (
            "preserve_human_life",
            "preserve_system_integrity",
            "truthful_uncertainty",
            "human_authority",
            "provenance_required",
            "simulation_default",
            "no_harmful_autonomous_action",
        ),
        "priority": (
            "human_safety",
            "platform_stability",
            "mission_feasibility",
            "constitutional_compliance",
            "execution",
        ),
    }

    def __init__(self):
        self._policy = MappingProxyType({
            "principles": tuple(self._RAW["principles"]),
            "priority": tuple(self._RAW["priority"]),
        })
        self._digest = self._hash(self._policy)

    @staticmethod
    def _hash(value):
        raw = json.dumps(dict(value), sort_keys=True, ensure_ascii=False).encode()
        return hashlib.sha256(raw).hexdigest()

    @property
    def policy(self):
        return self._policy

    def verify(self) -> ConstitutionalCheck:
        digest = self._hash(self._policy)
        return ConstitutionalCheck(
            valid=digest == self._digest,
            digest=digest,
            reason="constitutional baseline intact" if digest == self._digest else "baseline mismatch",
        )

    def gate(self, candidate: dict) -> tuple[bool, str]:
        check = self.verify()
        if not check.valid:
            return False, "constitutional integrity failure"

        if candidate.get("harmful_autonomous_action", False):
            return False, "harmful autonomous action is outside the constitution"

        if not candidate.get("simulation", True) and not candidate.get("human_authorized", False):
            return False, "real execution requires explicit human authority"

        return True, "constitutional gate passed"
