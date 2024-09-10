from fastapi import FastAPI, Response
from routes.auth import router as auth
from routes.balance import router as balance

app = FastAPI()

@app.get("/")
def index(resp: Response):
	resp.headers.setdefault("Content-Type", "text")
	return "Hello, World!"

app.include_router(router=auth)
app.include_router(router=balance)
