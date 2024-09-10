import os
from dotenv import load_dotenv

load_dotenv()

conn_param = "host=%s port=%s dbname=%s user=%s password=%s" % (
	os.getenv("DB_URL"),
	os.getenv("DB_PORT"),
	os.getenv("DB_DATABASE"),
	os.getenv("DB_USERNAME"),
	os.getenv("DB_PASSWORD")
)
