import re

def find_phone_numbers(text):
    # define a regex pattern for phone numbers
    phone_number_pattern = re.compile(
        r'\+?\d{1,3}[-.\s]?\(?\d{1,4}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}'
    )
    
    # find all matches in the input text
    matches = phone_number_pattern.findall(text)
    
    return matches

# example
text = """
Call me at (123) 456-7890 or 123-456-7890. My office number is 123.456.7890.
You can also reach me at +31636363634 or +3(123)123-12-12.
"""

phone_numbers = find_phone_numbers(text)

print(phone_numbers)
