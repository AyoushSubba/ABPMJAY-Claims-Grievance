print("hello")
from sentence_transformers import SentenceTransformer

print("model initializing!!")
model =SentenceTransformer("sentence-transformers/all-MiniLm-L6-v2")
query="What happens if my grievance is not resolved on time?"

embedding=model.encode(query)

print(embedding.tolist())