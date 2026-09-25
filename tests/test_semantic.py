from stallion.semantic import SemanticAtlas


def test_semantic_roles():
    r = SemanticAtlas().analyze("ведун волхв характерник")
    assert r.terms == ["ведун", "волхв", "характерник"]
    assert "VEDUN" in r.roles
    assert "KHARAKTERNIK" in r.roles


def test_unknown_is_hypothesis():
    r = SemanticAtlas().analyze("неизвестная лексема")
    assert r.evidence_status.value == "hypothesis"
