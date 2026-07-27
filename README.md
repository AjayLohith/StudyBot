# 📚 StudyBot - AI Powered PDF Chatbot

An intelligent **Retrieval-Augmented Generation (RAG)** chatbot that allows users to upload PDF documents and ask natural language questions about their content. Instead of relying on the LLM's pre-trained knowledge, StudyBot retrieves relevant information from the uploaded document and generates context-aware answers using **Google Gemini**.
---

---

# 🛠️ Tech Stack

<p>
<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=python&logoColor=white">
<img src="https://img.shields.io/badge/Streamlit-FF4B4B.svg?style=flat&logo=streamlit&logoColor=white">
<img src="https://img.shields.io/badge/LangChain-121212.svg?style=flat">
<img src="https://img.shields.io/badge/Google%20Gemini-4285F4.svg?style=flat&logo=google&logoColor=white">
<img src="https://img.shields.io/badge/FAISS-0467DF.svg?style=flat">
<img src="https://img.shields.io/badge/PyPDF2-3776AB.svg?style=flat">
<img src="https://img.shields.io/badge/Python%20Dotenv-ECD53F.svg?style=flat">
<img src="https://img.shields.io/badge/Git-F05032.svg?style=flat&logo=git&logoColor=white">
<img src="https://img.shields.io/badge/GitHub-181717.svg?style=flat&logo=github&logoColor=white">
<img src="https://img.shields.io/badge/Streamlit%20Cloud-FF4B4B.svg?style=flat&logo=streamlit&logoColor=white">
</p>

---

## 🚀 Live Demo

🔗 **Demo:** https://studybottt.streamlit.app

---


# ✨ Features

- 📄 Upload any PDF document
- 🤖 Ask questions in natural language
- 🔍 Semantic Search using Vector Embeddings
- 🧠 Retrieval-Augmented Generation (RAG)
- ⚡ Google Gemini 2.5 Flash LLM
- 📚 FAISS Vector Database
- ✂️ Automatic Text Chunking
- 💬 Context-aware responses
- 🔄 Upload a new PDF without refreshing
- ☁️ Streamlit Cloud Deployment



# 🏗️ System Architecture

```
                 Upload PDF
                      │
                      ▼
            Extract Text (PyPDF2)
                      │
                      ▼
     RecursiveCharacterTextSplitter
                      │
                      ▼
       Google Embedding Model
                      │
                      ▼
              FAISS Vector Store
                      │
      Similarity Search (Top-K)
                      │
                      ▼
        Relevant Document Chunks
                      │
                      ▼
      Gemini 2.5 Flash + Prompt
                      │
                      ▼
             Final AI Response
```

---

# 🧠 RAG Workflow

```
User Uploads PDF
        │
        ▼
Extract Text
        │
        ▼
Split into Chunks
        │
        ▼
Generate Embeddings
        │
        ▼
Store Embeddings in FAISS
        │
        ▼
User asks Question
        │
        ▼
Similarity Search
        │
        ▼
Retrieve Top Matching Chunks
        │
        ▼
Gemini Generates Answer
```

---

# 📂 Project Structure

```
StudyBot
│
├── app.py
├── requirements.txt
├── .env
├── .gitignore
├── README.md
└── images
    ├── upload.png
    └── chat.png
```

---

# ⚙️ Core Concepts Used

## Retrieval-Augmented Generation (RAG)

Instead of sending the complete PDF to the LLM, the application retrieves only the most relevant document chunks and provides them as context for answer generation.

---

## Recursive Character Text Splitting

Large PDF text is divided into smaller overlapping chunks.

```
Chunk Size : 1000
Chunk Overlap : 100
```

This preserves context while improving retrieval accuracy.

---

## Vector Embeddings

Each chunk is converted into a dense numerical vector using:

```
models/gemini-embedding-001
```

Semantic similarity between vectors enables intelligent document search.

---

## FAISS Vector Database

Facebook AI Similarity Search (FAISS) stores vector embeddings locally and performs high-speed nearest-neighbor searches.

Benefits:

- Fast retrieval
- Memory efficient
- Scalable
- No external database required

---

## Semantic Search

Instead of keyword matching,

```
Question

↓

Embedding

↓

Nearest Vector Search

↓

Relevant Chunks
```

This allows users to ask questions naturally.

---

## Prompt Engineering

The LLM receives only retrieved document context.

Example Prompt

```
You are a helpful study assistant.

Answer the question only using the provided context.

Context:
{context}

Question:
{question}
```

This minimizes hallucinations.

---

## LangChain Components Used

| Component | Purpose |
|------------|----------|
| ChatPromptTemplate | Prompt Creation |
| GoogleGenerativeAIEmbeddings | Text Embeddings |
| ChatGoogleGenerativeAI | Gemini LLM |
| RecursiveCharacterTextSplitter | Chunking |
| FAISS | Vector Database |
| create_stuff_documents_chain | Combine Retrieved Documents |
| invoke() | Execute Chain |

---

# 🚀 Strategies Implemented

### ✅ Retrieval-Augmented Generation (RAG)

Improves answer accuracy by grounding responses in uploaded documents.

---

### ✅ Semantic Search

Retrieves relevant chunks using embedding similarity instead of keyword matching.

---

### ✅ Chunk Overlap Strategy

Maintains contextual continuity across chunk boundaries.

---

### ✅ Top-K Retrieval

Retrieves the three most relevant chunks before generating an answer.

```
k = 3
```

---

### ✅ Session State Management

Caches the vector store to avoid regenerating embeddings on every Streamlit rerun.

---

### ✅ Dynamic PDF Detection

Automatically rebuilds the FAISS index whenever a different PDF is uploaded.

---

### ✅ Context-Limited Prompting

The model answers only from the retrieved document context.

---

# 🔄 Application Flow

```
Start

↓

Upload PDF

↓

Extract Text

↓

Chunk Text

↓

Generate Embeddings

↓

Create FAISS Index

↓

Store in Session

↓

Ask Question

↓

Similarity Search

↓

Retrieve Chunks

↓

Gemini

↓

Answer
```

---

# 📦 Installation

Clone the repository

```bash
git clone https://github.com/yourusername/StudyBot.git
```

Move into the project

```bash
cd StudyBot
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env`

```
GOOGLE_API_KEY=YOUR_API_KEY
```

Run the application

```bash
streamlit run app.py
```

---

# 📋 Requirements

```
streamlit
langchain
langchain-community
langchain-google-genai
langchain-text-splitters
PyPDF2
faiss-cpu
python-dotenv
```

---

# 🎯 Future Improvements

- Conversation Memory
- Chat History
- Multi-PDF Retrieval
- Hybrid Search (BM25 + Vector Search)
- Persistent Vector Database (ChromaDB/Pinecone)
- Source Citation
- Streaming Responses
- OCR Support for Scanned PDFs
- Document Summarization
- Multi-language Support

---

# 👨‍💻 Author

**Ajay Lohith**

GitHub: https://github.com/AjayLohith

LinkedIn: https://linkedin.com/in/your-linkedin

---

## ⭐ If you found this project useful, consider giving it a star!
