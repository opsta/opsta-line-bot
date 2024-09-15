import os
from flask import Flask, request, abort

from langchain_openai import OpenAI
from langchain_huggingface.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

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

retriever = None
llm = None
system_prompt = (
  "You are an assistant for question-answering tasks. "
  "Use the following pieces of retrieved context to answer "
  "the question. If you don't know the answer, say that you "
  "don't know. Use three sentences maximum and keep the "
  "answer concise. Answer in Thai language."
  "\n\n"
  "{context}"
)
prompt = ChatPromptTemplate.from_messages(
  [
    ("system", system_prompt),
    ("human", "{input}"),
  ]
)

# Declare variables from environment variables
configuration = Configuration(access_token=os.environ['LINE_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['LINE_CHANNEL_SECRET'])
openai_api_base = os.environ.get('OPENAI_API_BASE', 'http://localhost:1234/v1')
openai_api_key = os.environ.get('OPENAI_API_KEY', '1234')
openai_temperature = os.environ.get('OPENAI_TEMPERATURE', '0.0')
embedding_model = os.environ.get('EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')
pdf_file = os.environ.get('PDF_FILE', 'data.pdf')


# Function to load PDF for data
def configure_retriever(pdf_file):
  loader = PyPDFLoader(pdf_file)
  docs = loader.load()

  text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=300)
  splits = text_splitter.split_documents(docs)

  embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
  vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
  retriever = vectorstore.as_retriever()

  return retriever


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
  with ApiClient(configuration) as api_client:
    global retriever, llm

    # Chain question
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    results = rag_chain.invoke({"input": event.message.text})

    line_bot_api = MessagingApi(api_client)
    line_bot_api.reply_message_with_http_info(
      ReplyMessageRequest(
        reply_token=event.reply_token,
        messages=[TextMessage(text=results["answer"].strip())]
      )
    )


def init_app():
  global retriever, llm
  app = Flask(__name__, instance_relative_config=False)
  with app.app_context():
    # Load PDF file
    retriever = configure_retriever(pdf_file)
    # Call OpenAI
    llm = OpenAI( openai_api_base=openai_api_base,
                  openai_api_key=openai_api_key,
                  temperature=float(openai_temperature),
                  streaming=True
          )
    return app


app = init_app()

if __name__ == "__main__":
  app.run()


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
