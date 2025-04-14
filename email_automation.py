import pandas as pd
import os
import csv
import time
import win32com.client as win32
from concurrent.futures import ThreadPoolExecutor
from threading import Lock, Semaphore

# -------------------- CONFIG --------------------
INPUT_CSV = 'employee_data.csv'
SENT_LOG = 'sent_log.csv'
OUTPUT_DIR = 'personal_csvs'
MAX_WORKERS = 10
MAX_EMAILS_PER_SEC = 5
SUBJECT = 'Your Personal Report'
BODY_TEMPLATE = """Hi {name},

Please find your personal data report attached.

Best regards,
Analytics Team
"""

TEST_EMAILS = [
    "test1@example.com",
    "test2@example.com",
    "test3@example.com"
]
TEST_N = len(TEST_EMAILS)
# ------------------------------------------------

# Prompt for test mode
is_test = input("Is this a test run? (y/n): ").strip().lower() == 'y'

# Load full data
df_full = pd.read_csv(INPUT_CSV)

# Determine rows to send
if is_test:
    df = df_full.head(TEST_N).copy()
    df['email'] = TEST_EMAILS[:len(df)]
else:
    df = df_full

# Load sent log
if os.path.exists(SENT_LOG):
    with open(SENT_LOG, newline='') as f:
        sent_emails = set(row[0] for row in csv.reader(f))
else:
    sent_emails = set()

# Ensure output folder exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Thread-safe lock and rate limiter
lock = Lock()
rate_limiter = Semaphore(MAX_EMAILS_PER_SEC)

def send_email(row):
    email = row['email']
    if email in sent_emails:
        return

    filename = f"{email.replace('@', '_at_')}.csv"
    filepath = os.path.join(OUTPUT_DIR, filename)
    row.to_frame().T.to_csv(filepath, index=False)

    try:
        with rate_limiter:
            time.sleep(1 / MAX_EMAILS_PER_SEC)

            outlook = win32.Dispatch("Outlook.Application")
            mail = outlook.CreateItem(0)
            mail.To = email
            mail.Subject = SUBJECT

            name = row.get('name', 'there')
            body = BODY_TEMPLATE.format(name=name)
            mail.Body = body

            mail.Attachments.Add(filepath)
            mail.Send()

        with lock:
            with open(SENT_LOG, 'a', newline='') as log_file:
                csv.writer(log_file).writerow([email])
                print(f"Sent to: {email}")
    except Exception as e:
        print(f"Failed to send to {email}: {e}")

# Run threads
with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    executor.map(send_email, [row for _, row in df.iterrows()])