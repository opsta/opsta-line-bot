import requests
import sys

url = 'http://localhost:5000/health'

response = requests.get(url)

if response.status_code != 200:
  sys.exit(1)

sys.exit(0)
