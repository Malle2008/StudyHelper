import uuid
import time
from fastapi import FastAPI
from pydantic import BaseModel
from qdrant_client.http import models
from qdrant_client import QdrantClient
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer
from fastapi import Query

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

qdrant= QdrantClient(url="http://192.168.68.141:6333")
collection_name = "studyhelper"
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")


stored_texts = []

class TextItem(BaseModel):
    text: str

@app.post("/add")
def add(item: TextItem):
    stored_texts.append(item.text)

    vector = model.encode([item.text])[0].tolist()
    qdrant.upsert(
        collection_name=collection_name,
        points=[models.PointStruct(id=str(uuid.uuid4()), vector=vector, payload={"text": item.text, "timeStamp": str(time.time())})]
    )

    return {"message": "Text added successfully"}

@app.get("/all")
def get_all():
    return {"texts": stored_texts}

@app.get("/ask")
def ask(text: str = Query(...)):
    query_vector = model.encode([text])[0].tolist()

    results = qdrant.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=3
    ).points

    response = []
    for r in results:
        response.append({"text": r.payload["text"], "score": r.score})

    return response


'''
- add more upload options
    - pdf
    - docx
    - txt
    - video/audio (transcription)

- add collections
    - creating new collections 
    - removing collections 
    
- add llm functionality 
    - answering questions based on context
    - used to create quizzes
        -types  
            - multiple choice
            - fill in the blanks
        - made by llm with specific pattern to later be parsed into a html quiz
'''