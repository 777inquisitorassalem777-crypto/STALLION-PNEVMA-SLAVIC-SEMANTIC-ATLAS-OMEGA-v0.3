# PNEVMA–SLAVIC SEMANTIC ATLAS Ω v0.3

Исследовательский программный прототип на основе предоставленного документа:
**Ведун → Волхв → Вещун → Знахарь → Характерник**.

Проект объединяет:
- историко-лингвистический слой;
- семантический атлас;
- Knowledge/Memory;
- Symbolic Interpretation;
- Communication/Proclamation;
- Intention/Will;
- Action/Agency;
- обратную связь и обучение;
- CLI;
- FastAPI;
- граф семантических связей;
- тесты.

Важно: исторические сведения и современные когнитивные интерпретации разделены.
Модель не утверждает наличие сверхъестественных способностей как факта и не
представляет позднего «характерника» как доказанную праславянскую роль.

## Запуск

```bash
python slavic_cognitive_agent.py
python slavic_cognitive_agent.py --interactive
python slavic_cognitive_agent.py "ведун"
python slavic_cognitive_agent.py "волхв"
python slavic_cognitive_agent.py --atlas
python slavic_cognitive_agent.py --graph
python slavic_cognitive_agent.py --json
```

## API

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Swagger: http://localhost:8000/docs

## Docker

```bash
docker compose up --build
```

## Основной цикл

`ВОСПРИЯТИЕ → ВЕДУН → ВОЛХВ → ВЕЩУН → ВОЛЯ → ДЕЯНИЕ → ОБРАТНАЯ СВЯЗЬ → ВЕДУН`

## Семантическая формула

`ЗНАНИЕ → СЛОВО → СМЫСЛ → ВОЛЯ → ДЕЙСТВИЕ → РЕФЛЕКСИЯ → НОВОЕ ЗНАНИЕ`
