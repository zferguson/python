import pandas as pd

def flatten_dict_or_list(d, parent_key = '', sep = '.'):
    items = []
    for k, v in d.items() if isinstance(d, dict) else enumerate(d):
        new_key = parent_key + sep + str(k) if parent_key else str(k)
        if isinstance(v, dict):
            items.extend(flatten_dict_or_list(v, new_key, sep = sep).items())
        elif isinstance(v, list):
            items.extend(flatten_dict_or_list(v, new_key, sep = sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def parse_to_dataframe(d, sep = '.'):
    flat_dict = flatten_dict_or_list(d, sep = sep)
    return pd.DataFrame([flat_dict])

test = {
    "person": {
        "name": "John Doe",
        "age": 30,
        "address": {
            "street": "123 Main St",
            "city": "Anytown",
            "state": "CA",
            "zip": "12345"
        },
        "holdings": {
            "holding_id": 1,
            "holding": {
                "symbol": "AAPL",
                "amount": 50000,
                "purchase": '2022-01-01'
            }
        }
    }
}

nested_dict = {'a': 1, 'b': {'c': [2, 3, {'d': 4}]}}

df = parse_to_dataframe(test)

print(df)
