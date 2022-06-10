import json


def read_json(filename, encoding="utf-8") -> json:
    with open(filename, encoding=encoding) as f:
        return json.load(f)
