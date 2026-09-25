from slavic_cognitive_agent import (
    SlavicCognitiveAgent, KnowledgeType, graph, ATLAS
)

def test_agent_initializes():
    a = SlavicCognitiveAgent()
    assert a.status()["knowledge"]["total_knowledge"] >= 6

def test_learning_and_retrieval():
    a = SlavicCognitiveAgent()
    a.learn_new("Огонь связан с очищением", KnowledgeType.ПРИРОДА, ["огонь"])
    assert a.vedun.know("огонь")

def test_cycle():
    a = SlavicCognitiveAgent()
    result = a.perceive_and_act("огонь горит", "понять огонь")
    assert "interpretation" in result
    assert "action" in result

def test_atlas():
    assert "ведун" in ATLAS
    assert ATLAS["характерник"]["layer"].startswith("поздний")

def test_graph():
    g = graph()
    assert len(g["nodes"]) == 5
    assert any(x["source"] == "VEDUN" and x["target"] == "VOLHV" for x in g["edges"])
