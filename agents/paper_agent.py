def paper_agent(state):

    papers = state["papers"][:5]

    recommendations = [p["title"] for p in papers]
    for p in papers:
        recommendations.append(p["title"])

    state["recommended_papers"] = recommendations

    return state