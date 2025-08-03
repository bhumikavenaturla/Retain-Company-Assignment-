import requests

short_code = "KTVYIU"  # use the one from your response
response = requests.get(f"http://127.0.0.1:5000/api/stats/{short_code}")

print(response.status_code)
print(response.json())
