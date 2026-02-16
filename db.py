import psycopg2
import pandas as pd
import logging

def get_db_connection(cfg):
    try:
        conn = psycopg2.connect(
            host=cfg["host"],
            port=cfg["port"],
            dbname=cfg["dbname"],
            user=cfg["user"],
            password=cfg["password"],
        )
        logging.info("Connected to database.")
        return conn
    except Exception as e:
        logging.error(f"Database connection failed: {e}")
        raise


def fetch_transactions(conn, start_date, end_date, failure_reasons):
    query = """
    SELECT
        t.id AS transaction_id,
        t.type AS transaction_type,
        t.status,
        t.updated_at,
        t.failure_reason
    FROM transactions t
    WHERE t.failure_reason = ANY(%s)
      AND t.updated_at BETWEEN %s AND %s
    ORDER BY t.id;
    """

    df = pd.read_sql_query(
        query,
        conn,
        params=(failure_reasons, start_date, end_date)
    )

    logging.info(f"Fetched {len(df)} transactions.")
    return df
