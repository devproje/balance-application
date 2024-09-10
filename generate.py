import psycopg2, os
import random, string
from getpass import getpass
from util.auth_lib import hash
from util.config import conn_param
from service.auth_service import AuthData, AuthService

def gen_salt(length = 20):
   letters = string.ascii_lowercase + string.digits + string.punctuation
   return ''.join(random.choice(letters) for i in range(length))

def __main__():
	conn = psycopg2.connect(conn_param)
	cur = conn.cursor()

	try:
		f = open("./load.txt", "r")
		if f.read().split("=")[1] == "false":
			raise ValueError("value not true")

		print("server already initialized")
	except: 
		cur.execute(
			"""
			create table if not exists account(
				name varchar(25),
				username varchar(25) not null,
				password varchar(100) not null,
				salt varchar(50),
				primary key(username)
			);
			"""
		)

		cur.execute(
			"""
			create table if not exists balset(
				id serial primary key,
				uid varchar(25) not null,
				name varchar(50),
				date bigint,
				price bigint,
				buy boolean,
				memo varchar(300),
				constraint FK_Account_ID
					foreign key (uid)
					references account(username)
					on delete CASCADE
			);
			"""
		)

		conn.commit()

		cur.close()
		conn.close()

		name = input("input your display name: ")
		username = input("input your username: ")
		password = getpass("input your password: ")
		passchk = getpass("type password one more time: ")
		salt = gen_salt()

		if password != passchk:
			return
		
		hashed_password = hash(password, salt)
		packed = AuthData(
			name=name,
			username=username,
			password=hashed_password,
			salt=salt
		)

		service = AuthService()
		service.create(data=packed)

		f = open("load.txt", "w")
		f.write("init=true")

__main__()
