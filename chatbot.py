import langchain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import os

os.environ['GOOGLE_API_KEY'] = "AIzaSyCEzMSha7n-gShG5UTdEWJVVIlrRWQ_IaU"


llm = ChatGoogleGenerativeAI(model="gemini-pro",
                             temperature=0.7)

store = {}
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

with_message_history = RunnableWithMessageHistory(llm, get_session_history)
def chatbot(session_id: str, message: str) -> str:
    # history = get_session_history(session_id)
    # history.add_message(HumanMessage(message))
    config = {"configurable": {"session_id": session_id}}
    response = with_message_history.invoke([HumanMessage(content=message)],
    config=config,)
    # history.add_message(response)
    return response.content

def chat():
    session_id = "1"
    while True:
        message = input("You: ")
        if message == "\\exit":
            print("Terminting session with chatbot. Press 'y' to continue: ")
            if input() == "y":
                print("Session terminated")
                return 
        response = chatbot(session_id, message)
        print(f"Bot: {response}")

if __name__ == "__main__":
    chat()