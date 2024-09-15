import os
from flask import Flask, request, abort

from langchain_openai import OpenAI

from linebot.v3 import (
  WebhookHandler
)
from linebot.v3.exceptions import (
  InvalidSignatureError
)
from linebot.v3.messaging import (
  Configuration,
  ApiClient,
  MessagingApi,
  ReplyMessageRequest,
  TextMessage
)
from linebot.v3.webhooks import (
  MessageEvent,
  TextMessageContent
)

app = Flask(__name__)

configuration = Configuration(access_token=os.environ['LINE_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['LINE_CHANNEL_SECRET'])
openai_api_base = os.environ.get('OPENAI_API_BASE', 'http://localhost:1234/v1')
openai_api_key = os.environ.get('OPENAI_API_KEY', '1234')
openai_temperature = os.environ.get('OPENAI_TEMPERATURE', '0.0')


@app.route("/callback", methods=['POST'])
def callback():
  # get X-Line-Signature header value
  signature = request.headers['X-Line-Signature']

  # get request body as text
  body = request.get_data(as_text=True)
  app.logger.info("Request body: " + body)

  # handle webhook body
  try:
    handler.handle(body, signature)
  except InvalidSignatureError:
    app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
    abort(400)

  return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
  with ApiClient(configuration) as api_client:

    llm = OpenAI( openai_api_base=openai_api_base, 
                  openai_api_key=openai_api_key, 
                  temperature=float(openai_temperature),
                  streaming=True
          )
    response = llm.invoke(event.message.text)

    line_bot_api = MessagingApi(api_client)
    line_bot_api.reply_message_with_http_info(
      ReplyMessageRequest(
        reply_token=event.reply_token,
        messages=[TextMessage(text=response)]
      )
    )

if __name__ == "__main__":
  app.run()
