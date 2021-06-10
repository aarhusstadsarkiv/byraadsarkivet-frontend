from typing import Dict, List
import csv
import json

"""
When viewing online meetings, use:
.json?_shape=object&_json=agenda&_json=metadata&_json=files

"""

template: Dict = {
    "id": "int",
    "fora_id": "int",
    "fora_name": "str",
    "year": "int",
    "date": "str",
    "title": "str",
    "public": "bool",
    "agenda": {
        "number": "int",
        "public": "bool",
        "sender": "str",
        "title": "str",
        "type": "indstilling/adhoc",
        "id": "int",
    },
    "metadata": {
        "original_id": "str",
        "time_of_meeting": "str",
        "place_of_meeting": "str",
        "agenda_type": "str",
        "notes": "str",
    },
    "files": {
        "filename": "str",
        "href": "url",
        "agendaitem": "int",
        "ordering": "int",
    },
}

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


def main():
    # load current db.cases (no headers)
    cases: List[Dict] = []
    with open("../data/cases_20210507.csv", encoding="utf-8") as f:
        rows = csv.DictReader(
            f,
            fieldnames=case_headers,
        )
        for r in rows:
            cases.append(r)
    # load current db.meetings (no headers)
    meetings: List[Dict] = []
    with open("../data/meetings_20210507.csv", encoding="utf-8") as f:
        rows = csv.DictReader(
            f,
            fieldnames=meeting_headers,
        )
        for r in rows:
            meetings.append(r)

    ############################################
    # List all cases not references in a meeting
    ############################################
    refs = []
    out_meetings = []
    for m in meetings:
        agenda: List[Dict] = json.loads(m["agenda"])
        new_agenda = []
        for i in agenda:
            if i.get("id"):
                refs.append(int(i["id"]))
            else:
                print(f"Meeting: {m['id']}. Agendaitem missing id.")

            new_agendaitem = {}
            for k, v in i.items():
                if v:
                    new_agendaitem[k] = v
            new_agenda.append(new_agendaitem)

        new_metadata = {}
        for k, v in json.loads(m["metadata"]).items():
            if v:
                new_metadata[k] = v
        m["agenda"] = json.dumps(new_agenda, ensure_ascii=False)
        m["metadata"] = json.dumps(new_metadata, ensure_ascii=False)
        out_meetings.append(m)

    with open("meetings_20210517.csv", "w", encoding="utf-8") as o:
        writer = csv.DictWriter(o, fieldnames=meeting_headers)
        for d in out_meetings:
            writer.writerow(d)

    out_cases = []
    for c in cases:
        # Not referenced in any meetings. Should be deleted
        if int(c["id"]) not in refs and (c["type"] == "record"):
            continue
        else:
            out_cases.append(c)

    # Save total meetings to csv, ready for import to db
    with open("cases_20210517.csv", "w", encoding="utf-8") as o:
        writer = csv.DictWriter(o, fieldnames=case_headers)
        for d in out_cases:
            writer.writerow(d)

    # for m in meetings:
    #     agenda: List[Dict] = json.loads(m["agenda"])
    #     # case_ids: List[int] = []
    #     # item_title: List[str] = []
    #     item_number: List[str] = []
    #     for i in agenda:
    ########################################
    # Test for multiple refs to same case_id
    ########################################
    # if int(i["id"]) in case_ids:
    #     print(f"Multiple case_refs in meeting {m['id']}: {i['id']}")
    # else:
    #     case_ids.append(int(i["id"]))

    # test for similar titles
    # if i["title"] in item_title:
    #     print(f"Similar titles in meeting {m['id']}: {i['title']}")
    # else:
    #     item_title.append(i["title"])

    ######################################################
    # Test for multiple agendaitem numbers, excluding zero
    ######################################################
    # number = i["number"]
    # if number in item_number and int(number) > 0:
    #     print(
    #         f"Similar numbers in meeting {m['id']}: \
    #         {number} ({m['fora_name']})"
    #     )
    # else:
    #     item_number.append(number)


if __name__ == "__main__":
    main()
