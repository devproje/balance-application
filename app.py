import psycopg2
from generate import on_load
from fastapi import FastAPI, Response
from routes.auth import router as auth
from contextlib import asynccontextmanager
from util.config import conn_param, db_url, get_otld
from routes.balance import router as balance
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
	conn = psycopg2.connect(conn_param)
	cur = conn.cursor()

	try:
		print("loading database for: %s" % db_url())
		on_load(conn, cur)
	except:
		print("[warn] error occurred while creating table. aborted")
	finally:
		cur.close()
		conn.close()

	yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"]
)

@app.get("/")
async def index(resp: Response):
	resp.headers.setdefault("Content-Type", "text")
	return "Hello, World!"

app.include_router(router=auth)
app.include_router(router=balance)

if get_otld():
	import logging
	from otlp_tracing import configure_oltp_grpc_tracing
	from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

	logging.basicConfig(level=logging.INFO)
	tracer = configure_oltp_grpc_tracing()
	logger = logging.getLogger(__name__)

	FastAPIInstrumentor.instrument_app(app)
