import psycopg2
from db_config import host, user, password, db_name

query = """
SELECT * FROM Note;
"""

query_2 = """
SELECT * FROM user_agent_to_user_id;
"""

query_3 = """
SELECT * FROM request;
"""


with psycopg2.connect(host=host, user=user, password=password, database=db_name) as conn:
    with conn.cursor() as cursor:
        cursor.execute(query)
        print(cursor.fetchone())
        cursor.execute(query_2)
        print(cursor.fetchone())
        #cursor.execute(query_3)
        #print(cursor.fetchall())
        #cursor.execute("""SELECT * FROM Note WHERE SEASSION_timestamp = 1000;""")
        #print(cursor.fetchall())