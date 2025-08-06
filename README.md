# 🎯 TRT Digital Support Assistant | RAG-Based Smart Q&A System

This project is a smart support assistant built on a **Retrieval-Augmented Generation (RAG)** architecture, developed specifically for **TRT's corporate knowledge base**.  
The system semantically analyzes user questions in natural language and then identifies the most relevant content to generate meaningful and contextual answers with the help of an **LLM (Large Language Model)**.

---

## 🛠️ Key Technologies

- **Backend**: FastAPI  
- **Vector Database**: FAISS  
- **Embedding Model**: SentenceTransformers  
- **Large Language Model (LLM)**: Azure OpenAI  
- **Web Interface**: Streamlit  
- **Containerization**: Docker  

---

## ⚙️ System Architecture & Flow

1. **Question Embedding**  
   The user's question is converted into a vector representation (embedded) using **SentenceTransformers**.

2. **Semantic Search**  
   The vectorized question is searched via **FAISS** to semantically find the most relevant corporate content.

3. **Context Creation**  
   The selected content is passed as context to the **LLM from Azure OpenAI** for answer generation.

4. **Answer Generation**  
   The LLM uses the provided context to create a customized, natural language answer and presents it on the **user interface**.

5. **Interaction Logging**  
   All answers are logged via a **logging system** for future analysis and system improvement processes.

---


## ✨ Project Outcomes

- **Accurate Responses**: High-accuracy answers thanks to targeted content filtering  
- **Corporate Context**: Contextual and consistent answers based on company-specific knowledge  
- **Flexible Infrastructure**: A modular, reusable, and scalable RAG architecture  
- **Enhanced User Experience**: A chat-based solution designed for real user interactions
