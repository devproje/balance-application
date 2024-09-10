import psycopg2
from util.config import conn_param

def __main__():
	conn = psycopg2.connect(conn_param)
	cur = conn.cursor()

	cur.execute(
		"""
		create table account(
			name varchar(25),
			username varchar(25) primary key,
			password varchar(50) not null,
			salt varchar(50)
			unique(username)
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

__main__()
