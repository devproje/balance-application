import base64
from hashlib import sha256

def hash(password: str, salt: str):
	m = sha256()
	m.update("{}:{}".format(password, salt).encode())
	
	return m.hexdigest()
	

def gen_token(username: str, hashed_password: str):
	raw = ("{}:{}".format(username, hashed_password)).encode("utf-8")
	raw_token = base64.b64encode(raw)

	token = raw_token.decode("ascii")
	return token
