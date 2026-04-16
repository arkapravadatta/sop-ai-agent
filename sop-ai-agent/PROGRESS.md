# Implementation Progress

## Phase 1 — MVP  (target: Monday demo)

### Backend
- [x] Folder structure created
- [x] CSV data loader (`loader.py`)
- [x] Pydantic schemas
- [x] FastAPI app + `/api/chat` endpoint
- [x] LangGraph orchestrator graph skeleton
- [x] Intent classifier node
- [x] Data Query agent node
- [x] Visualization agent node
- [x] Notification agent node
- [x] Prompt templates
- [x] Notification `config.json`
- [ ] Unit tests (stretch)

### Frontend
- [x] React app scaffolded (CRA / Vite)
- [x] ChatWindow + MessageBubble
- [x] InputBar
- [x] API integration (`POST /api/chat`)
- [x] ChartPanel (`react-plotly.js`)
- [x] NotificationToast
- [x] Loading spinner
- [ ] Error handling UI

## Phase 2 — RAG Layer  (planned)
- [ ] Vector store setup (ChromaDB / FAISS)
- [ ] Document ingestion pipeline
- [ ] RAG retrieval node in LangGraph

## Phase 3 — Multi-Agent Hierarchy  (planned)
- [ ] Sales Agent + sub-agents
- [ ] SCM Agent + sub-agents
- [ ] Production Agent + sub-agents
- [ ] Business Management orchestrator upgrade

## Phase 4 — Production Hardening  (planned)
- [ ] Auth (JWT / OAuth)
- [ ] RBAC
- [ ] Logging & audit trail
- [ ] Docker / K8s deployment
