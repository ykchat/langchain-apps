from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from langchain.memory import ChatMessageHistory
from bot_engine import ChatBot
import os
from dotenv import load_dotenv

load_dotenv()

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

class SlackBot:

    def __init__(self, app):

        self.bot = ChatBot()
        self.bot.add_vectorstore_tools("./src/", glob_pattern="**/*.py")

        self.app = app
        self.app.event("app_mention")(self.handle_mention)

    def handle_mention(self, event, say):

        history = self.app.client.conversations_history(
            channel = event["channel"],
            limit=3
        )

        bot_id = self.app.client.auth_test()["user_id"]

        chat_history = ChatMessageHistory()
        for message in reversed(history["messages"]):
            text = message["text"]
            if message["user"] == bot_id:
                chat_history.add_ai_message(text)
            else:
                chat_history.add_user_message(text)

        user_message = event["text"]
        bot_message = self.bot.chat(user_message, chat_history)

        say(bot_message)

if __name__ == "__main__":

    bot = SlackBot(app)

    app_env = os.environ.get("APP_ENV", "production")

    if app_env == "production":
        port = os.environ.get("PORT", 3000)
        app.start(port=port)
    else:
        SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()