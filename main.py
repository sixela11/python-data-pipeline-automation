import configparser
from tqdm import tqdm
from db import get_db_connection, fetch_transactions
from api_client import APIClient
from report_generator import ExcelReport
from utils import get_previous_week_range, safe_json

# Load config
config = configparser.ConfigParser()
config.read("config.ini")
db_config = config["database"]
net_conf = config["network"]

# Connect DB
conn = get_db_connection(db_config)

# Compute previous week
start_date, end_date = get_previous_week_range()

# Fetch transactions
failure_reasons = ["ERROR_TYPE_A", "ERROR_TYPE_B"]
df = fetch_transactions(conn, start_date, end_date, failure_reasons)
conn.close()

if df.empty:
    print("⚠ No transactions found")
    exit()

# Authenticate API client
client = APIClient(
    net_conf["base_url"],
    net_conf["auth_url"],
    net_conf["client_id"],
    net_conf["client_secret"]
)
client.authenticate()

# Prepare Excel report
headers = ["Transaction ID", "Type", "Status", "Failure Reason", "Extra Info"]
report = ExcelReport("weekly_report.xlsx", headers)

# Fetch extra info from API
for transaction_id in tqdm(df["transaction_id"].unique(), desc="Fetching records"):
    fields = client.fetch_record(transaction_id)
    row = [
        transaction_id,
        df.loc[df.transaction_id == transaction_id, "transaction_type"].values[0],
        df.loc[df.transaction_id == transaction_id, "status"].values[0],
        df.loc[df.transaction_id == transaction_id, "failure_reason"].values[0],
        safe_json(fields, "extra_info")
    ]
    report.add_row(row)

# Save report
report.save()
