# Opsta Line Chat Bot

## Prerequisite

* LLM that support standard OpenAI api
* file `data.pdf` as context

## Manual Run Opsta Line Chat Bot

```bash
# Virtualenv
virtualenv opsta-line-bot
source opsta-line-bot/bin/activate

# Install Requirement
pip install -r requirements.txt

# Export Line channel access token and secret
export LINE_CHANNEL_ACCESS_TOKEN=YOURTOKEN
export LINE_CHANNEL_SECRET=YOURSECRET
export OPENAI_API_KEY=YOUROPENAIKEY

# Or if you have .env file
export $(xargs <.env)

# This will run on port 5000
flask --app chat run --host 0.0.0.0 --port 5000
```

## Run with Docker Compose

```bash
docker compose up
```
