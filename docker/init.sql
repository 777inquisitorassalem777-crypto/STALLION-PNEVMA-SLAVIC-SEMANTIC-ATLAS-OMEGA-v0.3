CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS provenance_events (
    id BIGSERIAL PRIMARY KEY,
    event_id TEXT UNIQUE NOT NULL,
    kind TEXT NOT NULL,
    payload_hash TEXT NOT NULL,
    source TEXT NOT NULL,
    evidence_status TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS semantic_memory (
    id BIGSERIAL PRIMARY KEY,
    term TEXT NOT NULL,
    content TEXT NOT NULL,
    evidence_status TEXT NOT NULL,
    source TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
