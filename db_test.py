import psycopg

conn = psycopg.connect(
    host="localhost",
    port=5433,
    dbname="abpmjay",
    user="abpmjay",
    password="abpmjay_dev"
)
print("Connected to PostgreSQL!")

conn.close()