from fastapi import FastAPI, status, Request, Response
import httpx
import json


app = FastAPI()


@app.post("/billing/trigger_calculate")
async def user_calculate(item_id: int, token: str, data: dict):
	url = f"http://billing_container/trigger_calculate?token={token}"
	data = json.dumps(data)
	r = httpx.post(url, data=data)
	return r.json()


@app.post("/billing/get_data")
async def user_calculate(item_id: int, token: str, data: dict):
	url = f"http://billing_container/get_data?token={token}"
	data = json.dumps(data)
	r = httpx.post(url, data=data)
	return r.json()


@app.get("/billing/get_token")
async def get_token():
	url = f"http://billing_container/get_token"
	r = httpx.get(url)
	return r.json()


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8002)