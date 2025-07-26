
import os
from typing import List
#from langchain.vectorstores import FAISS
# from langchain.llms import GoogleGenerativeAI
# from langchain_community.llms import GoogleGenerativeAI

from langchain_google_genai import GoogleGenerativeAI

from langchain_community.vectorstores import FAISS

from langchain.schema import HumanMessage

from embedding_utils.embedder import get_embedder
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage


# ─── Load Gemini API Key from .env ───
from dotenv import load_dotenv
load_dotenv()

# ─── Initialize embedder once ───
EMBEDDER = get_embedder()

# ─── Load FAISS Index ───
def load_index(index_path: str) -> FAISS:
    return FAISS.load_local(index_path, EMBEDDER,allow_dangerous_deserialization=True)

# ─── Retrieve Top‑K Chunks ───
def retrieve_chunks(query: str, index: FAISS, top_k: int = 8)-> List[str]:
    docs = index.similarity_search(query, k=top_k)
    return [doc.page_content for doc in docs]

# def call_llm(query: str, context_chunks: List[str]) -> str:
#     context = "\n\n".join(context_chunks)
#     prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"

#     llm = GoogleGenerativeAI(model="gemini-pro")
#     response = llm([HumanMessage(content=prompt)])
#     return response.content



def call_llm(query: str, context_chunks: List[str]) -> str:
    """
    Sends the retrieved context + query to Gemini and returns the generated answer.
    """
    # Build the prompt as a single string
    context = "\n\n".join(context_chunks)
    
    prompt = (
    f"Context:\n{context}\n\n"
    f"Question: {query}\n"
    f"Instructions: Answer only from the context above in 1-5 Bengali words. "
    f"Do not add any extra text or explanation.\n"
    f"try to give exact asnwer"
    
    f"Do not explain or add anything.\n"
    f"Answer:"
    )


    # Initialize the Gemini chat model
 
    #llm = ChatGoogleGenerativeAI(model="gemini-pro")
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

    # Use invoke to send a single prompt

    
    llm_response = llm.invoke([HumanMessage(content=prompt)])

    # Extract the generated text
    # generated = llm_response.generations[0][0].text
    generated = llm_response.content
    return generated



def generate_answer(query: str, index_path: str, top_k: int =8 ) -> str:
    index = load_index(index_path)
    chunks = retrieve_chunks(query, index, top_k)
    return call_llm(query, chunks)

# ─── Best Practice: Externalized Interface ───
# Use this function in a separate CLI/API/GUI app to query the system.
# Avoid mixing it into your main indexing code (main.py).





# from typing import List
# import os
# from dotenv import load_dotenv
# load_dotenv()

# from langchain_community.vectorstores import FAISS
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_community.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.retrievers import VectorStoreRetriever
# from langchain.chains import RetrievalQA
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.schema import HumanMessage

# # ─── Embedder & Retriever Setup ───
# def get_retriever(index_path: str, model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2") -> VectorStoreRetriever:
#     """
#     Load FAISS index and return a retriever that fetches top_k chunks.
#     """
#     # Load embeddings + index
#     embeddings = HuggingFaceEmbeddings(model_name=model_name)
#     vectorstore = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
#     return VectorStoreRetriever(vectorstore=vectorstore, k=6)  # adjust k as needed

# # ─── Build RetrievalQA Chain ───
# def get_qa_chain(index_path: str) -> RetrievalQA:
#     """
#     Constructs a RetrievalQA chain with map_reduce strategy for Bengali QA.
#     """
#     retriever = get_retriever(index_path)
#     llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-pro")
#     return RetrievalQA.from_chain_type(
#         llm,
#         retriever=retriever,
#         chain_type="map_reduce",
#         return_source_documents=True,
#         chain_type_kwargs={
#             "map_prompt": """Context:
# {context}

# Question: {question}
# Instructions: Answer only from the context, in Bengali, with exactly the entity (no extra text).
# Answer:""",
#             "reduce_prompt": """You are given partial answers:
# {answers}

# Combine them into a single, concise Bengali answer that exactly matches the fact.
# Answer:"""
#         }
#     )

# # ─── Full RAG Pipeline ───
# def generate_answer(query: str, index_path: str) -> str:
#     """
#     1) Build a RetrievalQA chain
#     2) Run the query
#     3) Return the final answer
#     """
#     qa = get_qa_chain(index_path)
#     result = qa({"query": query})
#     return result["result"]
