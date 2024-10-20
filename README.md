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

## Sample Kubernetes secret manifest file

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: opsta-line-bot-secrets-dev
  namespace: demo-opsta-line-bot-dev
type: Opaque
stringData:
  LINE_CHANNEL_SECRET: CHANGEME
  LINE_CHANNEL_ACCESS_TOKEN: CHANGEME
  PDF_FILE: https://storage.googleapis.com/bucket/file.pdf
  OPENAI_API_BASE: https://api.openai.com/v1
```

## Security Context

* Add the following to `iac/helm-values/*` to increase container security

```yaml
securityContext:
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
  runAsNonRoot: true
  runAsUser: 65532
  runAsGroup: 65532
  seccompProfile:
    type: RuntimeDefault
  capabilities:
    drop:
      - ALL
```
