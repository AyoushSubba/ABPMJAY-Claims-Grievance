import json 
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

input_file="data/embedded_chunks.json"
model=SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
with open(input_file, "r") as f:
    chunks=json.load(f)

query="What happens if my grievance is not resolved on time?"

query_embedding=model.encode(query)

for chunk in chunks:
    chunk_embedding=chunk["embedding"]

    similarity=cosine_similarity(
        [query_embedding],
        [chunk_embedding]
    )
    print("This is the similarity ok!!!",similarity)
    chunk["similarity"]=similarity

chunks.sort(
    key=lambda chunk: chunk["similarity"],
    reverse=True
)
# Display top 5
print("\nTop 5 Relevant Chunks\n")

for i, chunk in enumerate(chunks[:5], start=1):

    print(f"--- Result {i} ---")
    print("Similarity:", chunk["similarity"])
    print("Page:", chunk["metadata"]["page"])
    print("Text:")
    print(chunk["text"][:700])
    print()