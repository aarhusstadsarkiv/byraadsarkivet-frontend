from typing import List, Dict, Literal
import csv
import json
from pathlib import Path

case_headers = [
    "id",
    "db_id",
    "type",
    "title",
    "public",
    "date",
    "last_deliberation_date",
    "year",
    "subtitle",
    "resume",
    "suggestion",
    "presentation",
    "notes",
    "fora",
    "decisions",
    "files",
    "metadata",
]

meeting_headers = [
    "id",
    "fora_id",
    "fora_name",
    "year",
    "date",
    "title",
    "public",
    "agenda",
    "metadata",
    "files",
]


def load_table(
    csv_table: Path, table: Literal["cases", "meetings"]
) -> List[Dict]:

    fields: List[str] = case_headers if table == "cases" else meeting_headers
    table_data: List[Dict] = []
    with open(csv_table, encoding="utf-8") as i:
        reader = csv.DictReader(i, fieldnames=fields)
        for row in reader:
            if row.get("decisions"):
                row["decisions"] = json.loads(row["decisions"])
            if row.get("files"):
                row["files"] = json.loads(row["files"])
            if row.get("metadata"):
                row["metadata"] = json.loads(row["metadata"])
            table_data.append(row)
    return table_data


# fetch all json-encoded columns of a given case (decisions, files, metadata)
# return as strings in dict
def updated_json_values(case_id: str) -> Dict[str, str]:
    out: Dict = {}
    for f in Path("../temp/").iterdir():
        if f.is_file() and f.stem.startswith(case_id) and f.suffix == ".json":
            print(f"found file {f.name}")
            key = f.stem.split("_")[1]
            with open(f, encoding="utf-8") as i:
                value = json.load(i)
                out[key] = json.dumps(value, ensure_ascii=False)
    return out


def remove_empty_subvalues(case: Dict) -> Dict:
    out: Dict = {}
    for key, val in case.items():
        if key in ["decisions", "files"] and val is not None:
            l: List[Dict] = []
            for dict_ in val:
                l.append({k: v for k, v in dict_.items() if v is not None})
            out[key] = l
        elif key == "metadata" and val is not None:
            d = {k: v for k, v in val.items() if v is not None}
            out[key] = d
        else:
            out[key] = val
    return out


def main():
    cases = load_table(Path("../data/cases_20210615_v2.csv"), "cases")

    for case in cases:
        # if case.get("files"):
        #     new_files = []
        #     for f in case.get("files"):
        #         new_file = {}
        #         for k, v in f.items():
        #             if v == "null" or v is None:
        #                 f.pop(k, None)
        #                 print(f"popped {k} from files in {case['id']}")
        #             else:
        #                 new_file[k] = v
        #         new_files.append(new_file)
        #     case["files"] = json.dumps(new_files, ensure_ascii=False)

        if case.get("decisions"):
            new_decisions = []
            for f in case.get("decisions"):
                new_decision = {}
                for k, v in f.items():
                    if v == "null" or v is None:
                        print(f"popped {k} from decision in {case['id']}")
                        continue
                    if type(v) == "str":
                        v = str(v).strip()
                    new_decision[k] = v
                new_decisions.append(new_decision)
            case["decisions"] = json.dumps(new_decisions, ensure_ascii=False)

        # if case.get("metadata"):
        #     new_metadata = {}
        #     for k, v in case["metadata"].items():
        #         if v == "null" or v is None:
        #             f.pop(k, None)
        #             print(f"popped {k} from metadata in {case['id']}")
        #         else:
        #             new_metadata[k] = v
        #     case["metadata"] = json.dumps(new_metadata, ensure_ascii=False)

    with open(
        Path("../data/cases_20210615_v3.csv"),
        "w",
        encoding="utf-8",
        newline="",
    ) as o:
        writer = csv.DictWriter(o, fieldnames=case_headers)
        for case in cases:
            writer.writerow(case)


if __name__ == "__main__":
    main()
