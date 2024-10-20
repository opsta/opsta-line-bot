import os
from flask import Flask, request, abort

from langchain_openai import ChatOpenAI
from langchain_huggingface.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from openai import APITimeoutError, APIConnectionError

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


# Declare variables from environment variables
configuration = Configuration(access_token=os.environ['LINE_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['LINE_CHANNEL_SECRET'])
openai_api_base = os.environ.get('OPENAI_API_BASE', 'http://localhost:1234/v1')
openai_api_key = os.environ.get('OPENAI_API_KEY', '1234')
openai_temperature = float(os.environ.get('OPENAI_TEMPERATURE', '0.0'))
openai_max_tokens = int(os.environ.get('OPENAI_MAX_TOKENS', None))
embedding_model = os.environ.get('EMBEDDING_MODEL', 'sentence-transformers/all-mpnet-base-v2')
pdf_file = os.environ.get('PDF_FILE', 'data.pdf')
answer_language = os.environ.get('ANSWER_LANGUAGE', 'English')
text_splitter_chunk_size = int(os.environ.get('TEXT_SPLITTER_CHUNK_SIZE', '1000'))
text_splitter_chunk_overlap = int(os.environ.get('TEXT_SPLITTER_CHUNK_OVERLAP', '200'))
search_return_documents = int(os.environ.get('SEARCH_RETURN_DOCUMENTS', '5'))
# THIS IS DUMMY AWS SECRET KEY FOR SECURITY TESTING
aws_secret_key = int(os.environ.get('AWS_SECRET_KEY', '4wcTdlSgTZAIoT7JPLduafIE90St95bQffGx3laI'))

retriever = None
system_prompt = (
  "You are an assistant for question-answering tasks. "
  "Use the following pieces of retrieved context to answer "
  "the question. If you don't know the answer, say that you "
  "don't know. Use three sentences maximum and keep the "
  "answer concise. Answer in " + answer_language + " language."
  "\n\n"
  "{context}"
)
prompt = ChatPromptTemplate.from_messages(
  [
    ("system", system_prompt),
    ("human", "{input}"),
  ]
)


# Function to load PDF for data
def configure_retriever(pdf_file):
  loader = PyPDFLoader(pdf_file)
  docs = loader.load()

  text_splitter = RecursiveCharacterTextSplitter(chunk_size=text_splitter_chunk_size, chunk_overlap=text_splitter_chunk_overlap)
  splits = text_splitter.split_documents(docs)

  embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
  vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
  retriever = vectorstore.as_retriever(search_kwargs={'k': search_return_documents})

  return retriever


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
  with ApiClient(configuration) as api_client:
    global retriever

    try:
      # Call OpenAI
      llm = ChatOpenAI( openai_api_base=openai_api_base,
                        openai_api_key=openai_api_key,
                        temperature=openai_temperature,
                        streaming=True,
                        request_timeout=1,
                        max_tokens=openai_max_tokens,
                      )

      # Chain question
      question_answer_chain = create_stuff_documents_chain(llm, prompt)
      rag_chain = create_retrieval_chain(retriever, question_answer_chain)

      results = rag_chain.invoke({"input": event.message.text})["answer"].strip()
    except (APITimeoutError, APIConnectionError):
      results = "I can't connect to OpenAI " + openai_api_base + " server. Please contact Opsta."
    except Exception as err:
      results = "Unknown error: " + err

    line_bot_api = MessagingApi(api_client)
    line_bot_api.reply_message_with_http_info(
      ReplyMessageRequest(
        reply_token=event.reply_token,
        messages=[TextMessage(text=results)]
      )
    )


def init_app():
  global retriever
  app = Flask(__name__, instance_relative_config=False)
  with app.app_context():
    # Load PDF file
    retriever = configure_retriever(pdf_file)
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

@app.route('/health')
def health():
  return 'OK'
