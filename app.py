
import logging
import os
from slack_sdk import WebClient
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

logging.basicConfig(level=logging.DEBUG)

app = App(token=os.environ["SLACK_BOT_TOKEN"])

# イベント API
@app.message("こんにちは")
def handle_messge_evnts(message, say):
    say(f"こんにちは <@{message['user']}> さん！")

# ショートカットとモーダル
@app.shortcut("socket-mode-shortcut")
def handle_shortcut(ack, body: dict, client: WebClient):
    ack()
    client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "modal-id",
            "title": {"type": "plain_text", "text": "タスク登録"},
            "submit": {"type": "plain_text", "text": "送信"},
            "close": {"type": "plain_text", "text": "キャンセル"},
            "blocks": [
                {
                    "type": "input",
                    "block_id": "input-task",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "input",
                        "multiline": True,
                        "placeholder": {
                            "type": "plain_text",
                            "text": "タスクの詳細・期限などを書いてください",
                        },
                    },
                    "label": {"type": "plain_text", "text": "タスク"},
                }
            ],
        },
    )

@app.view("modal-id")
def handle_view_submission(ack, view, logger):
    logger.info(f"Submitted data: {view['state']['values']}")
    ack()

if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()
