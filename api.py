from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag_utils.query_engine import generate_answer, load_index, retrieve_chunks
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from embedding_utils.embedder import get_embedder
app = FastAPI(title="RAG Conversation API")

class QueryRequest(BaseModel):
    query: str
    top_k: int = 6
    index_path: str = "vectorstores/HSC26-Bangla1st-paper"

class QueryResponse(BaseModel):
    answer: str
    query: str
    retrieved_chunks: list[str]

@app.post("/chat", response_model=QueryResponse)
async def chat(request: QueryRequest):
    try:
        index = load_index(request.index_path)
        chunks = retrieve_chunks(request.query, index, top_k=request.top_k)
        answer = generate_answer(request.query, request.index_path, top_k=request.top_k)

        return QueryResponse(
            query=request.query,
            answer=answer,
            
            retrieved_chunks=chunks
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


test_cases = [
    ("অনুপমের ভাষায় সুপুরুষ কোন নাম?", "শুম্ভুনাথ"),
    ("বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?", "১৫ বছর"),
    ("কাকে অনুপমের ভাগ্য দেবতা বলে উল্লেখ করা হয়েছে?", "মামাকে"),
]

embedder = get_embedder()

def evaluate_groundedness(answer, contexts):
    vectors = embedder.embed_documents(contexts + [answer])
    ctx_vecs, ans_vec = np.array(vectors[:-1]), np.array(vectors[-1])
    sims = cosine_similarity(ctx_vecs, ans_vec.reshape(1, -1)).flatten()
    return float(np.mean(sims))


@app.get("/evaluate")
async def evaluate(index_path: str = "vectorstores/HSC26-Bangla1st-paper", k: int = 6):
    try:
        index = load_index(index_path)
        relevance_results = {}
        groundedness_results = {}

        for query, expected in test_cases:
            retrieved = retrieve_chunks(query, index, top_k=k)
            hit = any(expected in chunk for chunk in retrieved)
            relevance_results[query] = 1.0 if hit else 0.0

            answer = generate_answer(query, index_path, top_k=k)
            groundedness_score = evaluate_groundedness(answer, retrieved)
            groundedness_results[query] = groundedness_score

        return {
            "precision@k": relevance_results,
            "groundedness": groundedness_results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))