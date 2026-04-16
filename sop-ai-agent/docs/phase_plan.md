# SOP AI Agent - Feature Roadmap

## Phase 1 — MVP
- Flat CSV data querying.
- Intent classification.
- Plotly based visualisation generation.
- Static notification alerting via frontend overlays.

## Phase 2 — RAG Layer
- Setup ChromaDB or FAISS.
- Document ingestion pipeline (sales SOPs, SCM documents, production manuals as chunked embeddings).
- Incorporate a `rag_retrieval_node` in LangGraph that fetches relevant context before the query/viz agent runs.

## Phase 3 — Multi-Agent Hierarchy
- Upgrade Orcherstrator to a **Business Management Agent** that aggregates delegates to domain-specific nested logic.
- Sales Agent → Sales Supervision Agent, Regional Sales Agent
- Global SCM Agent → SCM sub-agents
- Production Agent → Production Supervision, Regional Factory

## Phase 4 — Production Hardening
- Auth / IDAM (JWT or OAuth).
- Code sandboxing (RestrictedPython / Docker).
- CI/CD & infrastructure-as-code deployments.
- Structured API audit trails.
