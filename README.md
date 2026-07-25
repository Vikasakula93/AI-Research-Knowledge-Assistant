# AI Research & Knowledge Assistant

An AI-powered backend application developed to simplify searching, understanding, and interacting with research papers and technical documents. The project combines semantic search, Retrieval-Augmented Generation (RAG), document summarization, document comparison, and machine learning-based document classification into a single backend system.

The main objective of this project was to build a scalable backend that allows users to upload documents, search information using semantic similarity instead of simple keyword matching, and receive AI-generated answers that are grounded in the uploaded documents.

---

# Project Overview

While working on this project, I focused on solving a common problem faced by researchers and organizations—finding accurate information from large collections of documents.

Instead of relying only on keyword search, the application converts document content into vector embeddings, stores them in a vector database, and retrieves the most relevant information before sending it to the language model. This Retrieval-Augmented Generation (RAG) approach improves answer quality and reduces hallucinations.

Along with intelligent document search, I also integrated TensorFlow-based document classification, automatic summarization, document comparison, and conversation memory to provide a better research experience.

---

# Key Features

### Document Management

- Upload PDF, DOCX, and TXT documents
- Store document metadata
- List uploaded documents
- Delete documents
- Reprocess documents

### AI-Powered Search

- Semantic search using embeddings
- Keyword search
- Hybrid search
- Multi-document retrieval
- Relevance ranking

### AI Question Answering

- Retrieval-Augmented Generation (RAG)
- Citation-supported answers
- Source document tracking
- Page number references
- Context-aware responses

### Document Intelligence

- Executive summaries
- Technical summaries
- Bullet-point summaries
- Document comparison
- Key takeaway extraction

### Machine Learning

- TensorFlow document classification
- Automatic category prediction
- Confidence scoring

### Analytics

- Uploaded document statistics
- Processed chunk count
- Generated embedding count
- Search analytics
- Question history

---

# Technology Stack

| Category | Technology |
|----------|------------|
| Backend | FastAPI |
| Language | Python |
| Validation | Pydantic |
| Embeddings | Sentence Transformers |
| Vector Database | FAISS |
| Large Language Model | OpenAI GPT |
| Machine Learning | TensorFlow |
| PDF Processing | PyPDF2 |
| Document Processing | python-docx |
| API Documentation | Swagger / OpenAPI |
| Environment Management | python-dotenv |

---

# System Architecture

```text
                        Client Applications
                                │
                                ▼
                      FastAPI Backend Server
                                │
        ┌───────────────────────┼────────────────────────┐
        │                       │                        │
        ▼                       ▼                        ▼
 Document APIs            Search APIs              Analytics APIs
        │
        ▼
                Business Logic Layer
        ┌──────────────────────────────────────┐
        │ Document Service                     │
        │ Search Service                       │
        │ Embedding Service                    │
        │ Vector Database Service              │
        │ LLM Service                          │
        │ Question Answering Service           │
        │ Summarization Service                │
        │ Comparison Service                   │
        │ Classification Service               │
        └──────────────────────────────────────┘
                                │
                                ▼
                 External AI & Storage Layer
        ┌──────────────────────────────────────┐
        │ FAISS Vector Database                │
        │ Sentence Transformers                │
        │ OpenAI GPT API                       │
        │ TensorFlow Classification Model      │
        │ File Storage                         │
        └──────────────────────────────────────┘
```

---

# Why I Built This Project

The goal of this project was to understand how modern AI applications combine document processing, vector databases, embeddings, machine learning, and Large Language Models into a single system.

Instead of building only a chatbot, I wanted to build an application that follows a real-world RAG architecture where responses are generated from uploaded documents rather than relying only on the language model's general knowledge.

Throughout the development process, I focused on writing modular code, separating business logic into services, and designing REST APIs that are easy to maintain and extend.

---

# 📁 Project Structure

