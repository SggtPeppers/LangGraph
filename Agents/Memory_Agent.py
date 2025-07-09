from email import message
from typing import TypedDict, List, Union
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]


llm = ChatOpenAI(model="gpt-4o")

def procces(state: AgentState) -> AgentState:
    """This node will procces your request"""
    response = llm.invoke(state["messages"])

    state["messages"].append(AIMessage(content=response.content))

    print(f"\nAi: {response.content}")

    return state

graph = StateGraph(AgentState)
graph.add_node("procces", procces)
graph.add_edge(START, "procces")
graph.add_edge("procces", END )

agent = graph.compile()

conversation_history = []

user_input = input("Enter: ")
while user_input != 'exit':
    conversation_history.append(HumanMessage(content=user_input))

    result = agent.invoke({"messages": conversation_history})
    conversation_history = result["messages"]

    user_input = input("Enter: ")

with open("logging.txt", "w") as file:
    file.write("Conversation Log: \n")

    for message in conversation_history:
        if isinstance(message, HumanMessage):
            file.write(f"You: {message.content}\n")
        elif isinstance(message, AIMessage):
            file.write(f"AI: {message.content}\n\n")

    file.write("End of conversation")


print("Conversation saved to loggin.txt")





