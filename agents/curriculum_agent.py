from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3")

def curriculum_agent(state):

    prompt = f"""
A user has the following background:
{state['background']}

They want to move into this research field:
{state['target']}

List 5 important courses or subjects they should study first.
Only return a short list.
"""

    response = llm.invoke(prompt)

    state["courses"] = response.content

    return state