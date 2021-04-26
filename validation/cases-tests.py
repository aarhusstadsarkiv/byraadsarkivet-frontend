from typing import Dict, List
import csv
import json

"""
When viewing online cases, use ".json?_shape=object&_json=metadata&_json=files&_json=decisions"
"""

template: Dict = {
    "id": "int",
    "db_id": "int",
    "type": "str",
    "title": "int",
    "public": "bool",
    "date": "str",
    "last_deliberation_date": "str",
    "year": "int",
    "subtitle": "str",
    "resume": "str",
    "suggestion": "str",
    "presentation": "str",
    "notes": "str",
    "fora": "str",
    "decisions": {
        "original_id": "str",
        "public": "bool",
        "date": "str",
        "title": "str",
        "fora_name": "",
        "id": "int",
        "fora_id": "int",
        "meeting_id": "int",
        "meeting_original_id": "str",
    },
    "files": {
        "filename": "str",
        "href": "url",
        "agendaitem": "int",
        "ordering": "int",
    },
    "metadata": {
        "original_id": "str",
        "time_of_meeting": "str",
        "place_of_meeting": "str",
        "agenda_type": "str",
        "notes": "str",
    },
}

file = "../data/cases_table_20210412.csv"

def main():
    # load current db.cases (no headers)
    cases: List[List] = []
    with open(file, encoding="utf-8") as f:
        rows = csv.DictReader(
            f,
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
            ],
        )
        for r in rows:
            cases.append(r)

    # TEST 1. Which cases have multiple refs to same case_id
    for d in cases:
        id_ = d["id"]
        type_ = d["type"]
        if type_ == "indstilling":
            decisions: List[Dict] = json.loads(d["decisions"])

            ########################################
            # Test for multiple refs to same case_id
            ########################################
            # decision_set: List[str] = []
            # for i in decisions:
                # if i in decision_set:
                #     print(f"Multiple decisions in case {d['id']}")
                # else:
                #     decision_set.append(i)


        ############################
        # Test for similar textblobs
        ############################
        title = d.get("title")
        resume = d.get("resume")
        subtitle = d.get("subtitle")
        presentation = d.get("presentation")
        notes = d.get("notes")

        if title:
            if subtitle and subtitle == title:
                print(f"Similar titls/subtitle in case: {id_}")
            if resume and resume == title == title:
                print(f"Similar title/resume in case: {id_}")
            if presentation and presentation == title:
                print(f"Similar title/presentation in case: {id_}")
            if notes and notes == title:
                print(f"Similar title/notes in case: {id_}")                
        if resume:
            if subtitle and subtitle == resume:
                print(f"Similar resume/subtitle in case: {id_}")
            if presentation and presentation == resume:
                print(f"Similar resume/presentation in case: {id_}")
            if notes and notes == resume:
                print(f"Similar resume/notes in case: {id_}")
        if subtitle:
            if presentation and presentation == subtitle:
                print(f"Similar subtitle/presentation in case: {id_}")
            if notes and notes == subtitle:
                print(f"Similar subtitle/notes in case: {id_}")
        if presentation:
            if notes and notes == presentation:
                print(f"Similar presentation/notes in case: {id_}")

if __name__ == "__main__":
    main()
