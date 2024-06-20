import httpx
import json

data = json.dumps({
  "uuid": "string",
  "n": 3,
  "x": 5,
  "rank": 6,
  "date": "2024-06-19T20:55:55.248Z"
})
url = f"http://127.0.0.1:8000/trigger_calculate?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZWNoIiwiaWF0IjoxNzE4ODMyODA5LCJleHAiOjE3MTg5MTkyMDl9.U3THuut-_O9OhOfKiTLKf0bLQWBJ9BGs9dTt0VFIWgA"
r = httpx.post(url, data=data)
print(r.content)