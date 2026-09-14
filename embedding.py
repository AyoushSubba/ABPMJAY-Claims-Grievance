from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json

#loading the pretrained model
model= SentenceTransformer('all-MiniLM-L6-v2')

input_file="data/chunks.json"

output_file="data/embedding_chunks.json"

with open(input_file,"r") as f:
    chunks=json.load(f)
texts=[chunk["text"] for chunk in chunks]

#create Embeddings..
embeddings=model.encode(
    texts,
    show_progress_bar=True
)

for chunk ,embedding in zip(chunks,embeddings):
    chunk["embedding"]=embedding.tolist()


with open(output_file,"w",encoding="utf-8") as f:
    json.dump(
        chunks,
        f,
        ensure_ascii=False,
        indent=2
    )

print(f"Embedded {len(chunks)} chunks.")
print(f"Saved to {output_file}")
print(f"Embedding size: {len(chunks[0]['embedding'])}")

