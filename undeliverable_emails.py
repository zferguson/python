import win32com.client
import re
import csv
import os

def extract_email_and_name(body):
    """
    Extracts recipient name and email address from undeliverable message body.
    """
    match = re.search(r'to\s+(.+?)\s+<(.+?)>', body, re.IGNORECASE)
    if match:
        name, email = match.groups()
        return name.strip(), email.strip()

    match = re.search(r'[\w\.-]+@[\w\.-]+', body)
    if match:
        return None, match.group().strip()

    return None, None

def get_undeliverable_recipients():
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6)
    messages = inbox.Items
    messages.Sort("[ReceivedTime]", True)

    recipients = []

    for message in messages:
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
    failed_recipients = get_undeliverable_recipients()
    export_to_csv(failed_recipients)