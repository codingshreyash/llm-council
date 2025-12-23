# LLM Council

![llmcouncil](header.jpg)

> **Note:** This is a fork/modification of the original [LLM Council](https://github.com/karpathy/llm-council) project by [Andrej Karpathy](https://github.com/karpathy). The original project used OpenRouter to access multiple LLM providers. This version has been modified to use direct API access to OpenAI, Anthropic, and Google (Gemini) instead.

The idea of this repo is that instead of asking a question to your favorite LLM provider (e.g. OpenAI GPT-4o, Google Gemini, Anthropic Claude Sonnet, etc.), you can group them into your "LLM Council". This repo is a simple, local web app that essentially looks like ChatGPT except it uses direct API access to send your query to multiple LLMs, it then asks them to review and rank each other's work, and finally a Chairman LLM produces the final response.

In a bit more detail, here is what happens when you submit a query:

1. **Stage 1: First opinions**. The user query is given to all LLMs individually, and the responses are collected. The individual responses are shown in a "tab view", so that the user can inspect them all one by one.
2. **Stage 2: Review**. Each individual LLM is given the responses of the other LLMs. Under the hood, the LLM identities are anonymized so that the LLM can't play favorites when judging their outputs. The LLM is asked to rank them in accuracy and insight.
3. **Stage 3: Final response**. The designated Chairman of the LLM Council takes all of the model's responses and compiles them into a single final answer that is presented to the user.

## Credits

This project is based on the original [LLM Council](https://github.com/karpathy/llm-council) project by [Andrej Karpathy](https://github.com/karpathy). The original project was 99% vibe coded as a fun Saturday hack to explore and evaluate a number of LLMs side by side in the process of [reading books together with LLMs](https://x.com/karpathy/status/1990577951671509438). This fork modifies the original to use direct API access instead of OpenRouter.

## Modifications

This version has been modified to:
- Use direct API access to OpenAI, Anthropic, and Google (Gemini) instead of OpenRouter
- Support provider-specific API keys and model identifiers
- Maintain the same 3-stage council functionality and UI

## Setup

### 1. Install Dependencies

The project uses [uv](https://docs.astral.sh/uv/) for project management.

**Backend:**
```bash
uv sync
```

**Frontend:**
```bash
cd frontend
npm install
cd ..
```

### 2. Configure API Keys

Create a `.env` file in the project root (you can copy from `.env.example`):

```bash
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...
```

Get your API keys:
- **OpenAI:** [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **Anthropic:** [console.anthropic.com](https://console.anthropic.com/)
- **Google:** [makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)

### 3. Configure Models (Optional)

Edit `backend/config.py` to customize the council. Model identifiers use the format `"provider:model_name"`:

```python
COUNCIL_MODELS = [
    "openai:gpt-4o",
    "google:gemini-2.0-flash-exp",
    "anthropic:claude-3-5-sonnet-20241022",
]

CHAIRMAN_MODEL = "google:gemini-2.0-flash-exp"
```

Available providers:
- `openai:` - OpenAI models (e.g., `gpt-4o`, `gpt-4-turbo`)
- `anthropic:` - Anthropic models (e.g., `claude-3-5-sonnet-20241022`, `claude-sonnet-4-20250514`)
- `google:` - Google Gemini models (e.g., `gemini-2.0-flash-exp`, `gemini-1.5-pro`)

## Running the Application

**Option 1: Use the start script**
```bash
./start.sh
```

**Option 2: Run manually**

Terminal 1 (Backend):
```bash
uv run python -m backend.main
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

Then open http://localhost:5173 in your browser.

## Tech Stack

- **Backend:** FastAPI (Python 3.10+), direct API clients for OpenAI, Anthropic, and Google
- **Frontend:** React + Vite, react-markdown for rendering
- **Storage:** JSON files in `data/conversations/`
- **Package Management:** uv for Python, npm for JavaScript
