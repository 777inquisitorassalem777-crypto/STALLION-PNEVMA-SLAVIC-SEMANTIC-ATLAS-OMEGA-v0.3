#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Any, Optional

class KnowledgeType(str, Enum):
    ПРИРОДА = "природа"
    ЧЕЛОВЕК = "человек"
    РОД = "род"
    ВРЕМЯ = "время"
    БОЛЕЗНЬ = "болезнь"
    НЕБЕСНЫЕ_ЯВЛЕНИЯ = "небесные_явления"
    СКРЫТОЕ = "скрытое"
    СВЯЗИ = "скрытые_связи"
    СЛОВО = "слово"
    СИЛА = "сила"
    ДУХ = "дух"

class ActionOutcome(str, Enum):
    УСПЕХ = "успех"
    ЧАСТИЧНЫЙ_УСПЕХ = "частичный_успех"
    НЕУДАЧА = "неудача"

@dataclass
class KnowledgeUnit:
    content: str
    type: KnowledgeType
    confidence: float = 1.0
    source: str = "internal"
    timestamp: datetime = field(default_factory=datetime.now)
    tags: list[str] = field(default_factory=list)
    connections: list[str] = field(default_factory=list)

    def to_dict(self):
        x = asdict(self)
        x["type"] = self.type.value
        x["timestamp"] = self.timestamp.isoformat()
        return x

@dataclass
class SymbolicConnection:
    symbol: str
    meaning: str
    context: str
    strength: float = 1.0

@dataclass
class Intention:
    goal: str
    priority: float = 0.5
    context: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class Action:
    name: str
    description: str
    outcome: ActionOutcome
    result: Any = None
    feedback: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)

ATLAS = {
    "ведун": {
        "role": "VEDUN", "axis": "ВИДЕТЬ → РАСПОЗНАТЬ → ЗНАТЬ",
        "layer": "ранний славянский / древнерусский",
        "evidence": "историко-лингвистическая модель",
        "note": "Этимологически связан с ведать/знать; точные функции зависят от источника."
    },
    "волхв": {
        "role": "VOLHV", "axis": "СЛОВО → СМЫСЛ → РИТУАЛ",
        "layer": "древнерусский / старославянский",
        "evidence": "спорная этимология + исторические свидетельства",
        "note": "Термин связан с сакральной речью, прорицанием и дохристианскими практиками."
    },
    "вещун": {
        "role": "VESHCHUN", "axis": "ЗНАТЬ → ВОЗВЕЩАТЬ",
        "layer": "славянская лексика",
        "evidence": "семантическая модель",
        "note": "Роль сообщения/возвещения знания и предсказания."
    },
    "знахарь": {
        "role": "ZNAKHAR", "axis": "ЗНАТЬ → УМЕТЬ ПРИМЕНЯТЬ",
        "layer": "народная традиция",
        "evidence": "семантическая модель",
        "note": "Практическое знание, прежде всего лечение и помощь."
    },
    "характерник": {
        "role": "KHARAKTERNIK", "axis": "ХАРАКТЕР → ВОЛЯ → ДЕЙСТВИЕ",
        "layer": "поздний украинский / казацкий",
        "evidence": "поздняя фольклорная традиция",
        "note": "Не праславянский термин; переносить его напрямую в праславянскую эпоху нельзя."
    },
}

class Vedun:
    """Knowledge / Memory: ВИДЕТЬ → РАСПОЗНАТЬ → ЗНАТЬ."""

    def __init__(self):
        self.memory: list[KnowledgeUnit] = []

    def learn(self, content, ktype, confidence=1.0, tags=None, source="internal"):
        unit = KnowledgeUnit(
            content=content, type=ktype, confidence=max(0.0, min(1.0, confidence)),
            tags=tags or [], source=source
        )
        self.memory.append(unit)
        return unit

    def know(self, query, limit=10):
        q = query.lower()
        qwords = set(re.findall(r"\w+", q))
        ranked = []
        for unit in self.memory:
            text = unit.content.lower()
            words = set(re.findall(r"\w+", text))
            score = (1.0 if q in text else 0.0)
            score += 0.3 * len(qwords & words)
            score += 0.5 * sum(1 for t in unit.tags if any(w in t.lower() for w in qwords))
            score *= unit.confidence
            if score > 0:
                ranked.append((score, unit))
        ranked.sort(key=lambda x: x[0], reverse=True)
        return [u for _, u in ranked[:limit]]

    def recognize(self, observation):
        return self.know(observation)

    def stats(self):
        by_type = {}
        for x in self.memory:
            by_type[x.type.value] = by_type.get(x.type.value, 0) + 1
        return {"total_knowledge": len(self.memory), "by_type": by_type}

