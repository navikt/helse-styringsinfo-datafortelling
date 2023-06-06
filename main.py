from google.cloud import bigquery

client = bigquery.Client()

QUERY = """--sql
SELECT dato, verdi FROM `tbd-dev-7ff9.hvilepuls.styringsinformasjon`
"""

query_job = client.query(QUERY)
rows = query_job.result()

for row in rows:
    print(row.values[0], row.values[1])
