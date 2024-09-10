from fastapi import FastAPI, Response
from routes.auth import router as auth
from routes.balance import router as balance
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["POST, GET, PATCH, DELETE"],
	allow_headers=["*"]
)

@app.get("/")
def index(resp: Response):
	resp.headers.setdefault("Content-Type", "text")
	return "Hello, World!"

app.include_router(router=auth)
app.include_router(router=balance)
