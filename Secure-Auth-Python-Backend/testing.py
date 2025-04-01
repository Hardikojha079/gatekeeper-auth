import psycopg2
conn = psycopg2.connect(
    host="localhost",
    dbname="DB",
    user="postgres",
    password="<Your_Password>",
    port=5432
)
print("Connection successful!")