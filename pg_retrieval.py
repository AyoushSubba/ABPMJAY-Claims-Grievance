from sentence_transformers import SentenceTransformer
import psycopg
from pgvector.psycopg import register_vector


# Load the embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


# User's search query
query = "What happens if my grievance is not resolved on time?"


# Convert the query into a 384-dimensional vector
query_embedding = model.encode(query)


# Connect to PostgreSQL
conn = psycopg.connect(
    host="localhost",
    port=5433,
    dbname="abpmjay",
    user="abpmjay",
    password="abpmjay_dev"
)

# Enable pgvector support for this connection
register_vector(conn)


# Search for the most similar chunks
with conn.cursor() as cursor:

    cursor.execute(
        """
        SELECT
            id,
            text,
            source,
            document,
            version,
            page,
            1 - (embedding <=> %s) AS similarity
        FROM knowledge_chunks
        ORDER BY embedding <=> %s
        LIMIT %s
        """,
        (
            query_embedding,
            query_embedding,
            5
        )
    )

    results = cursor.fetchall()


# Display the results
print("\nTop 5 Retrieved Chunks:\n")

for result in results:

    chunk_id, text, source, document, version, page, similarity = result

    print(f"Chunk ID: {chunk_id}")
    print(f"Page: {page}")
    print(f"Similarity: {similarity:.4f}")
    print(f"Text: {text[:300]}")
    print("-" * 60)


conn.close()