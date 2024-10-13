import requests
import json

url = "https://api.elevenlabs.io/v1/voices"

response = requests.request("GET", url)
print(response.text)
response = json.loads(response.text)

print(type(response))

for i in response["voices"]:
    print(i["name"])

