# S&OP AI Agent — MVP

![Version](https://img.shields.io/badge/version-1.0.0--MVP-blue.svg)
![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)
![React](https://img.shields.io/badge/react-18-blue.svg)

## Executive Summary
This project is an MVP of a Sales & Operations Planning (S&OP) AI Agent for an industrial-machinery manufacturing client. It allows users to query sales data intuitively in natural language, retrieve text-based answers, visualise metrics effortlessly with dynamic charts, and receive threshold-based regional notifications. The agent orchestration happens dynamically depending on the user intent.

## Architecture

```text
User ↔ React Chat UI ↔ FastAPI (/api/chat)
                           ↓
                 LangGraph Orchestrator
                /         |           \
     Intent Node    DataQuery Node   Viz Node
                                       \
                                 Notification Node
```

## Tech Stack
* **Backend:** Python 3.11+, FastAPI, LangGraph, LangChain, OpenAI (`gpt-4o-mini` default), Pandas, Plotly.
* **Frontend:** React 18 (Vite), Axios, react-plotly.js.

## Data Model
The backend relies on three flat CSV files (`backend/data/`):
* `dim_product.csv`: Product dimensions (`product_id`, `product_name`, `category`, `sub_category`, etc.)
* `dim_customer.csv`: Customer dimensions (`customer_id`, `customer_name`, `region`, `segment`, etc.)
* `fact_billing.csv`: Transaction table (`bill_id`, `bill_date`, `customer_id`, `product_id`, `quantity`, `unit_price`, `total_amount`, etc.)

These are loaded and merged into a static in-memory Pandas dataframe `sales_df` for real-time querying.

## Getting Started

### Backend Setup
1. `cd backend`
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and configure your `OPENAI_API_KEY`.
4. `python main.py` or `uvicorn main:app --reload`
The backend will run on `http://localhost:8000`. 

### Frontend Setup
1. `cd frontend`
2. `npm install`
3. `npm run dev`
The client app will launch locally typically on `http://localhost:5173`.

## API Reference
**Endpoint:** `POST /api/chat`
* Request Schema:
  ```json
  {
      "message": "give me total revenue by region",
      "session_id": "default"
  }
  ```
* Response Schema:
  ```json
  {
      "answer": "...",
      "chart": { ... plotly json spec ... },
      "notification": { "person_in_charge": "...", "role": "...", "message": "..." },
      "intent": "visualization"
  }
  ```

## Agent Details
1. **Intent Classifier:** Examines `user_message` and triggers branch routing. Sets `intent` to `data_query`, `visualization`, or `general`. It also pulls out implicit region requirements.
2. **Data Query Agent:** Auto-generates lightweight Pandas code snippets based on the prompt injecting the CSV schema, then dynamically executes them to produce answers.
3. **Visualization Agent:** Creates Plotly charts natively through dynamically generated Plotly Express snippet execution, parsing outputs strictly to JSON specs.
4. **General Agent:** Handles standard conversational greeting / fallback dialogues.
5. **Notification System:** Conditionally assesses if an alert should trigger. Looks up a region's person-in-charge mapping (`config.json`) and bundles a payload for the UI.

## Phase Roadmap
- **Phase 1 (Current):** Data Query + Viz + Notification over flat-file sales data.
- **Phase 2:** RAG layer with domain knowledge (sales SOPs, SCM docs).
- **Phase 3:** Multi-agent hierarchy (Sales Agent, SCM Agent, Production Agent) with supervisory and regional sub-agents.
- **Phase 4:** Production hardening — auth, RBAC, audit trail, deployment.

## Contributing / Dev Notes
Please read `docs/phase_plan.md` for architectural extensions and planned upgrades. Ensure local tests pass seamlessly.

## License
MIT License
