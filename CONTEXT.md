# 🏗 Project Context: PsychoAI

## 👤 User Profile (Alex)
- **Role:** Experienced Backend Architect.
- **Goal:** Mastering Prompt Engineering & AI Agents.
- **Stack Transition:** From High-load Backend -> to AI Engineering.
- **Preferences:** Clean Architecture, Src Layout, understanding low-level API mechanics.

## 🎯 Project Goal
Create a sophisticated **AI Psychologist Telegram Bot** (`PsychoAI`) that acts as a middleware between users and multiple LLMs.

### 🧠 Core Features (PsychoAI)
| Feature | Description |
|---------|-------------|
| **Absolute Memory** | Full context of all sessions, coherent client history |
| **Knowledge Base** | Perls, Yalom, thousands of cases, successful sessions |
| **Navigator** | Psyche map, pattern detection, specific interventions |
| **Red Shield** | Risk prediction (suicide, psychosis), ALERT to therapist |
| **Ethics** | Local storage, encryption, AI talks ONLY to therapist (never to client) |

### 🧩 Architecture
1.  **Frontend:** Telegram Bot (Polling for dev, Webhook for prod).
2.  **Middleware:** Python App (located in `/src`).
    - Logic: Routing, State Management, Logging.
3.  **Backend (Brain) - Multi-Provider:**
    - **Primary:** OpenAI (`gpt-4o-mini`, `gpt-4o`).
    - **Alternative 1:** Google Gemini (High speed/Low cost).
    - **Alternative 2:** YandexGPT (Russian regulatory compliance if needed).
4.  **Observability:** Langfuse (Tracing, Cost analysis).

### 📚 Current Module: "PEs06. Personal Assistant via API"
Building the bot skeleton using `python-telegram-bot` and integrating the Assistants API.

## 📦 Directory Structure (Src Layout)
- `/src` -> Main application code.
- `/notebooks` -> Jupyter sandboxes.
- `/docs` -> Knowledge base.
- `.env` -> Secrets (OPENAI_API_KEY, TELEGRAM_TOKEN, GOOGLE_API_KEY, YANDEX_IAM_TOKEN).

## 🚀 Deployment Strategy
**Path:** `Docker Local` → `Serverless Containers` → `Managed K8s (if needed)`

| Stage | Platform Options | Use Case |
|-------|------------------|----------|
| **Dev** | Docker / Docker Compose | Local development, testing |
| **MVP/Prod** | Yandex Serverless Containers / Google Cloud Run | Serverless, auto-scale to 0, pay-per-use |
| **Alt: VPS** | Yandex Compute / Google CE + Docker | Simple deploy, fixed cost, full control |
| **Scale** | Yandex Managed K8s / GKE Autopilot | Only if horizontal scaling truly needed |

### Platform Comparison
| Feature | Yandex Cloud | Google Cloud |
|---------|--------------|--------------|
| **Serverless Containers** | Serverless Containers | Cloud Run |
| **Managed K8s** | Managed Kubernetes | GKE Autopilot |
| **Registry** | Container Registry | Artifact Registry |
| **Secrets** | Lockbox | Secret Manager |
| **RU Data Compliance** | ✅ Native | ❌ Requires setup |

**Recommendation:** For Telegram bot — Serverless Containers is enough. K8s is overkill unless you need multi-service orchestration.