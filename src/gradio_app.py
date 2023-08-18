import gradio as gr
from langchain.memory import ChatMessageHistory
from bot_engine import ChatBot
import os
from dotenv import load_dotenv

load_dotenv()

class GradioBot:

    def __init__(self):

        self.bot = ChatBot()
        self.bot.add_vectorstore_tools("./src/", glob_pattern="**/*.py")

    def handle_message(self, message, history):

        chat_history = ChatMessageHistory()
        for user, ai in history:
            chat_history.add_user_message(user)
            chat_history.add_ai_message(ai)

        bot_message = self.bot.chat(message, chat_history)

        return bot_message

if __name__ == '__main__':

    bot = GradioBot()

    app_env = os.environ.get("APP_ENV", "production")

    if app_env == "production":
        username = os.environ["GRADIO_USERNAME"]
        password = os.environ["GRADIO_PASSWORD"]
        auth = (username, password)
    else:
        auth = None

    gr.ChatInterface(bot.handle_message).launch(auth=auth)