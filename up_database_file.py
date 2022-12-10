from db_config import host, user, password, db_name
import psycopg2
from queries.ext_query import check_db_name_by_user

create_table_for_req_extinsion = """
    CREATE TABLE IF NOT EXISTS request (ID SERIAL PRIMARY KEY, headers TEXT, method TEXT, initiator TEXT, url TEXT, timestamp TEXT, type TEXT, document TEXT, frame TEXT, request TEXT);
"""

create_table_user_and_id = """
    CREATE TABLE IF NOT EXISTS user_agent_to_user_id (USERID SERIAL PRIMARY KEY, USER_AGENT TEXT, MAX_X INTEGER, MAX_Y INTEGER, DATASET INTEGER DEFAULT 0);
"""

create_table_dataset_of_mouse = """
    CREATE TABLE IF NOT EXISTS Note (ID SERIAL PRIMARY KEY, X INTEGER, Y INTEGER, SEASSION_timestamp INTEGER, USERID INTEGER REFERENCES user_agent_to_user_id (USERID) ON DELETE CASCADE, url TEXT);
"""

drop_table_note = """
    DROP TABLE Note
"""

drop_table_user_and_id = """
    DROP TABLE user_agent_to_user_id
"""
drop_table_user = """
    DROP TABLE request
"""

drop_all_user_tables = """
    DROP TABLE user_{0};
"""


def up_all():
    with psycopg2.connect(host=host, user=user, password=password, database=db_name) as conn:
        with conn.cursor() as cursor:
            cursor.execute(drop_table_note)
            cursor.execute(drop_table_user_and_id)
            cursor.execute(drop_table_user)
            for i in range(100):
                cursor.execute(check_db_name_by_user.format(i))
                res = cursor.fetchone()[0]
                if res:
                    cursor.execute(drop_all_user_tables.format(i))
            cursor.execute(create_table_user_and_id)
            cursor.execute(create_table_for_req_extinsion)
            cursor.execute(create_table_dataset_of_mouse)


if __name__ == "__main__":
    up_all()
