from typing import Dict, List
import csv
import json

"""
When viewing online meetings, use ".json?_shape=object&_json=agenda&_json=metadata&_json=files"
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


def main():
    # load current db.meetings (no headers)
    meetings: List[List] = []
    with open("../data/meetings_table_20210426.csv", encoding="utf-8") as f:
        rows = csv.DictReader(
            f,
            fieldnames=[
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
            ],
        )
        for r in rows:
            meetings.append(r)

    # TEST 1. Which meetings have multiple refs to same case_id
    for m in meetings:
        try:
            agenda: List[Dict] = json.loads(m["agenda"])
        except KeyError as e:
            print(f"This meeting has no agenda: {m['id']}")
        case_ids: List[str] = []
        item_title: List[str] = []
        item_number: List[str] = []
        for i in agenda:
            ########################################
            # Test for multiple refs to same case_id
            ########################################
            # if i["id"] in case_ids:
            #     print(f"Multiple case_refs in meeting {m['id']}: {i['id']}")
            # else:
            #     case_ids.append(i["id"])

            # test for similar titles
            # if i["title"] in item_title:
            #     print(f"Similar titles in meeting {m['id']}: {i['title']}")
            # else:
            #     item_title.append(i["title"])

            # test for multiple agendaitem numbers, excluding zero
            number = i["number"]
            if number in item_number and int(number) > 0:
                print(f"Similar numbers in meeting {m['id']}: {number} ({m['fora_name']})")
            else:
                item_number.append(number)


if __name__ == "__main__":
    main()
