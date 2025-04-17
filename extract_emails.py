import os
import re
import extract_msg
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

def extract_first_email_from_body(msg_path):
    """Extract the first email address found in the body of a .msg file."""
    try:
        msg = extract_msg.Message(msg_path)
        msg_body = msg.body or ""
        match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', msg_body)
        return msg_path, match.group(0) if match else None
    except Exception as e:
        return msg_path, f"Error: {e}"

def collect_msg_files(directory):
    """Collect all .msg file paths from a directory recursively."""
    msg_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.msg'):
                msg_files.append(os.path.join(root, file))
    return msg_files

def process_files_parallel(file_paths, max_workers=8):
    """Process .msg files in parallel using ThreadPoolExecutor."""
    results = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(extract_first_email_from_body, path): path for path in file_paths}
        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing"):
            path, email = future.result()
            results[path] = email
    return results

# Set your directory here
msg_directory = r'C:\path\to\your\msg_files'

if __name__ == "__main__":
    all_msg_files = collect_msg_files(msg_directory)
    extracted_emails = process_files_parallel(all_msg_files, max_workers=8)

    # Print or save results
    for path, email in extracted_emails.items():
        print(f"{path}: {email}")