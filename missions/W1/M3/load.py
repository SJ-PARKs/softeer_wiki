import sqlite3
from log_file import log_message

# Load 함수
def load_to_db(df, db_name, table_name, if_exists="replace"):
    log_message(f"Load start - DB: {db_name}, Table: {table_name}")
    conn = sqlite3.connect(db_name)

    df.to_sql(
        table_name,
        conn,
        if_exists=if_exists,
        index=False
    )

    conn.close()
    log_message(f"Load end - DB: {db_name}, Table: {table_name}")
