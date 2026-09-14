import json 
from sentence_transformers import SentenceTransformer
from sklearn_metrics.pairwise import cossine_similarity

input_file="data/embedded_chunks.json"
model=SentenceTransformer('all_MiniLM-L6-v2')
with open(input_file, "r") as f:
    chunks=json.load(f)

query="What happens if my grievance is not resolved on time?"

query_embedding=model.encode(query)

for chunk in chunks:
    chunk_embedding=chunk["embedding"]

    similarity=cossine_similarity(
        [query_embedding],
        [chunk_embedding]
    )
    print("This is the similarity ok!!!",similarity)
    chunk["similarity"]=float(similarity)
