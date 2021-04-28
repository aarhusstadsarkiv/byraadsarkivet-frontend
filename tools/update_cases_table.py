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
        if (
            f.is_file()
            and f.stem.startswith(case_id)
            and f.suffix == ".json"
        ):
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
    cases_to_update = ["52210", "59260"]
    cases = load_table(Path("../data/cases_table_20210427.csv"), "cases")

    new_table = Path("../data/cases_table_20210427_v2.csv")
    with open(new_table, "w", encoding="utf-8", newline="") as o:
        writer = csv.DictWriter(o, fieldnames=case_headers)
        for case in cases:
            if case["id"] in cases_to_update:
                json_strings = updated_json_values(case["id"])
                case["decisions"] = json_strings.get("decisions")
                case["files"] = json_strings.get("files")
                case["metadata"] = json_strings.get("metadata")
            # new_case: Dict = remove_empty_subvalues(case)
            writer.writerow(case)


if __name__ == "__main__":
    main()
