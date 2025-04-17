import win32com.client
import re
import csv
import os
from datetime import datetime, timedelta

def extract_email_and_name(body):
    """
    Extract recipient name and email from the body of an undeliverable message.
    """
    match = re.search(r'to\s+(.+?)\s+<(.+?)>', body, re.IGNORECASE)
    if match:
        name, email = match.groups()
        return name.strip(), email.strip()

    match = re.search(r'[\w\.-]+@[\w\.-]+', body)
    if match:
        return None, match.group().strip()

    return None, None

def get_undeliverable_recipients_since_yesterday():
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6)

    # Format the date for Restrict (Outlook expects: 'mm/dd/yyyy hh:mm AM/PM')
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%m/%d/%Y %H:%M %p")
    filtered_items = inbox.Items.Restrict(f"[ReceivedTime] >= '{yesterday}'")
    filtered_items.Sort("[ReceivedTime]", True)

    recipients = []

    for message in filtered_items:
        try:
            if "undeliverable" in message.Subject.lower():
                name, email = extract_email_and_name(message.Body)
                if email:
                    recipients.append({
                        "Name": name if name else "Unknown",
                        "Email": email
                    })
        except AttributeError:
            continue

    return recipients

def export_to_csv(data, filename="undeliverable_recipients.csv"):
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    filepath = os.path.join(desktop, filename)
    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["Name", "Email"])
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    print(f"Exported {len(data)} entries to '{filepath}'")

if __name__ == "__main__":
    failed_recipients = get_undeliverable_recipients_since_yesterday()
    export_to_csv(failed_recipients)