from typing import List, Dict, Literal
import csv
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
            table_data.append(row)
    return table_data


def main():
    cases = load_table(Path("../data/cases_table_20210427.csv"), "cases")
    cases2 = load_table(Path("../data/cases_table_20210427_v2.csv"), "cases")

    for i in range(0, 10):
        if cases[i] != cases2[i]:
            print(cases[i])
            print(type(cases[i]["metadata"]))
            print(cases2[i])
            print("\n")


if __name__ == "__main__":
    main()
