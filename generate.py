import psycopg2, os
from getpass import getpass
from util.config import conn_param

def __main__():
	conn = psycopg2.connect(conn_param)
	cur = conn.cursor()

	try:
		open("./load.txt", "r")
		print("server already initialized")
	except: 
		cur.execute(
			"""
			create table account(
				name varchar(25),
				username varchar(25),
				password varchar(50) not null,
				salt varchar(50),
				primary key(username)
			);
			"""
		)

		cur.execute(
			"""
			create table balset(
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

		name = input("input your display name: ")
		username = input("input your username: ")
		password = getpass("input your password: ")
		passchk = getpass("type password one more time: ")

		cur.close()
		conn.close()
		f = open("load.txt", "w")
		f.write("init=true")

__main__()
