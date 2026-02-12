# Python Data Pipeline Automation (Portfolio Project)

## Overview
This project demonstrates a **generic, portfolio-ready Python automation workflow** that performs:

- Database extraction of transactions or records within a dynamic weekly range.
- REST API integration with authentication to enrich each record.
- Deduplication and transformation of data.
- Excel report generation for analysis and review.

The workflow is modular, reusable, and designed to mimic real-world enterprise automation pipelines.

---

## Features

- **PostgreSQL Database Integration**  
  Fetches records from a database based on dynamic date ranges and failure conditions.

- **Dynamic Date Calculation**  
  Automatically computes previous week’s range (Saturday → Friday) to extract data.

- **REST API Integration**  
  Authenticates and fetches additional information for each record.

- **Data Deduplication**  
  Ensures each record is processed only once.

- **Excel Reporting**  
  Generates structured Excel files for easy review and sharing.

- **Progress Monitoring**  
  Uses `tqdm` for real-time progress visualization.

- **Modular & Generic Design**  
  Code is organized into separate modules:
  - `db.py` – Database connection and queries
  - `api_client.py` – API authentication and record fetching
  - `report_generator.py` – Excel report builder
  - `utils.py` – Helper functions (date ranges, safe JSON parsing)
  - `main.py` – Orchestrates the workflow

---

## How to Run

1. Clone the repository:

git clone https://github.com/YourUsername/python-data-pipeline-automation.git
cd python-data-pipeline-automation

2. Create a config.ini file with your database and API credentials:

[database]
host = localhost
port = 5432
dbname = mydatabase
user = myuser
password = mypassword

[network]
base_url = https://api.example.com
auth_url = https://auth.example.com
client_id = your_client_id
client_secret = your_client_secret

3. Install dependencies:
   
pip install -r requirements.txt

4. Run the pipeline:

python main.py

5. Output:

Excel file: weekly_report_YYYYMMDD-YYYYMMDD.xlsx containing enriched record data.


Technologies Used

Python 3.x
pandas
psycopg2
openpyxl
urllib3
tqdm

Sample Output

<img width="854" height="433" alt="image" src="https://github.com/user-attachments/assets/bdba0b85-adaa-4815-9fe6-a757639f313e" />

