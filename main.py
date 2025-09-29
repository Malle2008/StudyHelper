import uuid
from qdrant_client.http import models
from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter
from sentence_transformers import SentenceTransformer

texts = [
    "Fotosyntesen är processen där växter omvandlar solljus till energi.",
    "Einstein developed the theory of relativity, which revolutionized physics."
]

VectorSize = 384  # Dimension of the sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 model

# Connect to local Qdrant instance
qdrant= QdrantClient(url="http://192.168.68.141:6333")
collection_name = "studyhelper"
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# Check if collection exists
if not qdrant.collection_exists(collection_name):
    qdrant.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(size=VectorSize, distance=models.Distance.COSINE)
    )
    print(f"✅ Collection '{collection_name}' created")
else:
    print(f"Collection '{collection_name}' already exists")
'''
for t in texts:
    vector = model.encode([t])[0].tolist()
    qdrant.upsert(
        collection_name=collection_name,
        points=[models.PointStruct(id=str(uuid.uuid4()), vector=vector, payload={"text": t})]
    )
'''

query_vector = model.encode(["hello"])[0].tolist()

results = qdrant.query_points(
    collection_name=collection_name,
    query=query_vector,
    limit=3
).points

for r in results:
    print(r.payload["text"], "(score:", r.score, ")")
