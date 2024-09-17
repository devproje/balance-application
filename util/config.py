import os
from dotenv import load_dotenv

load_dotenv(verbose=True, override=True)

def _load_secret():
	try:
		tok = open("./secret_token.txt", "r").read()
	except:
		return ""
	
	return tok

def db_url():
	return os.getenv("DB_URL")

conn_param = "host=%s port=%s dbname=%s user=%s password=%s" % (
	os.getenv("DB_URL"),
	os.getenv("DB_PORT"),
	os.getenv("DB_DATABASE"),
	os.getenv("DB_USERNAME"),
	os.getenv("DB_PASSWORD")
)

secret = _load_secret()
