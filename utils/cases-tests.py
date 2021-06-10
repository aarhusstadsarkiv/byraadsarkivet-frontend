from typing import Dict, List
import csv
import json

# import requests
# import time

"""
When viewing online cases, use:
.json?_shape=object&_json=metadata&_json=files&_json=decisions

"""

template: Dict = {
    "id": "int",
    "db_id": "int",
    "type": "str",
    "title": "str",
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

file_ = "../data/cases_20210428_v2.csv"


def main():
    # load current db.cases (no headers)
    cases: List[Dict] = []
    with open(file_, encoding="utf-8") as f:
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

    ###############################
    # Add all adhoc-items with same title
    # to the generated multi-decision adhocs
    ###############################
    duplicates: Dict[Dict[str, List]] = {}
    with open("adhoc_duplicates_title_based.json", encoding="utf-8") as i:
        duplicates = json.load(i)

    for d in cases:
        id_ = d["id"]
        title = d["title"]
        decisions = json.loads(d.get("decisions", []))

        if d.get("type") == "adhoc" and title in duplicates:
            if id_ not in duplicates[title]:
                duplicates[title][id_] = decisions

    with open("adhoc_duplicates_title_total.json", "w", encoding="utf-8") as o:
        json.dump(duplicates, o, ensure_ascii=False, indent=4)

    ###############################
    # Save all multi-meeting adhocs
    ###############################
    def common_meetings(new_decisions, data):
        new_tups = [(n.get("date"), n.get("fora_id")) for n in new_decisions]

        for id_, decisions in data.items():
            tups = [(d.get("date"), d.get("fora_id")) for d in decisions]
            if any(t in tups for t in new_tups):
                return True
        return False

    duplicate_adhocs = {}
    for d in cases:
        id_ = d["id"]
        title = d["title"]
        decisions = json.loads(d.get("decisions", []))
        length = len(decisions)

        # if d.get("type") == "adhoc" and length > 1:
        #     duplicate_adhocs[id_] = {"title": title, "decisions": decisions}

        # with open("adhoc_duplicates_basic.json", "w", encoding="utf-8") as o:
        #     json.dump(duplicate_adhocs, o, ensure_ascii=False, indent=4)

        if d.get("type") == "adhoc" and length > 1:

            if title not in duplicate_adhocs:
                duplicate_adhocs[title] = {id_: decisions}
            # elif common_meetings(decisions, duplicate_adhocs[title]):
            #     duplicate_adhocs[title][id_] = decisions
            else:
                duplicate_adhocs[title][id_] = decisions

            # cur_length = len(duplicate_adhocs[title].get("meetings"))
            # if length > cur_length:
            #     cur_ids: List[int] = duplicate_adhocs[title].get("ids", [])
            #     print(f"Working on {id_}")
            #     total_ids = cur_ids + [id_]
            #     duplicate_adhocs[title] = {
            #         "ids": total_ids,
            #         "length": length,
            #         "meetings": decisions,
            #     }

    with open("adhoc_duplicates_title_based.json", "w", encoding="utf-8") as o:
        json.dump(duplicate_adhocs, o, ensure_ascii=False, indent=4)

    ###############################
    ###############################
    # Needs to cater to this list (without nulls):
    #  58664, 58783, 58742, 58849, 58906
    # And this with nulls:
    #
    # adhocs = {}
    # for d in cases:
    #     ds_json = json.loads(d.get("decisions", []))
    #     ds_length = len(ds_json)

    #     if d.get("type") == "adhoc" and ds_length > 1:
    #         nulls = False
    #         for ds in ds_json:
    #             if not ds.get("meeting_id"):
    #                 nulls = True
    #                 break

    #         title = d["title"]
    #         # if nulls, something is wrong
    #         if nulls:
    #             new_entry = {
    #                 "id": d["id"],
    #                 "length": ds_length,
    #                 "dates": [ds.get("date") for ds in ds_json],
    #             }
    #             if title not in adhocs:
    #                 base = {"number_of_meetings": ds_length}
    #                 adhocs[title] = []

    #             # new_list = adhocs.get(title, []).append(new_entry)
    #             adhocs[title].append(new_entry)

    # for k, v in adhocs.items():
    #     print(f"{k}:")
    #     print(f"{v}")

    # with open("adhoc-duplicates.json", "w", encoding="utf-8") as o:
    #     json.dump(adhocs, o, ensure_ascii=False, indent=4)

    ########################################
    # Test for multiple refs to same case_id
    ########################################
    # for d in cases:
    #     id_ = d["id"]

    # type_ = d["type"]
    # if type_ == "indstilling":
    #     decisions: List[Dict] = json.loads(d["decisions"])
    #     decision_set: List[str] = []
    #     for i in decisions:
    #         if i in decision_set:
    #             print(f"Multiple decisions in case {d['id']}")
    #         else:
    #             decision_set.append(i)

    ############################################
    # Test for multiple files with same filename
    ############################################
    # def compare_length(case: int, files: Dict[str, List[str]]):
    #     lengths = []
    #     for k, v in files.items():
    #         for url in v:
    #             r = requests.head(url)
    #             length = r.headers.get("Content-Length")
    #             if not length:
    #                 print(f"{case}. No content-length for {k}: {url}")
    #             elif length in lengths:
    #                 print(f"{case} has duplicate files: {k}")
    #                 lengths.append(length)
    #             else:
    #                 lengths.append(length)

    # if d.get("files") and d["files"] != "null":
    #     files = {}
    #     for f in json.loads(d["files"]):
    #         r = requests.head(f["href"])
    #         length = r.headers.get("Content-Length")
    #         if not length:
    #             print(
    #                 f"{id_}. No content-length: \
    #                     {f['filename']}: {f['href']}"
    #             )
    #             time.sleep(0.05)
    # duplicates = False
    # for i in json.loads(d["files"]):
    #     name = i["filename"]
    #     if name in files:
    #         duplicates = True
    #         files[name].append(i["href"])
    #     else:
    #         files[name] =[i["href"]]
    # if duplicates:
    #     compare_length(id_, files)

    ############################
    # Test for similar textblobs
    ############################
    # title = d.get("title")
    # resume = d.get("resume")
    # subtitle = d.get("subtitle")
    # presentation = d.get("presentation")
    # notes = d.get("notes")

    # if title:
    #     if subtitle and subtitle == title:
    #         print(f"Similar titls/subtitle in case: {id_}")
    #     if resume and resume == title == title:
    #         print(f"Similar title/resume in case: {id_}")
    #     if presentation and presentation == title:
    #         print(f"Similar title/presentation in case: {id_}")
    #     if notes and notes == title:
    #         print(f"Similar title/notes in case: {id_}")
    # if resume:
    #     if subtitle and subtitle == resume:
    #         print(f"Similar resume/subtitle in case: {id_}")
    #     if presentation and presentation == resume:
    #         print(f"Similar resume/presentation in case: {id_}")
    #     if notes and notes == resume:
    #         print(f"Similar resume/notes in case: {id_}")
    # if subtitle:
    #     if presentation and presentation == subtitle:
    #         print(f"Similar subtitle/presentation in case: {id_}")
    #     if notes and notes == subtitle:
    #         print(f"Similar subtitle/notes in case: {id_}")
    # if presentation:
    #     if notes and notes == presentation:
    #         print(f"Similar presentation/notes in case: {id_}")


if __name__ == "__main__":
    main()
