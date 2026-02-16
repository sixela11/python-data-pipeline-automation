import argparse
import logging
import os
from dotenv import load_dotenv
from tqdm import tqdm

from logger import setup_logger
from db import get_db_connection, fetch_transactions
from api_client import APIClient
from report_generator import ExcelReport
from utils import get_previous_week_range, safe_json

# setup logging
setup_logger()

# load environment variables
load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Transaction Failure Report Generator")
    parser.add_argument("--start", help="Start date YYYY-MM-DD")
    parser.add_argument("--end", help="End date YYYY-MM-DD")
    args = parser.parse_args()

    # DB config
    db_config = {
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
        "dbname": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
    }

    conn = get_db_connection(db_config)

    # date range
    if args.start and args.end:
        start_date, end_date = args.start, args.end
    else:
        start_date, end_date = get_previous_week_range()

    failure_reasons = ["ERROR_TYPE_A", "ERROR_TYPE_B"]

    df = fetch_transactions(conn, start_date, end_date, failure_reasons)
    conn.close()

    if df.empty:
        logging.warning("No transactions found.")
        return

    # optimize lookup
    lookup = df.set_index("transaction_id").to_dict("index")

    # API client
    client = APIClient(
        os.getenv("API_BASE_URL"),
        os.getenv("API_AUTH_URL"),
        os.getenv("API_CLIENT_ID"),
        os.getenv("API_CLIENT_SECRET"),
    )

    client.authenticate()

    # report
    report = ExcelReport(
        "weekly_report.xlsx",
        ["Transaction ID", "Type", "Status", "Failure Reason", "Extra Info"],
    )

    for tx_id in tqdm(lookup.keys(), desc="Fetching API records"):
        fields = client.fetch_record(tx_id)
        row_data = lookup[tx_id]

        report.add_row([
            tx_id,
            row_data["transaction_type"],
            row_data["status"],
            row_data["failure_reason"],
            safe_json(fields, "extra_info"),
        ])

    report.save()
    logging.info("Report generated successfully.")

if __name__ == "__main__":
    main()
