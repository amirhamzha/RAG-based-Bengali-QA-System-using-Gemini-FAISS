
# 📚 Bengali RAG-based Question Answering System

A Retrieval-Augmented Generation (RAG) pipeline for answering questions in **Bengali** using PDF documents. This project demonstrates how to process Bengali text, chunk, embed, index, and retrieve document segments for accurate semantic question answering.

---

## 🚀 Setup Guide

### 1. Clone the Repo
```bash
git clone https://github.com/amirhamzha/RAG-based-Bengali-QA-System-using-Gemini-FAISS.git
cd bengali-rag-qa
```

### 2. Setup Virtual Environment
```bash
python -m venv rag-env
rag-env\Scripts\activate  # On Windows
```

### 3. Install Requirements
```bash
pip install -r requirements.txt
```

### 4. Add `.env` File
```bash
GOOGLE_API_KEY=your_google_gemini_api_key
```

### 5. Run the Pipeline
```bash
python main.py        # To generate FAISS index

### 6. uvicorn api:app --reload --port 8000   #to run front-end

#  then go to the listed url 

http://localhost:8000/docs




## 🛠️ Tools, Libraries, and Packages Used

- **LangChain**: Framework for chaining LLMs with retrievers and indexes.
- **FAISS**: Fast vector similarity search.
- **Google Gemini API**: LLM for answering in Bengali.
- **HuggingFace Embedding Models**: Multilingual sentence embeddings.
- **PyMuPDF (fitz)**: Accurate Bengali PDF extraction.
- **dotenv**: Load API keys securely.

---

## 🔍 Sample Queries & Outputs

### Input: অনুপমের ভাষায় সুপুরুষ কাকে বলা হয়েছে?
**Output:** শুম্ভুনাথ

### Input: বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?
**Output:** ১৫ বছর

#after going to the specific url listed url 
 http://localhost:8000/docs

you find fast-api frontend and there is method listed below how to user input 

## 📖 API Documentation ()

write query in the query string and click excecute

- Endpoint: `/query`
- Method: `POST`
- Body:
```json
{
  "query": "বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?",    ##  only put query you want search top k and index are alrady given 
  "top_k": 6,
  "index_path": "vectorstores/HSC26-Bangla1st-paper"
}

---
##  responese 

  "answer": "পনেরো বছর",
  "query": "বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?",
  "retrieved_chunks": []



## 📊 Evaluation Matrix  select try it out it will povide similariest score of preselect queries and also for test cases
seleect try it out 

	
Response body
Download
{
  "precision@k": {
    "অনুপমের ভাষায় সুপুরুষ কোন নাম?": 0,
    "বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?": 0,
    "কাকে অনুপমের ভাগ্য দেবতা বলে উল্লেখ করা হয়েছে?": 0
  },
  "groundedness": {
    "অনুপমের ভাষায় সুপুরুষ কোন নাম?": 0.7472267362804645,
    "বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?": 0.6455140870209664,
    "কাকে অনুপমের ভাগ্য দেবতা বলে উল্লেখ করা হয়েছে?": 0.5142006681262803
  }
}

---

## ❓ Must Answer Questions

### 1. **What method or library did you use to extract the text, and why?**
We used **PyMuPDF (fitz)** for its superior handling of complex Bengali fonts and layouts. Standard extractors like PyPDF2 missed important glyphs.

### 2. **What chunking strategy did you choose?**
Character-level chunking using `RecursiveCharacterTextSplitter` with size = 5000 and overlap = 1100. This ensures semantic continuity in low-resource languages.

### 3. **What embedding model did you use?**
`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` — chosen for its lightweight footprint and strong performance across many languages including Bengali.

### 4. How are you comparing the query with your stored chunks? Why did you choose this similarity method and storage setup?
I index the chunk embeddings in a FAISS vectorstore. At query time I embed the question identically, then run a cosine‑similarity nearest‑neighbor search. FAISS gives millisecond lookups, and cosine similarity is ideal for direction‑based comparisons in embedding space.

### 5. **How do you ensure meaningful query-document comparison?**
Semantic embeddings + overlap-based chunking preserves context. Queries are matched to top-K relevant chunks before LLM processing.If a query is too vague (e.g. “age”), the top similarities will all be low—you can detect that via a threshold and then prompt for clarification or fall back to a simple keyword search.


### 6. **Are results relevant? What could improve them?**
Most answers are correct. To improve further:
- Tune chunk size/overlap.
- Try more powerful emedding paid one.
- Use Gemini paid or open ai paid  for better reasoning.






## Illustrations

### 1.  query-1
![query-1](./images/1.png)

---

### 2. query-2 
![query-2](./images/2.png)

---

### 3. query-3  
![query-3](./images/3.png)

---

### 4. evaluation  
![evaluation](./images/evaluation.png)


## if images are not seen go to image folder to see the out put of the images  and download those png

## 📌 Project Summary (for Resume)

> **Bengali RAG QA System**: Built a multilingual RAG pipeline to answer factual questions from Bengali literature using Gemini and HuggingFace embeddings. PDF to FAISS indexing, retrieval + LLM-based response. Used in education/NLP domains.

---



