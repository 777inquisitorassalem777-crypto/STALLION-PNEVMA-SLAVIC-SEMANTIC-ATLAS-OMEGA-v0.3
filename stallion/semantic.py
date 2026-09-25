from __future__ import annotations
import re
from dataclasses import asdict
from .models import SemanticResult, EvidenceStatus

LEXICON = {
    "ведун": {
        "role": "VEDUN",
        "axis": "видеть → распознавать → знать",
        "meaning": "knowledge and recognition",
        "status": EvidenceStatus.FACT,
        "note": "historical/linguistic category; exact historical meanings depend on source and period",
    },
    "волхв": {
        "role": "VOLHV",
        "axis": "слово → символ → смысл",
        "meaning": "ritual/symbolic interpretation",
        "status": EvidenceStatus.INTERPRETATION,
        "note": "historical semantics require source-specific dating",
    },
    "вещун": {
        "role": "VESHCHUN",
        "axis": "знать → возвещать",
        "meaning": "communication / prognostic speech",
        "status": EvidenceStatus.INTERPRETATION,
        "note": "semantic role in this architecture is a model, not a claim of one historical profession",
    },
    "знахарь": {
        "role": "ZNAKHAR",
        "axis": "знать → применять",
        "meaning": "applied healing/folk knowledge",
        "status": EvidenceStatus.INTERPRETATION,
        "note": "historical functions vary by region and period",
    },
    "характерник": {
        "role": "KHARAKTERNIK",
        "axis": "характер → воля → действие",
        "meaning": "bounded agency / warrior-folklore layer",
        "status": EvidenceStatus.FACT,
        "note": "later Ukrainian/Cossack cultural layer; not a reconstructed Proto-Slavic term",
    },
}

CROSS_CIV = {
    "vedun": ["PIE *weyd- / *wid- (hypothesis family)", "Indo-Iranian vid-/veda"],
    "volhv": ["Slavic ritual vocabulary", "comparative Indo-European ritual specialists"],
    "character": ["Ukrainian/Cossack folklore"],
}


class SemanticAtlas:
    def analyze(self, query: str) -> SemanticResult:
        q = query.lower()
        terms = [term for term in LEXICON if term in q]
        roles = [LEXICON[t]["role"] for t in terms]

        if terms:
            fragments = [
                f"{LEXICON[t]['role']}: {LEXICON[t]['axis']} — {LEXICON[t]['meaning']}"
                for t in terms
            ]
            interpretation = "; ".join(fragments)
            statuses = {LEXICON[t]["status"] for t in terms}
            status = EvidenceStatus.FACT if statuses == {EvidenceStatus.FACT} else EvidenceStatus.INTERPRETATION
            confidence = 0.82
        else:
            interpretation = "No lexeme matched. The hypothesis space remains open."
            status = EvidenceStatus.HYPOTHESIS
            confidence = 0.20

        return SemanticResult(
            query=query,
            terms=terms,
            roles=roles,
            interpretation=interpretation,
            evidence_status=status,
            confidence=confidence,
            provenance=["PNEVMA-SLAVIC-SEMANTIC-ATLAS-v0.1"],
        )

    def graph(self):
        edges = []
        for term, item in LEXICON.items():
            edges.append({"source": term, "target": item["role"], "relation": "implements"})
            edges.append({"source": item["role"], "target": item["axis"], "relation": "semantic_axis"})
        return {"nodes": list(LEXICON), "edges": edges}

    def export(self):
        return {k: {**v, "status": v["status"].value} for k, v in LEXICON.items()}
