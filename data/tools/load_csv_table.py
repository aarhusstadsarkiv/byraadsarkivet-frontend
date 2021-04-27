import csv
from typing import List, Dict
from pathlib import Path

csv_file = Path("../data/cases_table_20210427.csv")
fieldnames=[
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

def main():
    table_data: List[Dict] = []
    with open(csv_file, encoding="utf-8") as i:
        table_data = csv.DictReader(i, fieldnames=fieldnames)

if __name__ == "__main__":
    main()