from routes.balance import router
from fastapi import FastAPI, Response

app = FastAPI()

@app.get("/")
def index(resp: Response):
	resp.headers.setdefault("Content-Type", "text")
	return "Hello, World!"

app.include_router(router=router)
