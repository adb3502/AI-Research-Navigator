"""
Flask web server for the AI Research Navigator.
Wraps the LangGraph pipeline with SSE streaming so the UI
can show each agent step as it completes.
"""

import json
import sys
import os

from flask import Flask, render_template, request, Response, stream_with_context

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/navigate", methods=["POST"])
def navigate():
    data = request.get_json(force=True)
    background = (data.get("background") or "").strip()
    target = (data.get("target") or "").strip()

    if not background or not target:
        return {"error": "Both fields are required."}, 400

    def generate():
        state = {"background": background, "target": target}

        try:
            # ── Step 1: Background Analysis ──────────────────────────────
            yield _event("background", "running", message="Analyzing knowledge gaps...")
            from agents.background_agent import analyze_background
            state = analyze_background(state)
            yield _event("background", "done", data=state["knowledge_plan"])

            # ── Step 2: Curriculum Mapping ───────────────────────────────
            yield _event("curriculum", "running", message="Mapping course prerequisites...")
            from agents.curriculum_agent import curriculum_agent
            state = curriculum_agent(state)
            yield _event("curriculum", "done", data=state["courses"])

            # ── Step 3: Research Trends ──────────────────────────────────
            yield _event("research", "running", message="Scanning research landscape...")
            from agents.research_agent import research_agent
            state = research_agent(state)
            yield _event("research", "done", data=state["trends"])

            # ── Step 4: Paper Recommendations ───────────────────────────
            yield _event("papers", "running", message="Selecting key papers...")
            from agents.paper_agent import paper_agent
            state = paper_agent(state)

            # Build clean paper list directly from raw papers (avoids duplication bug)
            raw_papers = state.get("papers", [])[:5]
            paper_data = [
                {"title": p.get("title", ""), "link": p.get("link", "")}
                for p in raw_papers
            ]
            yield _event("papers", "done", data=paper_data)

            yield _event("complete", "done")

        except Exception as exc:
            yield _event("error", "error", message=str(exc))

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


def _event(step, status, message=None, data=None):
    payload = {"step": step, "status": status}
    if message is not None:
        payload["message"] = message
    if data is not None:
        payload["data"] = data
    return f"data: {json.dumps(payload)}\n\n"


if __name__ == "__main__":
    app.run(debug=True, port=5000, threaded=True)
