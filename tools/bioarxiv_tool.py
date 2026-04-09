import requests
from datetime import datetime


BASE_URL = "https://api.biorxiv.org/details/biorxiv"


def search_biorxiv(query, max_results=20, start_date="2023-01-01"):
    """
    Search bioRxiv papers matching a domain query.

    Parameters
    ----------
    query : str
        Research domain (e.g. "computational biology")
    max_results : int
        Maximum papers to return
    start_date : str
        Start date for search (YYYY-MM-DD)

    Returns
    -------
    list of dict
        Papers with title, abstract, authors, date, and link
    """

    end_date = datetime.today().strftime("%Y-%m-%d")

    papers = []
    cursor = 0

    while len(papers) < max_results:

        url = f"{BASE_URL}/{start_date}/{end_date}/{cursor}"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()

        except Exception as e:
            print(f"BioRxiv API error: {e}")
            break

        collection = data.get("collection", [])

        if not collection:
            break

        for paper in collection:

            text_blob = (
                paper.get("title", "") +
                " " +
                paper.get("abstract", "")
            ).lower()

            if query.lower() in text_blob:

                papers.append({
                    "title": paper.get("title"),
                    "authors": paper.get("authors"),
                    "abstract": paper.get("abstract"),
                    "date": paper.get("date"),
                    "doi": paper.get("doi"),
                    "link": f"https://www.biorxiv.org/content/{paper.get('doi')}"
                })

            if len(papers) >= max_results:
                break

        cursor += len(collection)

    return papers