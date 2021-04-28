import csv
from typing import List, Dict, Literal
from pathlib import Path

csv_file = Path("../data/cases_table_20210427.csv")

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
        table_data = [row for row in reader]
    return table_data
