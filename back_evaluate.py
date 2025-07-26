import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from rag_utils.query_engine import load_index, retrieve_chunks, generate_answer
from embedding_utils.embedder import get_embedder

embedder = get_embedder()

# Example test set
test_cases = [
    ("অনুপমের ভাষায় সুপুরুষ কোন নাম?", "শুম্ভুনাথ", "Chunk containing শুম্ভুনাথ"),
    ("বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?", "১৫ বছর", "Chunk containing ১৫ বছর"),
]

def evaluate_groundedness(answer, contexts):
    vectors = embedder.embed_documents(contexts + [answer])
    ctx_vecs, ans_vec = np.array(vectors[:-1]), np.array(vectors[-1])
    sims = cosine_similarity(ctx_vecs, ans_vec.reshape(1, -1)).flatten()
    return float(np.mean(sims))

def evaluate_relevance(index_path, k=6):
    index = load_index(index_path)
    results = {}
    for query, expected, _ in test_cases:
        retrieved = retrieve_chunks(query, index, top_k=k)
        hit = any(expected in chunk for chunk in retrieved)
        results[query] = 1.0 if hit else 0.0
    return results

if __name__ == "__main__":
    index_path = "vectorstores/HSC26-Bangla1st-paper"
    relevance = evaluate_relevance(index_path, k=6)
    print("Precision@6:", relevance)

    index = load_index(index_path)
    for query, expected, _ in test_cases:
        chunks = retrieve_chunks(query, index, k=6)
        ans = generate_answer(query, index_path, top_k=6)
        score = evaluate_groundedness(ans, chunks)
        print(f"Groundedness for '{query}': {score:.3f}")
