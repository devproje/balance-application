import os
import psycopg2
import time as time_2
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter

load_dotenv()

conn_param = "host=%s port=%s dbname=%s user=%s password=%s" % (
	os.getenv("DB_URL"),
	os.getenv("DB_PORT"),
	os.getenv("DB_DATABASE"),
	os.getenv("DB_USERNAME"),
	os.getenv("DB_PASSWORD")
)

app = FastAPI()
router = APIRouter()

class Balance(BaseModel):
	name: str
	date: int
	price: int

@router.get("/")
def index():
	return "Hello, World!"

@router.post("/balance")
def insert(balance: Balance):
	started = time_2.time()
	conn = psycopg2.connect(conn_param)
	cur = conn.cursor()
	cur.execute(
		"insert into balset(name, date, price) values (%s, %s, %s);",
		(balance.name, balance.date, balance.price)
	)

	conn.commit()
	
	cur.close()
	conn.close()

	return {"ok": 1, "respond_time": f"{time_2.time() - started}ms", "name": balance.name}

@router.get("/balance/{id}")
def query(id):
	conn = psycopg2.connect(conn_param)
	cur = conn.cursor()
	cur.execute(
		"select * from balset where id = %s",
		id
	)

	data = cur.fetchone()
	cur.close()
	conn.close()

	return {"ok": 1, "data": {"id": data[0], "name": data[1], "date": data[2], "price": data[3]}}

@router.patch("/balance/{id}")
def update():
	return {"ok": 1, "id": "test"}

@router.delete("/balance/{id}")
def delete():
	return {"ok": 1, "id": "test"}

app.include_router(router=router)
