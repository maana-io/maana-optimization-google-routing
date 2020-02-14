
import requests
import json

from query_1 import query_1

URL = "http://localhost:4000/graphql"


def test_query():
    query_input = {"query": query_1}
    response = requests.post(url=URL, json=query_input)
    response_content = json.loads(response.content)

    with open("response_1.json") as f:
        expected_response_content = json.load(f)

    assert(response_content == expected_response_content)

    # assert(data["data"]["routingSolverMakeSchedules"]["totalProfit"] == 383.0)
