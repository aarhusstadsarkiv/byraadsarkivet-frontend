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
        if ".mp3" not in m.get("files"):
            continue

        files: List[Dict] = json.loads(m["files"])
        preserve: List[Dict] = []
        a_: List[Dict] = json.loads(m["agenda"])
        agenda: Dict[str, List] = {}

        # pop existing audio-keys
        for i in a_:
            i.pop("audio", None)
            number = str(i["number"])
            if number in agenda:
                print(f"More than one agendaitem with same number {m['id']}")
            agenda[number] = i

        for d in files:
            if any(
                t in str(d.get("filename")).lower()
                for t in ["gennemgang af", "forretningsorden"]
            ):
                preserve.append(
                    {
                        "filetype": "audio",
                        "filename": d["filename"],
                        "href": d["href"],
                        "ordering": int(d.get("ordering", 0)),
                    }
                )
                continue

            number = str(d.get("agendaitem", "0"))
            if number in agenda:
                agendaitem: Dict = agenda[number]
                if not agendaitem.get("audio"):
                    agendaitem["audio"] = []
                agendaitem["audio"].append(
                    {"filename": d["filename"], "href": d["href"]}
                )
                agenda[number] = agendaitem

        new_agenda = [v for k, v in agenda.items()]
        m["agenda"] = json.dumps(new_agenda, ensure_ascii=False)
        if preserve:
            m["files"] = json.dumps(preserve, ensure_ascii=False)
        else:
            m.pop("files", None)
        # if m["id"] == "11180":
        #     print(m["agenda"])

    with open("../data/meetings_20210615_v2.csv", "w", encoding="utf-8") as o:
        writer = csv.DictWriter(o, fieldnames=meeting_headers)
        for d in meetings:
            writer.writerow(d)


if __name__ == "__main__":
    main()
