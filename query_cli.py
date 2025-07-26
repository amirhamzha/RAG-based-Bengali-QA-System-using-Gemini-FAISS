from rag_utils.query_engine import generate_answer

# Set your FAISS index path (folder name inside vectorstores)
INDEX_PATH = "vectorstores/HSC26-Bangla1st-paper"  # adjust based on your indexed filename

def main():
    print("💬 Bengali/English RAG CLI — Type your question (or 'exit' to quit)")

    while True:
        query = input("👉 You: ")
        if query.lower() in ["exit", "quit"]:
            break

        try:
            answer = generate_answer(query, index_path=INDEX_PATH)
            print(f"🤖 Gemini: {answer.strip()}\n")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
