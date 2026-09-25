import json
import psycopg
from pgvector.psycopg import register_vector

INPUT_FILE = "data/embedded_chunks.json"

conn = psycopg.connect(
    host="localhost",
    port=5433,
    dbname="abpmjay",
    user="abpmjay",
    password="abpmjay_dev"
)

register_vector(conn)

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    chunks = json.load(file)

with conn.cursor() as cursor:
    for chunk in chunks:
        metadata = chunk["metadata"]

        cursor.execute(
            """
            INSERT INTO knowledge_chunks
            (text, source, document, version, page, embedding)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                chunk["text"],
                metadata["source"],
                metadata["document"],
                metadata["version"],
                metadata["page"],
                chunk["embedding"]
            )
        )

conn.commit()
print(f"Loaded {len(chunks)} chunks into PostgreSQL.")

conn.close()