import os
from member import MEMBER
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

app = App(token=os.environ["SLACK_BOT_TOKEN"])
member = MEMBER()
@app.message('募集')
def message_hello(message, say):
    member = MEMBER()
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
def handle_submission(ack, body, client, view, logger):
    # `input_c`という block_id に `dreamy_input` を持つ input ブロックがある場合
    #hopes_and_dreams = view["state"]["values"]["section1"]["value-1"]
    can_join_date = view["state"]["values"]["check_input"]["checkboxes-action"]
    date = [x["text"]["text"] for x in can_join_date["selected_options"]]
    date_value=[x["value"] for x in can_join_date["selected_options"]]
    user = body["user"]["id"]
    # 入力値を検証
    user_info = {}
    errors = {}
    ack()
    msg = ""
    try:
        # DB に保存
        if member.is_update(user):
            member.data_post(user, date_value)
            msg = f"{body['user']['name']}さんが行ける日は{date}に変更やな、了解やで〜"
        else:
            member.init_post(user, date_value)
            msg = f"{body['user']['name']}さんが行ける日は{date}やな！了解やで〜"
    except Exception as e:
        # エラーをハンドリング
        msg = "There was an error with your submission"

    # ユーザーにメッセージを送信
    try:
        client.chat_postMessage(channel=user, text=msg)
    except e:
        logger.exception(f"Failed to post a message {e}")
@app.message("参加者")
def show_data(say):
    num = member.check_join()
    say(f'月曜日: {num[0]}人, 火曜日:{num[1]}人, 水曜日:{num[2]}人, 木曜日:{num[3]}人, 金曜日:{num[4]}人')

@app.message("help")
def show_help(message,say):
    say(
	blocks=[
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "👋 ワイができることは今んとこ、こんだけや"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "1️⃣  `募集`って言ってくれたら、今週のフットサル来れる人を聞いたるで、ちなクソ仕様やから募集するたびに前回の募集状況はリセットされるから気いつけてや"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "2️⃣  `参加者`って言ってくれたら何曜日に何人おるか教えたるで"
			}
		}
	],
    text=f"Hey there <@{message['user']}>!"
    )

if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()

