from duckdb import connect
from sys import argv


def fetch_table():
    database_file = 'database.duckdb'
    con = connect(database=database_file, read_only=False)

    correct_tables = ['deployments', 'forks', 'issues', 'labels', 'milestones', 'pullRequests', 'releases']
    chosen_table = argv[1] if (len(argv) > 1 and argv[1]) else 'deployments'
    limit = argv[2] if (len(argv) > 2 and argv[2]) else 10

    query = f"SELECT * FROM {chosen_table} LIMIT {limit}"
    result = con.execute(query).fetchdf()

    # Close the connection
    con.close()

    print(result)


fetch_table()
