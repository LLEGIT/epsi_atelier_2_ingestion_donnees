import duckdb
from pandas import read_parquet

# Load Parquet files into Pandas DataFrames
deployments_file = read_parquet('./data/deployments.parquet')
forks_file = read_parquet('./data/forks.parquet')
issues_file = read_parquet('./data/issues.parquet')
labels_file = read_parquet('./data/labels.parquet')
milestones_file = read_parquet('./data/milestones.parquet')
pull_requests_file = read_parquet('./data/pullRequests.parquet')
releases_file = read_parquet('./data/releases.parquet')

# Create a DuckDB connection
database_file = 'database.duckdb'
con = duckdb.connect(database=database_file, read_only=False)

# Register the Pandas DataFrames as virtual tables
con.register('deployments', deployments_file)
con.register('forks', forks_file)
con.register('issues', issues_file)
con.register('labels', labels_file)
con.register('milestones', milestones_file)
con.register('pull_requests', pull_requests_file)
con.register('releases', releases_file)

# Create persistent tables in DuckDB from the registered virtual tables
con.execute("CREATE TABLE deployments AS SELECT * FROM deployments")
con.execute("CREATE TABLE forks AS SELECT * FROM forks")
con.execute("CREATE TABLE issues AS SELECT * FROM issues")
con.execute("CREATE TABLE labels AS SELECT * FROM labels")
con.execute("CREATE TABLE milestones AS SELECT * FROM milestones")
con.execute("CREATE TABLE pull_requests AS SELECT * FROM pull_requests")
con.execute("CREATE TABLE releases AS SELECT * FROM releases")

# Query the data to confirm the table is created successfully
result = con.execute("SELECT * FROM issues").fetchdf()
print(result.head())

# Close the connection
con.close()
