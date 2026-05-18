# 🎥 Advanced YouTube RAG Chatbot

An advanced AI-powered YouTube chatbot that enables conversational interaction with YouTube videos using Retrieval-Augmented Generation (RAG), semantic reranking, transcript processing, and Gemini AI.

---

# 🚀 Live Features

✅ YouTube transcript extraction  
✅ Conversational AI chatbot  
✅ Multi-video support  
✅ Semantic search with FAISS  
✅ Gemini-powered responses  
✅ Semantic reranking  
✅ Timestamp citations  
✅ Transcript download  
✅ Streaming responses  
✅ Video thumbnail preview  
✅ Persistent vector database  
✅ Production-style modular architecture  

---

# 🧠 Project Overview

This application allows users to interact conversationally with YouTube videos.

The system extracts video transcripts, converts them into semantic embeddings, stores them in a FAISS vector database, retrieves relevant transcript chunks, reranks results semantically, and generates contextual answers using Gemini AI.

The project demonstrates:
- RAG pipeline engineering
- NLP workflows
- conversational memory
- semantic retrieval
- vector databases
- production AI application architecture

---

# 🏗️ Architecture

```text
YouTube URL
      ↓
Transcript Extraction
      ↓
Chunking
      ↓
Embeddings Generation
      ↓
FAISS Vector Database
      ↓
Retriever + Semantic Reranking
      ↓
Gemini LLM
      ↓
Streaming AI Response
```

---

# ⚙️ Tech Stack

## Frontend
- Streamlit

## AI / NLP
- LangChain
- Google Gemini AI
- Sentence Transformers

## Vector Database
- FAISS

## Data Processing
- YouTube Transcript API
- Recursive Text Chunking

---

# 📂 Project Structure

```text
youtube-rag-chatbot/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env
│
├── utils/
│   ├── transcript.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── vectorstore.py
│   ├── rag_chain.py
│   ├── reranker.py
│
├── data/
│   └── faiss_index/
│
└── assets/
    └── screenshots/
```

---

# 🚀 Installation

## Clone Repository

```bash
git clone <your_repo_link>
cd youtube-rag-chatbot
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Application

```bash
streamlit run app.py
```

---

# 📸 Screenshots

## Home Interface
(Add screenshot here)

## Video Processing
(Add screenshot here)

## Conversational Chat
(Add screenshot here)

## Timestamp Citations
(Add screenshot here)

---

# 🔥 Key Features Explained

## 🎥 Transcript Extraction
Automatically extracts transcripts from YouTube videos.

## 🧠 Retrieval-Augmented Generation (RAG)
Relevant transcript chunks are retrieved before generating responses.

## 📚 Semantic Reranking
Retrieved chunks are reranked using transformer-based semantic similarity models.

## ⏱ Timestamp Citations
Responses include transcript timestamps for source verification.

## ⚡ Streaming Responses
Answers stream in real time for better conversational UX.

## 📥 Transcript Download
Users can download processed transcripts directly.

---

# 🚀 Future Improvements

- YouTube playlist support
- Multi-user authentication
- Chat export
- PDF summary generation
- Voice interaction
- Hybrid BM25 + vector retrieval
- LangGraph agent workflows

---

# 📌 Learning Outcomes

This project helped strengthen understanding of:
- AI application engineering
- RAG pipelines
- vector search systems
- semantic retrieval
- conversational memory
- Streamlit deployment
- modular software architecture

---

# 👨‍💻 Author

Ali Khan

AI Developer | RAG Systems | Streamlit AI Apps | Python
