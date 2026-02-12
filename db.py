import psycopg2
import pandas as pd

def get_db_connection(db_config):
    return psycopg2.connect(
        host=db_config["host"],
        port=db_config["port"],
        dbname=db_config["dbname"],
        user=db_config["user"],
        password=db_config["password"]
    )

def fetch_transactions(conn, start_date, end_date, failure_reasons):
    """
    Fetch transactions that match given failure reasons within a date range.
    """
    query = """
    SELECT t.id AS transaction_id,
           t.type AS transaction_type,
           t.status AS status,
           t.updated_at AS updated_at,
           t.failure_reason AS failure_reason
    FROM transactions t
    WHERE t.failure_reason = ANY(%s)
      AND t.updated_at BETWEEN %s AND %s
    ORDER BY t.id;
    """
    df = pd.read_sql_query(query, conn, params=(failure_reasons, start_date, end_date))
    return df
