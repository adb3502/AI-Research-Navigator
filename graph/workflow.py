from langgraph.graph import StateGraph

from agents.background_agent import analyze_background
from agents.curriculum_agent import curriculum_agent
from agents.research_agent import research_agent
from agents.paper_agent import paper_agent


def build_graph():

    workflow = StateGraph(dict)

    workflow.add_node("background", analyze_background)

    workflow.add_node("curriculum", curriculum_agent)

    workflow.add_node("research", research_agent)

    workflow.add_node("papers", paper_agent)

    workflow.set_entry_point("background")

    workflow.add_edge("background", "curriculum")

    workflow.add_edge("curriculum", "research")

    workflow.add_edge("research", "papers")

    workflow.set_finish_point("papers")

    return workflow.compile()