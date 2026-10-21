import json, os

_DATA_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'processed', 'docs.json')

def get_doc(key: str):
    with open(_DATA_FILE) as f:
        docs = json.load(f)
    name = key.replace('quickcart::', '')
    if name not in docs:
        raise KeyError(f"{key} not found in docs.json")
    return docs[name]
