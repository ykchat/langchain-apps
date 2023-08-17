import gradio as gr
from langchain.chat_models import ChatOpenAI
from langchain.memory import ChatMessageHistory
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(
    model='gpt-3.5-turbo', 
    temperature=0, 
    verbose=True
)

def chat(message, history):
    memory = ChatMessageHistory()
    for user, ai in history:
        memory.add_user_message(user)
        memory.add_ai_message(ai)
    memory.add_user_message(message)
    return llm(memory.messages).content

if __name__ == '__main__':

    app_env = os.environ.get("APP_ENV", "production")

    if app_env == "production":
        username = os.environ["GRADIO_USERNAME"]
        password = os.environ["GRADIO_PASSWORD"]
        auth = (username, password)
    else:
        auth = None

    gr.ChatInterface(chat).launch(auth=auth)