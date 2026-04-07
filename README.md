# ContractEnv — AI Contract Negotiation

## What It Is
ContractEnv is two things built as one:
1. **An OpenEnv RL Environment:** Satisfies all requirements for the Meta/Scaler OpenEnv Hackathon 2026. It features a complete `step()` / `reset()` / `state()` API, a deterministic scripted counterparty, and fully deterministic keyword/logic-based graders for 3 progressively harder tasks.
2. **A Real Two-Sided Negotiation Product:** A production-ready Next.js platform where buyers and sellers upload contracts and set private constraints. Two LLM agents negotiate dynamically via WebSocket streaming until an executable final agreement is reached.

## The Key Feature: Private Constraints
Unlike standard OpenAI Gymnasium environments where everything is public state, ContractEnv introduces **Private Constraints**. When companies start a negotiation, they define deal-breakers and rules (e.g. "liability cap max $50k") which are known only to their respective AI agent. This completely changes the RL dynamics — agents must probe to discover the opponent's limits and negotiate strategically without exposing their own deal-breakers.

## How a Negotiation Works
1. Seller uploads a contract and sets private constraints (deal-breakers, caps, required clauses).
2. Seller generates a unique invite link and sends it to the Client.
3. Client joins and sets their own private constraints.
4. Both hit "Start", and the two AI agents negotiate live on screen, arguing clause by clause.
5. The final agreed contract is presented for both to sign and execute.

## OpenEnv Compliance
We implement complete compliance with the spec:
- **Task 1 (Easy):** Clause Identification (Agent labels 6 clauses as fair/unfair).
- **Task 2 (Medium):** Clause Redlining (Agent proposes better text for unfair clauses).
- **Task 3 (Hard):** Full Negotiation (Agent negotiates multi-turn to reach a deal).
- Fully deterministic grading systems.
- Baseline inference script included (`inference.py`).
- Dockerized and deployed via Hugging Face spaces.

## Quick Start
```bash
# Set up backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn environment.main:app --host 0.0.0.0 --port 7860

# Set up frontend
cd frontend
npm install
npm run dev
```

## Architecture
- `environment/`: FastAPI backend, OpenEnv models, Env simulators, and Graders.
- `frontend/`: Next.js 14 frontend showcasing the product (Pink "legal-elegance" design system).
- `mcp_tools/`: Optional MCP tools for legal reference.
