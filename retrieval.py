import json 
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

input_file="data/embedded_chunks.json"
model=SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
with open(input_file, "r") as f:
    chunks=json.load(f)


def retrieve(query, top_k=5):
    query_embedding = model.encode(query)

    for chunk in chunks:
        chunk_embedding = chunk["embedding"]

        similarity = cosine_similarity(
            [query_embedding],
            [chunk_embedding]
        )[0][0]

        chunk["similarity"] = similarity

    ranked_chunks = sorted(
        chunks,
        key=lambda chunk: chunk["similarity"],
        reverse=True
    )

    return ranked_chunks[:top_k]

query=input("Enter Your Query: ")
results=retrieve(query)
# Display top 5
print("\nTop 5 Relevant Chunks\n")

for i, chunk in enumerate(results, start=1):

    print(f"--- Result {i} ---")
    print("Similarity:", chunk["similarity"])
    print("Page:", chunk["metadata"]["page"])
    print("Text:")
    print(chunk["text"][:700])
    print()