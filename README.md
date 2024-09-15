# Opsta Line Chat Bot

## Prerequisite

* LLM that support standard OpenAI api
* file `data.pdf` as context

## Run Opsta Line Chat Bot

```bash
# Virtualenv
virtualenv opsta-line-bot
source opsta-line-bot/bin/activate

# Install Requirement
pip install -r requirements.txt

# Export Line channel access token and secret
export LINE_CHANNEL_ACCESS_TOKEN=YOURTOKEN
export LINE_CHANNEL_SECRET=YOURSECRET

# This will run on port 5000
flask --app chat run
```

## Expose to the world with Ngrok

* Install Ngrok and authen

```bash
# On MacOS
brew install ngrok/ngrok/ngrok

# On Linux
curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
	| sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null \
	&& echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
	| sudo tee /etc/apt/sources.list.d/ngrok.list \
	&& sudo apt update \
	&& sudo apt install ngrok

# Auth
ngrok config add-authtoken [CHANGEME]
```

* Deploy Line Chat Bot app to the world

```bash
ngrok http http://localhost:5000
```
