from __future__ import annotations
from dataclasses import dataclass, asdict
from time import time
import hashlib, json


@dataclass(frozen=True)
class ProvenanceRecord:
    event_id: str
    kind: str
    payload_hash: str
    source: str
    evidence_status: str
    timestamp: float


class ProvenanceLedger:
    def __init__(self):
        self.records = []

    def append(self, kind, payload, source, evidence_status="fact"):
        raw = json.dumps(payload, sort_keys=True, ensure_ascii=False, default=str).encode()
        digest = hashlib.sha256(raw).hexdigest()
        event_id = hashlib.sha256(f"{digest}:{len(self.records)}".encode()).hexdigest()[:20]
        rec = ProvenanceRecord(event_id, kind, digest, source, evidence_status, time())
        self.records.append(rec)
        return rec

    def verify(self):
        return all(len(r.payload_hash) == 64 for r in self.records)

    def export(self):
        return [asdict(x) for x in self.records]
