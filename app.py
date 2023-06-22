import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

app = App(token=os.environ["SLACK_BOT_TOKEN"])

@app.message('hello')
def message_hello(message, say):
    say(
        blocks=[
        {
            "type": "section",
            "text": {"type": "mrkdwn",
                     "text":f"Hey there <@{message['user']}>!"},
            "accessory": {
                "type":"button",
                "text":{"type": "plain_text",
                        "text": "Click Me"},
                "action_id":"button_click"
            }
        }
    ],
    text=f'Hey there <@{message["user"]}>!'

    )

if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()
