from pathlib import Path
import csv
import json
from typing import List, Dict, Literal

case_headers: List[str] = []
meeting_headers: List[str] = [
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


def main():
    meetings = load_table(Path("../data/meetings_20210611.csv"), "meetings")
    # new_meetings: List[Dict] = []
    for m in meetings:
        if not m.get("files"):
            continue
        a_: List[Dict] = json.loads(m["agenda"])
        agenda: Dict[str, List] = {}
        for i in a_:
            i.pop("audio", None)

            agenda[str(i["number"])]
        agenda = {str(i["number"]): i for i in a_}

        files: List[Dict] = json.loads(m["files"])
        for d in files:
            if not d.get("agendaitem"):
                continue
            number = str(d.get("agendaitem", "0"))
            if number in agenda:
                if not agenda[number].get("audio"):
                    agenda[number]["audio"] = []
                agenda[number]["audio"].append(
                    {"filename": d["filename"], "href": d["href"]}
                )
        new_agenda = [v for k, v in agenda.items()]
        m["agenda"] = json.dumps(new_agenda, ensure_ascii=False)
        # if m["id"] == "11180":
        #     print(m["agenda"])

    with open("meetings_20210614.csv", "w", encoding="utf-8") as o:
        writer = csv.DictWriter(o, fieldnames=meeting_headers)
        for d in meetings:
            writer.writerow(d)


if __name__ == "__main__":
    main()
