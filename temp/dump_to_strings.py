import json
from pathlib import Path

if __name__ == "__main__":

    for f in Path(".").iterdir():
        if f.is_file() and f.suffix == ".json":
            with open(f, encoding="utf-8") as fi:
                data = json.load(fi)
                print(f.name)
                print(json.dumps(data, ensure_ascii=False))
