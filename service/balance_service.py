import psycopg2
from pydantic import BaseModel
from util.config import conn_param

class Balance(BaseModel):
	name: str
	date: int
	price: int
	buy: bool = True
	memo: str = ""

class UpdateForm(BaseModel):
	name: str = ""
	date: int = 0
	price: int = 0
	buy: bool = True
	memo: str = ""

class BalanceService:
	def __init__(self):
		self._conn = psycopg2.connect(conn_param)

	def create(self, username: str, balance: Balance):
		ok = True
		cur = self._conn.cursor()
		try:
			cur.execute(
				"insert into balset(name, uid, date, price, buy, memo) values (%s, %s, %s, %s, %s, %s);",
				(balance.name, username, balance.date, balance.price, balance.buy, balance.memo)
			)

			self._conn.commit()
		except:
			self._conn.rollback()
			ok = False
		finally:
			cur.close()
			self._conn.close()

		return ok
	
	def query(self):
		cur = self._conn.cursor()
		cur.execute("select id, name, date, price, buy, memo from balset;")

		raw = cur.fetchall()
		data = []

		if len(raw) == 0:
			return None

		for d in raw:
			data.append({
				"id": d[0],
				"name": d[1],
				"date": d[2],
				"price": d[3],
				"buy": d[4],
				"memo": d[5]
			})

		return data
	
	def read(self, id: int):
		cur = self._conn.cursor()
		cur.execute("select id, name, date, price, buy, memo from balset where id = %s;", (id))

		data = cur.fetchone()
		
		if data == None:
			return None
		
		cur.close()
		self._conn.close()

		return {
			"id": data[0],
			"name": data[1],
			"date": data[2],
			"price": data[3],
			"buy": data[4],
			"memo": data[5]
		}
	
	def update(self, id: int, balance: UpdateForm):
		ok = True
		cur = self._conn.cursor()
		try:
			cur.execute(f"update balset set name = %s, date = %s, price = %s, buy = %s, memo = %s where id = %s;", (
				balance.name,
				balance.date,
				balance.price,
				balance.buy,
				balance.memo,
				id
			))
			self._conn.commit()
		except:
			self._conn.rollback()
			ok = False
		finally:
			cur.close()
			self._conn.close()

		return ok
	
	def delete(self, id: int):
		ok = True
		cur = self._conn.cursor()
		try:
			cur.execute("delete from balset where id = %s;", (id))
			self._conn.commit()
		except:
			self._conn.rollback()
			ok = False
		finally:
			cur.close()
			self._conn.close()
		
		return ok
