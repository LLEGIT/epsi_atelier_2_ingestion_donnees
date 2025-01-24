import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
if not ACCESS_TOKEN:
    raise ValueError("ACCESS_TOKEN not found in the .env file.")

GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json",
}

tables = [
    "issues",
    "pullRequests",
    "labels",
    "milestones",
    "releases",
    "deployments",
    "forks",
]

def get_table_fields(table_name):
    if table_name == "issues" or table_name == "pullRequests":
        return "{ title number url state createdAt updatedAt author { login } }"
    elif table_name == "labels":
        return "{ name color description }"
    elif table_name == "milestones":
        return "{ title description dueOn state number createdAt updatedAt }"
    elif table_name == "releases":
        return "{ name tagName createdAt description }"
    elif table_name == "deployments":
        return "{ id createdAt state environment description }"
    elif table_name == "forks":
        return "{ name owner { login } createdAt }"
    else:
        raise ValueError(f"Unknown table: {table_name}")

def generate_query(table_name, first=100, after=None):
    fields = get_table_fields(table_name)
    return f"""
    query {{
        repository(owner: "RocketChat", name: "Rocket.Chat") {{
            {table_name}(first: {first}, after: {after}) {{
                edges {{
                    node {fields}
                }}
                pageInfo {{
                    endCursor
                    hasNextPage
                }}
            }}
        }}
    }}
    """

def fetch_data_and_save_as_parquet(table_name, after=None, response_array=None):
    if response_array is None:
        response_array = []

    query = generate_query(table_name, first=100, after=f'"{after}"' if after else "null")
    response = requests.post(GITHUB_GRAPHQL_URL, headers=headers, json={"query": query})

    if response.status_code != 200:
        raise Exception(f"Query failed with status code {response.status_code}: {response.text}")

    data = response.json()
    if "errors" in data:
        raise Exception(f"GraphQL error: {data['errors']}")

    table_data = data["api_data"]["repository"][table_name]
    response_array.extend([edge["node"] for edge in table_data["edges"]])

    if table_data["pageInfo"]["hasNextPage"]:
        return fetch_data_and_save_as_parquet(table_name, after=table_data["pageInfo"]["endCursor"], response_array=response_array)

    df = pd.json_normalize(response_array)
    parquet_file_path = f"api_data/{table_name}.parquet"
    os.makedirs("api_data", exist_ok=True)
    df.to_parquet(parquet_file_path, engine="pyarrow")
    print(f"Data for {table_name} saved to {parquet_file_path}")

for table in tables:
    print(f"Fetching api_data for {table}...")
    try:
        fetch_data_and_save_as_parquet(table)
    except Exception as e:
        print(f"Failed to fetch api_data for {table}: {e}")
