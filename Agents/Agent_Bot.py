from typing import TypedDict, List
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv 

load_dotenv()

class AgentState(TypedDict):
    messages: List[HumanMessage]


llm = ChatOpenAI(model="gpt-4o")


def procces(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    print(f"\nAi: {response.content}")
    return state

graph = StateGraph(AgentState)
graph.add_node("procces", procces)
graph.add_edge(START, "procces")
graph.add_edge("procces", END )

agent = graph.compile()


user_input = input("Enter: ")
while user_input != 'exit':
    agent.invoke({"messages": [HumanMessage(content=user_input)]})
    user_input = input("Enter: ")







