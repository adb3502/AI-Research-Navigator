import feedparser

def search_arxiv(query, max_results=10):

    url = f"http://export.arxiv.org/api/query?search_query=all:{query}&max_results={max_results}"

    feed = feedparser.parse(url)

    papers = []

    for entry in feed.entries:

        papers.append({
            "title": entry.title,
            "summary": entry.summary,
            "link": entry.link
        })

    return papers