```text
AI-Research-Knowledge-Assistant/
│
├── backend/                                  # Backend application
│   │
│   ├── app/                                  # Main application source code
│   │   ├── __init__.py                       # Python package initialization
│   │   ├── main.py                           # FastAPI application entry point
│   │   ├── config.py                         # Application configuration
│   │   ├── exceptions.py                     # Custom exception handlers
│   │   │
│   │   ├── models/                           # Pydantic request & response models
│   │   │   ├── __init__.py
│   │   │   ├── document.py                   # Document schemas
│   │   │   ├── search.py                     # Search schemas
│   │   │   ├── qa.py                         # Question & Answer schemas
│   │   │   ├── comparison.py                 # Document comparison schemas
│   │   │   ├── summarization.py              # Summary schemas
│   │   │   ├── classification.py             # Classification schemas
│   │   │   └── analytics.py                  # Analytics schemas
│   │   │
│   │   ├── routes/                           # REST API endpoints
│   │   │   ├── __init__.py
│   │   │   ├── documents.py                  # Document APIs
│   │   │   ├── search.py                     # Search APIs
│   │   │   ├── qa.py                         # Question Answering APIs
│   │   │   ├── comparison.py                 # Comparison APIs
│   │   │   ├── summarization.py              # Summarization APIs
│   │   │   ├── classification.py             # Classification APIs
│   │   │   └── analytics.py                  # Analytics APIs
│   │   │
│   │   └── services/                         # Business logic layer
│   │       ├── __init__.py
│   │       ├── document_service.py           # Document processing
│   │       ├── embedding_service.py          # Embedding generation
│   │       ├── vector_db_service.py          # FAISS vector database operations
│   │       ├── llm_service.py                # OpenAI integration
│   │       ├── search_service.py             # Semantic & keyword search
│   │       ├── qa_service.py                 # Retrieval-Augmented Generation (RAG)
│   │       ├── summarization_service.py      # Document summarization
│   │       ├── comparison_service.py         # Multi-document comparison
│   │       ├── classification_service.py     # TensorFlow document classification
│   │       └── analytics_service.py          # Analytics & statistics
│   │
│   ├── ml_models/                            # Saved Machine Learning models
│   │   └── document_classifier.h5            # Trained TensorFlow model
│   │
│   ├── uploads/                              # Uploaded documents
│   │
│   ├── data/
│   │   ├── chunks/                           # Processed text chunks
│   │   ├── embeddings/                       # Generated embeddings
│   │   └── faiss_index/                      # FAISS vector index
│   │
│   ├── tests/                                # Unit & integration tests
│   │   ├── __init__.py
│   │   ├── test_documents.py
│   │   ├── test_search.py
│   │   ├── test_qa.py
│   │   ├── test_classification.py
│   │   └── test_summary.py
│   │
│   ├── .env.example                          # Environment variable template
│   ├── .env                                  # Local environment variables
│   ├── requirements.txt                      # Python dependencies
│   └── README.md                             # Backend documentation
│
├── frontend/                                 # Optional React frontend
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── README.md
│
├── docs/                                     # Project documentation
│   ├── API_GUIDE.md
│   ├── ARCHITECTURE.md
│   ├── DEPLOYMENT.md
│   └── SYSTEM_DESIGN.md
│
├── .gitignore                                # Files ignored by Git
├── LICENSE                                   # MIT License
└── README.md                                 # Main project documentation
```

## 📂 Folder Description

| Folder/File | Purpose |
|-------------|---------|
| **backend/** | Complete FastAPI backend application. |
| **app/** | Contains the application's source code. |
| **models/** | Pydantic models used for request validation and API responses. |
| **routes/** | REST API endpoints for all project features. |
| **services/** | Core business logic including RAG, search, embeddings, summarization, comparison, and classification. |
| **ml_models/** | Stores the trained TensorFlow document classification model. |
| **uploads/** | Stores uploaded research papers and technical documents. |
| **data/chunks/** | Stores processed document chunks before embedding generation. |
| **data/embeddings/** | Stores generated embedding vectors. |
| **data/faiss_index/** | Stores the FAISS vector database index for semantic retrieval. |
| **tests/** | Unit and integration test cases. |
| **frontend/** | Optional React frontend for interacting with the backend APIs. |
| **docs/** | Additional project documentation including API guide, architecture, deployment, and system design. |
| **README.md** | Main documentation containing setup instructions, architecture, API usage, and project overview. |
| **requirements.txt** | Python dependency list required to run the project. |
| **.env.example** | Template for required environment variables. |
| **LICENSE** | Project license information. |


---

---

# ▶️ Running the Project

After completing the installation and environment setup, start the FastAPI development server.

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

If the server starts successfully, you should see:

```text
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

---

# 🌐 API Documentation (Swagger)

Once the application is running, open the following URL in your browser:

```
http://localhost:8000/docs
```

Swagger UI provides an interactive interface where every API can be tested directly without using Postman.

You can perform the following operations:

### 📄 Document Management

- Upload PDF, DOCX, or TXT documents
- View uploaded documents
- Get document details
- Delete documents
- Reprocess documents

### 🔍 Search

- Semantic Search
- Keyword Search
- Hybrid Search
- Search across multiple uploaded documents

### 🤖 AI Question Answering

- Ask questions about uploaded documents
- Receive citation-supported answers
- View source documents
- View page numbers
- Retrieve supporting context

### 📚 Document Analysis

- Generate Executive Summary
- Generate Technical Summary
- Generate Bullet Point Summary
- Extract Key Takeaways
- Compare multiple documents

### 🧠 Machine Learning

- Classify uploaded documents
- Predict document category
- View confidence scores

### 📊 Analytics

- View uploaded document statistics
- Total processed chunks
- Total embeddings generated
- Most queried documents
- Total questions answered

---

# 📬 Example Workflow

A complete workflow can be performed directly from the Swagger interface.

### Step 1

Open:

```
http://localhost:8000/docs
```

### Step 2

Upload one or more research papers using the **Upload Document** endpoint.

### Step 3

After processing is complete, perform a Semantic Search using any query.

### Step 4

Ask questions related to the uploaded documents using the Question Answering endpoint.

### Step 5

Generate document summaries.

### Step 6

Compare two or more uploaded documents.

### Step 7

Run the Document Classification endpoint to predict the document category.

### Step 8

Open the Analytics endpoint to view processing statistics and usage information.

---

# ✅ Verifying the Installation

Health Check

```
GET /health
```

Expected Response

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "development"
}
```

If the health endpoint responds successfully and the Swagger UI loads at:

```
http://localhost:8000/docs
```

then the project has been configured correctly and is ready to use.

---

# 📦 Repository Setup

To ensure the project is fully executable:

- Clone the repository.
- Create and activate a Python virtual environment.
- Install all dependencies from `requirements.txt`.
- Configure the `.env` file using `.env.example`.
- Start the FastAPI server.
- Open `http://localhost:8000/docs`.
- Test all available APIs directly through the Swagger UI.

No additional setup is required beyond the steps described in this README.
