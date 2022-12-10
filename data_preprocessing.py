#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import psycopg2
import math
from db_config import host, user, password, db_name
from sqlalchemy import create_engine


def preprocess_data(id=1):
    from queries.ext_query import get_all_notes_for_user
    get_all_notes_for_user = get_all_notes_for_user.format(id)
    engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}/{db_name}')
    connection = engine.connect()
    df = pd.read_sql(get_all_notes_for_user, connection, index_col='id')
    df2 = pd.read_sql("SELECT * FROM user_agent_to_user_id", connection,
                      index_col='userid')  # TODO for future? max_screen_size

    for let in ['x', 'y']:
        df[f'v({let})'] = [abs((df[f'{let}'][index] - df[f'{let}'][index - 1]) / (
                    df['seassion_timestamp'][index] - df['seassion_timestamp'][index - 1])) if index > 1 else 0 for
                           index in range(1, len(df[f'{let}']) + 1)]
        df[f'a({let})'] = [abs((df[f'v({let})'][index] - df[f'v({let})'][index - 1]) / (
                    df['seassion_timestamp'][index] - df['seassion_timestamp'][index - 1])) if index > 1 else 0 for
                           index in range(1, len(df[f'v({let})']) + 1)]
        df[f'jerk({let})'] = [abs((df[f'a({let})'][index] - df[f'a({let})'][index - 1]) / (
                    df['seassion_timestamp'][index] - df['seassion_timestamp'][index - 1])) if index > 1 else 0 for
                              index in range(1, len(df[f'a({let})']) + 1)]

    for i in ['v', 'a', 'jerk']:
        df[f'{i}(pixels)'] = [math.sqrt(df[f'{i}(x)'][index] ** 2 + df[f'{i}(y)'][index] ** 2) for index in
                              range(1, len(df[f'a({let})']) + 1)]

    df['tan'] = [math.tan(
        (df['x'][index] - df['x'][index - 1]) / (df['y'][index] - df['y'][index - 1] + 0.001)) if index > 1 else 0 for
                 index in range(1, len(df[f'a({let})']) + 1)]

    df.to_sql(name=f"user_{id}", con=connection)
    connection.close()
    delete_query = f"DELETE FROM Note WHERE USERID={id}"
    with psycopg2.connect(host=host, user=user, password=password, database=db_name) as conn:
        with conn.cursor() as cursor:
            cursor.execute(delete_query)


if __name__ == '__main__':
    preprocess_data()
