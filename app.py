import os
from member import MEMBER
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

app = App(token=os.environ["SLACK_BOT_TOKEN"])
@app.message('フットサルのスケジュール')
def message_hello(message, say):
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"フットサルいつやりますか？"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text":"VOTE!!"},
                    "action_id": "button_click"
                }
            }
        ],
        text=f"Hey there <@{message['user']}>!"
    )
@app.action("button_click")
def action_button_click(body, ack, client):
    ack() #アクションを確認したことを即時で応答する
    # 組み込みのクライアントで views_open を呼び出し
    client.views_open(
        # 受け取りから 3 秒以内に有効な trigger_id を渡す
        trigger_id=body["trigger_id"],
        # ビューのペイロード
        view={
            "type": "modal",
            # ビューの識別子
            "callback_id": "view_1",
            "title": {"type": "plain_text", "text":"今週フットサル、マ？"},
            "submit": {"type": "plain_text", "text":"Submit"},
            "blocks": [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "New Paid Time Off request from <example.com|Fred Enriquez>\n\n<https://example.com|View request>"
			}
		},
		{
			"type": "input",
            "block_id":"check_input",
			"element": {
				"type": "checkboxes",
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": "月曜日",
						},
						"value": "value-0"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "火曜日",
						},
						"value": "value-1"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "水曜日",
						},
						"value": "value-2"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "木曜日",
						},
						"value": "value-3"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "金曜日",
						},
						"value": "value-4"
					}
				],
				"action_id": "checkboxes-action"
			},
			"label": {
				"type": "plain_text",
				"text": "Label",
			}
		}
	]
    }
    )
# view_submission リクエストを処理
@app.view("view_1")
def handle_submission(ack, body, client, view, logger, Member):
    # `input_c`という block_id に `dreamy_input` を持つ input ブロックがある場合
    #hopes_and_dreams = view["state"]["values"]["section1"]["value-1"]
    can_join_date = view["state"]["values"]["check_input"]["checkboxes-action"]
    print(can_join_date["selected_options"])
    date = [x["text"]["text"] for x in can_join_date["selected_options"]]
    user = body["user"]["id"]
    print(body["user"])
    # 入力値を検証
    user_info = {}
    errors = {}
    ack()
    msg = ""
    try:
        # DB に保存
        msg = f"{body['user']['name']}さんが行ける日は{date}ですね！了解しました！"
    except Exception as e:
        # エラーをハンドリング
        msg = "There was an error with your submission"

    # ユーザーにメッセージを送信
    try:
        client.chat_postMessage(channel=user, text=msg)
    except e:
        logger.exception(f"Failed to post a message {e}")

if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()
