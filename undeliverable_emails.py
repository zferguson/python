import win32com.client
import re
import os
from datetime import datetime, timedelta
import pandas as pd

def extract_from_embedded_msg(message):
    """
    Try to extract 'From' and 'To' from embedded message in the undeliverable notice.
    """
    for attachment in message.Attachments:
        if attachment.Type == 6:  # olEmbeddeditem
            try:
                embedded = attachment.EmbeddedMsg
                sender = embedded.SenderEmailAddress or embedded.SenderName
                recipients = [r.Address for r in embedded.Recipients]
                return [(sender, r) for r in recipients if r]
            except Exception:
                continue
    return []

def extract_from_body(body):
    """
    Fallback to regex-based extraction if no embedded message exists.
    """
    # Try to extract both name and email from lines like: "Your message to John Doe <john@example.com>"
    match = re.search(r'to\s+.*?<([\w\.-]+@[\w\.-]+)>', body, re.IGNORECASE)
    if match:
        return [("Unknown", match.group(1).strip())]
    
    # Fallback: just extract one email address
    match = re.search(r'[\w\.-]+@[\w\.-]+', body)
    if match:
        return [("Unknown", match.group().strip())]
    
    return []

def get_failed_deliveries_since_yesterday():
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6)
    messages = inbox.Items
    messages.Sort("[ReceivedTime]", True)

    cutoff = datetime.now() - timedelta(days=1)
    failed_pairs = set()

    for msg in messages:
        try:
            received_time = msg.ReceivedTime
            if hasattr(received_time, "tzinfo") and received_time.tzinfo is not None:
                received_time = received_time.replace(tzinfo=None)

            if received_time < cutoff:
                break  # Inbox is sorted descending

            subject = msg.Subject.lower()
            if "undeliverable" in subject or "delivery" in subject:
                extracted = extract_from_embedded_msg(msg)
                if not extracted:
                    extracted = extract_from_body(msg.Body or msg.HTMLBody or "")

                for from_email, to_email in extracted:
                    failed_pairs.add((from_email.lower(), to_email.lower()))
        except Exception:
            continue

    return sorted(failed_pairs)

def export_failed_emails_to_csv(pairs, filename="undeliverable_recipients.csv"):
    df = pd.DataFrame(pairs, columns=["From", "To"])
    desktop = os.path.join(os.path.expanduser("~"), "Desktop", filename)
    df.to_csv(desktop, index=False)
    print(f"Exported {len(df)} unique failure pairs to {desktop}")

if __name__ == "__main__":
    failures = get_failed_deliveries_since_yesterday()
    export_failed_emails_to_csv(failures)