class Volkhv:
    """Interpretation / Symbolism: СЛОВО → СМЫСЛ → РИТУАЛ."""

    def __init__(self, vedun):
        self.vedun = vedun
        self.symbols = {
            "огонь": "очищение и трансформация",
            "вода": "поток жизни и память",
            "земля": "род и устойчивость",
            "воздух": "слово и дыхание",
            "слово": "язык как инструмент символического действия",
            "память": "связь опыта во времени",
        }

    def interpret(self, knowledge):
        connections = []
        for unit in knowledge:
            for symbol, meaning in self.symbols.items():
                if symbol in unit.content.lower():
                    connections.append(asdict(SymbolicConnection(
                        symbol, meaning, unit.content, min(1.0, unit.confidence)
                    )))
        ritual_hint = None
        types = {x.type for x in knowledge}
        if KnowledgeType.БОЛЕЗНЬ in types:
            ritual_hint = "символическая практика исцеления; в программной модели — не медицинское предписание"
        elif KnowledgeType.СЛОВО in types or KnowledgeType.СКРЫТОЕ in types:
            ritual_hint = "анализ ритуальной речи / заговора как культурного феномена"
        elif KnowledgeType.ВРЕМЯ in types:
            ritual_hint = "интерпретация циклов и знаков"
        return {
            "meaning": " | ".join(x.content for x in knowledge) if knowledge else "нет найденного знания",
            "connections": connections,
            "ritual_hint": ritual_hint,
            "timestamp": datetime.now().isoformat(),
        }

class Veshchun:
    """Communication / Proclamation: ЗНАНИЕ → ПЕРЕДАЧА → ПРЕДСКАЗАНИЕ."""

    def __init__(self, volkhv):
        self.volkhv = volkhv
        self.history = []

    def proclaim(self, interpretation, style="ясный"):
        text = interpretation["meaning"]
        if style == "ритуальный":
            text = f"✶ Возвещаю: {text}"
        elif style == "аналитический":
            text = f"Аналитическое сообщение: {text}"
        record = {
            "text": text, "style": style,
            "interpretation": interpretation,
            "timestamp": datetime.now().isoformat()
        }
        self.history.append(record)
        return text

class Kharakternik:
    """Agency / Will / Action: ХАРАКТЕР → ВОЛЯ → ДЕЙСТВИЕ."""

    def __init__(self, veshchun):
        self.veshchun = veshchun
        self.intentions = []
        self.actions_history = []
        self.character_traits = {
            "сила_воли": 0.8,
            "способность_к_действию": 0.9,
            "рефлексия": 0.7,
        }

    def set_intention(self, goal, priority=0.7, context=None):
        x = Intention(goal, max(0, min(1, priority)), context or {})
        self.intentions.append(x)
        return x

    def act(self, intention):
        knowledge = self.veshchun.volkhv.vedun.know(intention.goal)
        interpretation = self.veshchun.volkhv.interpret(knowledge)
        proclamation = self.veshchun.proclaim(interpretation, "аналитический")
        score = intention.priority * self.character_traits["способность_к_действию"]
        outcome = ActionOutcome.УСПЕХ if score >= 0.4 else ActionOutcome.ЧАСТИЧНЫЙ_УСПЕХ
        action = Action(
            name=f"action:{intention.goal[:40]}",
            description=proclamation,
            outcome=outcome,
            result={"score": score, "interpretation": interpretation},
            feedback="результат возвращён в контур рефлексии"
        )
        self.actions_history.append(action)
        return action

    def strengthen(self, trait, amount=0.05):
        if trait in self.character_traits:
            self.character_traits[trait] = min(1.0, self.character_traits[trait] + amount)

