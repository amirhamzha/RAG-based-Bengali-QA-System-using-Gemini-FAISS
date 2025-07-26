import os
from pdf_utils import process_pdf
from chunk_utils.chunker import chunk_text
from embedding_utils.embedder import get_embedder
from vectorstore_utils.indexer import create_faiss_index, save_faiss_index

PDF_DIR = "pdfs"
OUTPUT_DIR = "cleaned"
VECTOR_DIR = "vectorstores"

# Ensure output folders exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(VECTOR_DIR, exist_ok=True)

embedder = get_embedder()  # Only once

for filename in os.listdir(PDF_DIR):
    if filename.lower().endswith(".pdf"):
        pdf_path = os.path.join(PDF_DIR, filename)

        cleaned_text = process_pdf(pdf_path)

        # Save cleaned text
        cleaned_path = os.path.join(OUTPUT_DIR, filename.replace(".pdf", ".txt"))
        with open(cleaned_path, "w", encoding="utf-8") as f:
            f.write(cleaned_text)

        # Chunk and save for inspection
        chunks = chunk_text(cleaned_text)
        chunk_path = os.path.join(OUTPUT_DIR, filename.replace(".pdf", ".chunks.txt"))
        with open(chunk_path, "w", encoding="utf-8") as f:
            for i, chunk in enumerate(chunks):
                f.write(f"--- Chunk {i+1} ---\n{chunk}\n\n")

        # Create and save vector index
        index = create_faiss_index(chunks, embedder, source_name=filename)
        index_path = os.path.join(VECTOR_DIR, filename.replace(".pdf", ""))
        save_faiss_index(index, index_path)

        print(f"✅ Finished: {filename}")


        


print("Chunks containing 'শুম্ভুনাথ':")
for chunk in chunks:
    if "শুম্ভুনাথ" in chunk:
        print(chunk, "\n---")

print("Chunks containing '১৫ বছর':")
for chunk in chunks:
    if "১৫ বছর" in chunk:
        print(chunk, "\n---")

print("🎉 All documents indexed.")
