# https://docs.locust.io/en/stable/index.html

import time
import random
from locust import HttpUser, task, between


queries = [
    "helhedsplan",
    "aarhus",
    "gellerup",
    "hjortshøj",
    "hjortshøj-egå",
    "aarhus havn",
    "byrådet",
    "legepladser",
    "byggesag miljø",
    "skæring",
    "letbanen etape",
    "lokalplan",
    "risskov gymnasium",
    "aarhus teater",
    "godsbanen anlæg",
]


class CuriousUser(HttpUser):
    wait_time = between(1, 2)

    @task(10)
    def homepage(self):
        self.client.get("/")

    @task(8)
    def search_cases(self):
        max_idx = len(queries) - 1
        for i in range(5):
            q = queries[random.randint(0, max_idx)]
            self.client.get(f"/db/cases?_search={q}", name="Search cases")
            time.sleep(1)

    @task(7)
    def view_meeting_list(self):
        for item_id in [13, 20, 19]:
            year = random.randint(2017, 2020)
            self.client.get(
                f"/db/meetings?fora_id={item_id}&year={year}",
                name="List of meetings",
            )
            time.sleep(1)

    @task(4)
    def view_meeting(self):
        for meeting_id in random.sample(range(0, 6500), 6):
            with self.client.get(
                f"/db/meetings/{meeting_id}",
                name="Single meeting",
                catch_response=True,
            ) as r:
                if r.status_code == 404:
                    r.success()

    @task(9)
    def view_case(self):
        for case_id in random.sample(range(0, 20000), 20):
            with self.client.get(
                f"/db/cases/{case_id}", name="Single case", catch_response=True
            ) as r:
                if r.status_code == 404:
                    r.success()

    @task(3)
    def search_casetitles(self):
        max_idx = len(queries) - 1
        for i in range(5):
            q = queries[random.randint(0, max_idx)]
            self.client.get(
                f"/db/cases?_search_title={q}", name="Search casetitles"
            )
            time.sleep(1)
