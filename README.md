# PsychoAI — AI Psychologist Assistant

> Diploma project for "Prompt Engineering 3.0" course

AI-powered assistant for psychotherapists. Acts as a "memory exoskeleton" — stores session context, detects patterns, suggests interventions.

## Features

- **Absolute Memory** — full context of all sessions
- **Knowledge Base** — trained on Perls, Yalom, thousands of cases
- **Navigator** — pattern detection, specific interventions
- **Red Shield** — risk prediction (suicide, psychosis), alerts
- **Multi-LLM** — OpenAI, Google Gemini, YandexGPT

## Tech Stack

- Python 3.11+ (async, strict typing)
- Telegram Bot (`python-telegram-bot` v20.x)
- OpenAI Assistants API / LangChain LCEL
- Docker / Docker Compose
- Langfuse (observability)

## Quick Start

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/promt_engineer_study.git
cd promt_engineer_study

# Setup
cp .env.example .env
# Edit .env with your API keys

# Install dependencies
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run
python -m src.main
```

## Project Structure

```
├── src/                 # Main application code
├── notebooks/           # Jupyter sandboxes
├── docs/                # Knowledge base, course materials
├── k8s/                 # Kubernetes manifests (if needed)
├── .env.example         # Environment template
├── docker-compose.yml   # Local development
├── Dockerfile           # Container build
└── CONTEXT.md           # Project context for AI assistants
```

## Deployment

| Environment | Platform |
|-------------|----------|
| Dev | Docker Compose (local) |
| Prod | Yandex Serverless Containers / Google Cloud Run |

## License

MIT

---

*Part of "Prompt Engineering 3.0" course diploma work*
