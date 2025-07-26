#from langchain.vectorstores import FAISS


from langchain_community.vectorstores import FAISS

from langchain.docstore.document import Document
import os

def create_faiss_index(chunks: list[str], embedder, source_name: str = "unknown") -> FAISS:
    docs = [Document(page_content=chunk, metadata={"source": source_name}) for chunk in chunks]
    index = FAISS.from_documents(docs, embedder)
    return index

def save_faiss_index(index: FAISS, path: str):
    os.makedirs(path, exist_ok=True)
    index.save_local(path)
