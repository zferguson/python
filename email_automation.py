import pandas as pd
import os
import csv
import time
import win32com.client as win32
from concurrent.futures import ThreadPoolExecutor
from threading import Lock, Semaphore
from tqdm import tqdm
import re

# -------------------- CONFIG --------------------
INPUT_CSV = 'employee_data.csv'
SENT_LOG = 'sent_log.csv'
FAILED_LOG = 'failed_log.csv'
OUTPUT_DIR = 'personal_csvs'
MAX_WORKERS = 10
MAX_EMAILS_PER_SEC = 5
SUBJECT = 'Your Personal Report'
REPLY_TO = 'data-team@company.com'

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

# Prompt for test or dry run
is_test = input("Is this a test run? (y/n): ").strip().lower() == 'y'
is_dry_run = input("Dry run (no emails sent)? (y/n): ").strip().lower() == 'y'

# Load full data
df_full = pd.read_csv(INPUT_CSV)

# Determine which rows to send
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

# Thread-safe lock and rate limiter
lock = Lock()
rate_limiter = Semaphore(MAX_EMAILS_PER_SEC)

# Ensure output and logs exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

def sanitize_filename(email):
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', email)

def send_email(row):
    email = row['email']
    if email in sent_emails or pd.isna(email) or not str(email).strip():
        return

    try:
        # Build and validate CSV
        filename = f"{sanitize_filename(email)}.csv"
        filepath = os.path.join(OUTPUT_DIR, filename)
        row.to_frame().T.to_csv(filepath, index=False)

        # Validate attached CSV matches expected values
        check = pd.read_csv(filepath)
        if not check.equals(row.to_frame().T.reset_index(drop=True)):
            raise ValueError(f"Mismatch in CSV content for {email}")

        # Respect rate limit
        with rate_limiter:
            time.sleep(1 / MAX_EMAILS_PER_SEC)

            if is_dry_run:
                print(f"[DRY RUN] Would send to: {email}")
                return

            # Send email via Outlook
            outlook = win32.Dispatch("Outlook.Application")
            mail = outlook.CreateItem(0)
            mail.To = email
            mail.Subject = SUBJECT

            name = row.get('name', 'there')
            mail.Body = BODY_TEMPLATE.format(name=name)

            mail.Attachments.Add(filepath)

            # Handle reply-to / bounces
            if REPLY_TO:
                mail.ReplyRecipients.Add(REPLY_TO)

            mail.Send()

        with lock:
            with open(SENT_LOG, 'a', newline='') as log_file:
                csv.writer(log_file).writerow([email])
            print(f"Sent to: {email}")

    except Exception as e:
        with lock:
            with open(FAILED_LOG, 'a', newline='') as log_file:
                csv.writer(log_file).writerow([email, str(e)])
        print(f"Failed to send to {email}: {e}")

# Run threads with progress bar
with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    list(tqdm(executor.map(send_email, [row for _, row in df.iterrows()]), total=len(df)))