class SlavicCognitiveAgent:
    def __init__(self, name="PNEVMA Slavic Cognitive Agent"):
        self.name = name
        self.vedun = Vedun()
        self.volkhv = Volkhv(self.vedun)
        self.veshchun = Veshchun(self.volkhv)
        self.kharakternik = Kharakternik(self.veshchun)
        self._seed()

    def _seed(self):
        seeds = [
            ("Огонь очищает и преобразует", KnowledgeType.ПРИРОДА, ["огонь"]),
            ("Вода является образом потока и памяти", KnowledgeType.РОД, ["вода", "память"]),
            ("Слово является объектом анализа ритуальной речи", KnowledgeType.СЛОВО, ["слово"]),
            ("Болезнь относится к традиционным представлениям о нарушении баланса", KnowledgeType.БОЛЕЗНЬ, ["болезнь"]),
            ("Время мыслится через циклы", KnowledgeType.ВРЕМЯ, ["время", "циклы"]),
            ("Знание позволяет распознавать связи", KnowledgeType.СВЯЗИ, ["знание", "связи"]),
        ]
        for content, typ, tags in seeds:
            self.vedun.learn(content, typ, tags=tags)

    def perceive_and_act(self, observation, goal):
        knowledge = self.vedun.recognize(observation)
        interpretation = self.volkhv.interpret(knowledge)
        proclamation = self.veshchun.proclaim(interpretation)
        intention = self.kharakternik.set_intention(goal, 0.8)
        action = self.kharakternik.act(intention)
        return {
            "observation": observation,
            "knowledge_found": [x.to_dict() for x in knowledge],
            "interpretation": interpretation,
            "proclamation": proclamation,
            "intention": asdict(intention) | {"timestamp": intention.timestamp.isoformat()},
            "action": {
                **asdict(action),
                "outcome": action.outcome.value,
                "timestamp": action.timestamp.isoformat(),
            }
        }

    def learn_new(self, content, ktype, tags=None, confidence=1.0):
        return self.vedun.learn(content, ktype, tags=tags, confidence=confidence)

    def status(self):
        return {
            "name": self.name,
            "knowledge": self.vedun.stats(),
            "character": self.kharakternik.character_traits,
            "actions": len(self.kharakternik.actions_history),
            "proclamations": len(self.veshchun.history),
        }

def graph():
    return {
        "nodes": [
            {"id": "VEDUN", "label": "Ведун", "function": "Knowledge/Memory"},
            {"id": "VOLHV", "label": "Волхв", "function": "Interpretation/Symbolism"},
            {"id": "VESHCHUN", "label": "Вещун", "function": "Communication"},
            {"id": "ZNAKHAR", "label": "Знахарь", "function": "Applied Knowledge"},
            {"id": "KHARAKTERNIK", "label": "Характерник", "function": "Agency/Action"},
        ],
        "edges": [
            {"source": "VEDUN", "target": "VOLHV", "relation": "knowledge→meaning"},
            {"source": "VOLHV", "target": "VESHCHUN", "relation": "meaning→communication"},
            {"source": "VESHCHUN", "target": "ZNAKHAR", "relation": "knowledge→application"},
            {"source": "VESHCHUN", "target": "KHARAKTERNIK", "relation": "communication→intention"},
            {"source": "KHARAKTERNIK", "target": "VEDUN", "relation": "action→feedback"},
        ],
    }

def print_atlas():
    for word, item in ATLAS.items():
        print(f"\n{word.upper()} — {item['role']}")
        print(f"  Ось: {item['axis']}")
        print(f"  Слой: {item['layer']}")
        print(f"  Статус: {item['evidence']}")
        print(f"  {item['note']}")

def main():
    parser = argparse.ArgumentParser(description="PNEVMA–SLAVIC SEMANTIC ATLAS Ω")
    parser.add_argument("query", nargs="?", help="наблюдение/термин")
    parser.add_argument("--interactive", action="store_true")
    parser.add_argument("--atlas", action="store_true")
    parser.add_argument("--graph", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.atlas:
        print_atlas()
        return
    if args.graph:
        print(json.dumps(graph(), ensure_ascii=False, indent=2))
        return

    agent = SlavicCognitiveAgent()

    if args.interactive:
        print("Интерактивный режим. exit — выход; atlas — атлас; graph — граф.")
        while True:
            try:
                q = input("slavic> ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if q.lower() in {"exit", "quit", "выход"}:
                break
            if q.lower() == "atlas":
                print_atlas()
                continue
            if q.lower() == "graph":
                print(json.dumps(graph(), ensure_ascii=False, indent=2))
                continue
            result = agent.perceive_and_act(q, q)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if args.query:
        result = {
            "query": args.query,
            "lexeme": ATLAS.get(args.query.lower()),
            "agent_status": agent.status(),
            "cycle": agent.perceive_and_act(args.query, args.query),
        }
    else:
        result = agent.status()

    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
