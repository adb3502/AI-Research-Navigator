# AI Research Navigator

Agentic system that takes a user's background and target research field, then outputs a learning roadmap: prerequisite courses (from IISc catalog), research trends (from arXiv), and recommended papers.

## Running the Project

```bash
# Requires Ollama running locally with llama3 pulled
ollama pull llama3
python main.py
```

## Project Structure

```
main.py                  # CLI entry point
config.py                # Global settings (paths, model names, limits)
graph/workflow.py        # LangGraph StateGraph definition
agents/
  background_agent.py    # Identifies knowledge gaps (llama3 via Ollama)
  curriculum_agent.py    # Lists prerequisite courses (llama3 via Ollama)
  research_agent.py      # Fetches arXiv papers, extracts TF-IDF trends
  paper_agent.py         # Selects top paper recommendations
tools/
  arxiv_tool.py          # arXiv Atom feed search
  bioarxiv_tool.py       # bioRxiv REST API search
  course_tool.py         # IISc course catalog lookup
data/
  iisc_courses.json      # IISc course catalog
output/
  roadmap.txt            # Output file (from config, not yet written by code)
```

## Architecture (Target State from Slides)

User Input -> Planner/Agent (Ollama) -> RAG Layer (Course Mapper + Trend Analyzer) -> Vector Store (cosine similarity) -> Context Builder -> Roadmap Generation via Ollama

## Known Issues

- `paper_agent.py`: titles are appended twice (bug — produces duplicates)
- `course_tool.py`: references undefined `courses` variable
- `tools/bioarxiv_tool.py` and `tools/course_tool.py` are not wired into the graph yet
- `config.py` values are not used by agents (agents hardcode `llama3`)
- Embedding-based RAG from architecture slides is not yet implemented (TF-IDF used instead)

## Stack

- Python 3.9+, LangGraph, LangChain, Ollama (llama3)
- scikit-learn (TF-IDF), sentence-transformers (all-MiniLM-L6-v2)
- feedparser (arXiv), requests (bioRxiv)
