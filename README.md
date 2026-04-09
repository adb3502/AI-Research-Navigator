# Meridian — Agentic Interdisciplinary Research Navigator

A multi-agent system that generates a personalised research roadmap for anyone moving into a new academic field. Given a user's background and a target domain, Meridian identifies knowledge gaps, maps prerequisite courses from the IISc catalog, extracts current research trends from arXiv, and recommends key papers — all surfaced through a live-streaming web UI.

---

## Problem

Researchers and students entering an unfamiliar discipline face three compounding problems:

- **Unclear learning path** — no structured guide from their current knowledge to the target field
- **Information overload** — generic web searches return too much noise, too little signal
- **No trend awareness** — existing tools do not surface what is actually being researched right now

---

## Solution

Meridian orchestrates four specialised agents in a LangGraph pipeline, each resolving one piece of the problem:

```
User Input (background + target)
        │
        ▼
┌─────────────────┐
│  Background     │  LLM identifies knowledge gaps and prerequisite subjects
│  Agent          │  between the user's background and the target domain
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Curriculum     │  LLM recommends 5 foundational courses to study first
│  Agent          │  (cross-referenced against IISc course catalog)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Research       │  Fetches recent papers from arXiv, extracts trending
│  Agent          │  keywords using TF-IDF (scikit-learn)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Paper          │  Selects top 5 recommended papers with direct links
│  Agent          │
└────────┬────────┘
         │
         ▼
  Structured Roadmap
  (streamed to browser via SSE)
```

---

## Architecture

### Backend

| Layer | Technology |
|---|---|
| Agent orchestration | LangGraph `StateGraph` |
| LLM inference | Ollama (llama3, local) |
| LLM interface | LangChain + `langchain-ollama` |
| Paper retrieval | arXiv Atom API via `feedparser` |
| Preprint retrieval | bioRxiv REST API via `requests` |
| Trend extraction | TF-IDF vectoriser (`scikit-learn`) |
| Embeddings (configured) | `sentence-transformers` — `all-MiniLM-L6-v2` |
| Web server | Flask with SSE streaming |
| Course data | IISc course catalog (`data/iisc_courses.json`) |

### Frontend

| Feature | Implementation |
|---|---|
| Multi-step wizard | Vanilla JS view transitions (fade + translate) |
| Live agent progress | `EventSource` SSE — pipeline steps light up in real-time |
| Typography | Playfair Display · Cormorant Garamond · Courier Prime |
| Styling | Pure CSS — dot-grid background, warm academic palette |
| No build step | Single `templates/index.html` served by Flask |

### Data Flow

```
Browser → POST /api/navigate
       ← SSE stream: per-agent status + data events
       ← { step, status, data } JSON frames
```

Each agent yields two SSE events: `running` (triggers UI animation) and `done` (renders result panel).

---

## Project Structure

```
.
├── app.py                  # Flask server — SSE endpoint + route
├── main.py                 # CLI entry point (no UI)
├── config.py               # Global settings (model, paths, limits)
│
├── graph/
│   └── workflow.py         # LangGraph StateGraph definition
│
├── agents/
│   ├── background_agent.py # Knowledge gap analysis via LLM
│   ├── curriculum_agent.py # Course recommendation via LLM
│   ├── research_agent.py   # arXiv fetch + TF-IDF trend extraction
│   └── paper_agent.py      # Top-5 paper selection
│
├── tools/
│   ├── arxiv_tool.py       # arXiv Atom feed search
│   ├── bioarxiv_tool.py    # bioRxiv REST API search
│   └── course_tool.py      # IISc course catalog lookup
│
├── data/
│   └── iisc_courses.json   # IISc course catalog
│
├── templates/
│   └── index.html          # Meridian web UI (single file)
│
└── requirement.txt
```

---

## Setup

### Prerequisites

- Python 3.9+
- [Ollama](https://ollama.com) installed and running locally

### Install

```bash
# Clone
git clone https://github.com/adb3502/AI-Research-Navigator.git
cd AI-Research-Navigator

# Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirement.txt

# Pull the LLM model
ollama pull llama3
```

### Run (Web UI)

```bash
python app.py
# Open http://localhost:5000
```

### Run (CLI)

```bash
python main.py
# Prompts for background and target field, prints results to terminal
```

---

## Configuration

All settings live in `config.py`:

| Setting | Default | Description |
|---|---|---|
| `LLM_MODEL` | `gpt-4o-mini` | Model name (agents currently use `llama3` via Ollama directly) |
| `ARXIV_MAX_RESULTS` | `40` | Papers fetched per arXiv query |
| `BIORXIV_MAX_RESULTS` | `40` | Papers fetched per bioRxiv query |
| `PAPER_START_YEAR` | `2023-01-01` | Earliest paper date for bioRxiv search |
| `MAX_TREND_KEYWORDS` | `15` | Max TF-IDF keywords extracted |
| `TOP_PAPER_RECOMMENDATIONS` | `5` | Papers shown in output |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | Sentence transformer for future RAG layer |

---

## Example Output

**Background:** Mechanical Engineering → **Target:** Biophysics

**Knowledge Gaps identified:**
- Cell biology, biochemistry, molecular biology
- Physical biology: thermodynamics applied to biological systems
- Biophysical measurement techniques (AFM, optical tweezers)

**Courses recommended:**
1. Biostatistics
2. Cell Biology
3. Molecular Biology
4. Biochemistry
5. Computational Methods in Biology

**Research trends (from arXiv):**
`biological` · `biophysical` · `model` · `single` · `molecular` · `dynamics` · `protein` · `neural` · `membrane` · `simulation`

**Recommended papers:**
- *Retina organoids: Window into the biophysics of neuronal systems*
- *Biophysics software for interdisciplinary education and research*
- *Single-molecule dynamics in living cells revealed by fluorescence*

---

## Differentiator

| Generic LLM | Meridian |
|---|---|
| Generic biology + physics topics | Knowledge gaps specific to your background |
| No course structure | Prerequisite courses from IISc catalog |
| Static training data | Live arXiv papers from 2023 onwards |
| One-shot response | Real-time agent pipeline with per-step progress |

---

## Roadmap

- [ ] Wire `course_tool.py` into curriculum agent for catalog-grounded recommendations
- [ ] Integrate bioRxiv papers alongside arXiv
- [ ] Replace TF-IDF trend extraction with embedding-based semantic clustering (RAG layer)
- [ ] Add cosine-similarity vector store for paper recommendations
- [ ] Export roadmap as PDF

---

## Dependencies

```
langchain / langgraph / langsmith
langchain-ollama
ollama
flask
requests
feedparser
pandas / numpy
scikit-learn
sentence-transformers
python-dotenv
tqdm / rich
```

---

## Presented at

**AI for Learning / Teaching** — Indian Institute of Science, 2025
Topic: *Agentic Interdisciplinary Research Navigator: Automated Skill Mapping and Trend Analysis from Scientific Literature*
