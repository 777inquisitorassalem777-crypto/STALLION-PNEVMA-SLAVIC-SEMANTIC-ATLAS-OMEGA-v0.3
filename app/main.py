from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from slavic_cognitive_agent import SlavicCognitiveAgent, ATLAS, graph

app = FastAPI(
    title="PNEVMA–SLAVIC SEMANTIC ATLAS Ω",
    version="0.3.0",
    description="Семантическая и когнитивная модель Ведун → Волхв → Вещун → Характерник."
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=False,
    allow_methods=["*"], allow_headers=["*"]
)
agent = SlavicCognitiveAgent()

class AnalyzeRequest(BaseModel):
    observation: str
    goal: str | None = None

@app.get("/health")
def health():
    return {"status": "ok", "version": "0.3.0"}

@app.get("/atlas")
def atlas():
    return ATLAS

@app.get("/graph")
def get_graph():
    return graph()

@app.get("/status")
def status():
    return agent.status()

@app.post("/analyze")
def analyze(payload: AnalyzeRequest):
    return agent.perceive_and_act(payload.observation, payload.goal or payload.observation)

@app.post("/learn")
def learn(payload: dict):
    from slavic_cognitive_agent import KnowledgeType
    typ = KnowledgeType(payload.get("type", KnowledgeType.СВЯЗИ.value))
    unit = agent.learn_new(
        payload["content"], typ,
        tags=payload.get("tags", []),
        confidence=float(payload.get("confidence", 1.0))
    )
    return unit.to_dict()
