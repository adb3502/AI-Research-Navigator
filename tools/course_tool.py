def find_relevant_courses(domain):

    relevant = []

    for c in courses:

        keywords = c.get("keywords", [])

        if domain.lower() in " ".join(keywords).lower():

            relevant.append(c)

    return relevant