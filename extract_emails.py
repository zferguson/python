import os
import re
import extract_msg

def extract_first_email_from_body(msg_path):
    """Extract the first email address found in the body of a .msg file."""
    try:
        msg = extract_msg.Message(msg_path)
        msg_body = msg.body or ""
        match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', msg_body)
        return match.group(0) if match else None
    except Exception as e:
        print(f"Error processing {msg_path}: {e}")
        return None

def process_msg_files(directory):
    """Iterate through all .msg files in the directory and extract email addresses."""
    results = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.msg'):
                full_path = os.path.join(root, file)
                email = extract_first_email_from_body(full_path)
                results[full_path] = email
    return results

# Replace with the path to your folder containing .msg files
msg_directory = r'C:\path\to\your\msg_files'
emails_found = process_msg_files(msg_directory)

# Print the results
for filepath, email in emails_found.items():
    print(f"{filepath}: {email}")