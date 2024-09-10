import psycopg2
from util.config import conn_param

def __main__():
	conn = psycopg2.connect(conn_param)
	cur = conn.cursor()

	cur.execute(
		"""
		create table balset(
			id serial primary key,
			name varchar(50),
			date bigint,
			price bigint,
			memo varchar(300)
		);
		"""
	)

	conn.commit()
	
	cur.close()
	conn.close()

__main__()
