from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

llm = ChatOllama(model="llama3")

def analyze_background(state):

    prompt = f"""
User background: {state['background']}
Target domain: {state['target']}

Identify knowledge gaps and required prerequisite subjects.
"""

    response = llm.invoke([HumanMessage(content=prompt)])

    state["knowledge_plan"] = response.content

    return state