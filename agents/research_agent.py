from tools.arxiv_tool import search_arxiv
from sklearn.feature_extraction.text import TfidfVectorizer

def research_agent(state):

    papers = search_arxiv(state["target"],50)

    print("Papers fetched:", len(papers))

    abstracts = [p.get("summary", "") for p in papers]

    # ✅ Clean data
    abstracts = [a.strip() for a in abstracts if a and a.strip()]

    if len(abstracts) == 0:
        raise ValueError("No valid abstracts found. Check arxiv_tool output.")

    vectorizer = TfidfVectorizer(stop_words="english", max_features=10)

    X = vectorizer.fit_transform(abstracts)

    trends = vectorizer.get_feature_names_out()

    state["papers"] = papers
    state["trends"] = trends.tolist()

    return state