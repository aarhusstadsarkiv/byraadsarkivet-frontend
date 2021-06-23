from collections import deque
from pathlib import Path
import csv


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


def largest_substring_algo1(string):
    list_ = list(string)
    d = deque(string[1:])
    match = []
    longest_match = []
    while d:
        for i, item in enumerate(d):
            if list_[i] == item:
                match.append(item)
            else:
                if len(longest_match) < len(match):
                    longest_match = match
                match = []
        d.popleft()
    return "".join(longest_match)


if __name__ == "__main__":

    with open(Path("../data/cases_20210615_v2.csv"), encoding="utf-8") as i:
        reader = csv.DictReader(i, fieldnames=case_headers)
        fields = ["notes", "presentation", "subtitle", "resume", "suggestion"]
        for row in reader:
            for field in fields:
                substring = largest_substring_algo1(row.get(field, ""))
                if len(substring.split()) > 25:
                    print(
                        f"Case: {row['id']}. Col: {field}. Text: {substring}"
                    )
