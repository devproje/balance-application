import base64, psycopg2
from fastapi import Request
from pydantic import BaseModel
from util.config import conn_param

class AuthData:
	name: str
	username: str
	password: str
	salt: str
	def __init__(self, name: str, username: str, password: str, salt: str):
		self.name = name
		self.username = username
		self.password = password
		self.salt = salt

class Credential(BaseModel):
	username: str
	password: str

class AuthService:
	def __init__(self):
		self._conn = psycopg2.connect(conn_param)

	def create(self, data: AuthData):
		cur = self._conn.cursor()

		try:
			if data.username == "" or data.password == "":
				raise ValueError("username or password must not be null")

			cur.execute(
				"insert into account (name, username, password, salt) values (%s, %s, %s, %s)",
				(data.name, data.username, data.password, data.salt)
			)

			self._conn.commit()
		except:
			self._conn.rollback()
			raise RuntimeError("create account failed")
		finally:
			cur.close()
			self._conn.close()

	def read(self, username: str):
		cur = self._conn.cursor()
		cur.execute("select * from account where username = %s;", (username))
		data = cur.fetchone()
		if data == None:
			return None
		
		cur.close()
		self._conn.close()

		return AuthData(
			name = data[0],
			username = data[1],
			password = data[2],
			salt = data[3]
		)

	def check_auth(self, req: Request) -> bool:
		raw = req.headers.get("Authorization")
		raw_token = raw.removeprefix("Basic ").encode("ascii")

		token = base64.b64decode(raw_token)
		data = token.decode("utf-8").split(":")

		acc = self.read(data[0])
		if acc.username == data[0] and acc.password == data[1]:
			return True
		
		return False
