from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from langchain.memory import ChatMessageHistory
from bot_engine import ChatBot
import os
from dotenv import load_dotenv

load_dotenv()

bot = ChatBot()
bot.add_vectorstore_tools("./src/", glob="**/*.py")

# ボットトークンとソケットモードハンドラーを使ってアプリを初期化します
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

@app.event("app_mention")
def handle_mention(event, say):

    history = app.client.conversations_history(
        channel = event["channel"],
        limit=3
    )

    bot_id = app.client.auth_test()["user_id"]

    chat_history = ChatMessageHistory()
    for message in reversed(history["messages"]):
        text = message["text"]
        if message["user"] == bot_id:
            chat_history.add_ai_message(text)
            print(f"ai: {text}")
        else:
            chat_history.add_user_message(text)
            print(f"user: {text}")

    user_message = event["text"]
    bot_message = bot.chat(user_message, chat_history)

    say(bot_message)

# アプリを起動します
if __name__ == "__main__":

    app_env = os.environ.get("APP_ENV", "production")

    if app_env == "production":
        port = os.environ.get("PORT", 3000)
        app.start(port=port)
    else:
        SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()