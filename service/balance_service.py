import psycopg2
from pydantic import BaseModel
from util.config import conn_param

class Balance(BaseModel):
	name: str
	date: int
	price: int
	memo: str = ""

class UpdateForm(BaseModel):
	name: str = ""
	date: int = 0
	price: int = 0
	memo: str = ""

class BalanceService:
	def __init__(self):
		self._conn = psycopg2.connect(conn_param)

	def create(self, balance: Balance) -> str:
		cur = self._conn.cursor()
		cur.execute(
			"insert into balset(name, date, price, memo) values (%s, %s, %s, %s);",
			(balance.name, balance.date, balance.price, balance.memo)
		)

		self._conn.commit()
		
		cur.close()
		self._conn.close()

		return balance.name
	
	def read(self, id: int):
		cur = self._conn.cursor()
		cur.execute("select * from balset where id = %s;", (id))

		data = cur.fetchone()
		
		if data == None:
			raise RuntimeError("data not found")
		
		cur.close()
		self._conn.close()

		return {
			"id": data[0],
			"name": data[1],
			"date": data[2],
			"price": data[3],
			"memo": data[4]
		}
	
	def update(self, id: int, act: str, balance: UpdateForm):
		cur = self._conn.cursor()
		cur.execute(f"update balset set {act} = %s where id = %s;", (balance[act], id))

		self._conn.commit()

		cur.close()
		self._conn.close()
	
	def delete(self, id: int):
		cur = self._conn.cursor()
		cur.execute("delete from balset where id = %s;", (id))

		self._conn.commit()

		cur.close()
		self._conn.close()
