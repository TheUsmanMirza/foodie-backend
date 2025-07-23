# FOODIE - API

## Description  
**FOODIE** is an AI-powered restaurant review and recommendation system that uses Retrieval-Augmented Generation (RAG) to answer user queries related to restaurant food, ambiance, service, cuisine types, and more.  

It includes the application API endpoints with user authentication, vector-based semantic search, analytics dashboard, and settings management.

---

## Tech Stack
- **Backend:** [FastAPI](https://fastapi.tiangolo.com/), [LangChain](https://www.langchain.com/)  
- **LLM:** OpenAI (RAG-powered)
- **Vector Store:** Pinecone  
- **Authentication:** JWT-based Auth  
- **Deployment:** Docker, Docker Compose  

---

## Features
- User Authentication (Signup, Login, Forgot/Reset Password)
- AI Chatbot (RAG-based Q&A on restaurant reviews)
- Dashboard with restaurant insights and analytics
- Settings panel (Update password and user profile)
- Scraped reviews used to generate meaningful and contextual responses using LLMs
- Containerized with Docker for smooth deployment


## Docker Deployment

1. **Ensure Docker and Docker Compose are installed**

2. **Run backend with one command**
   ```bash
   docker-compose up --build
   ```

   - FastAPI backend will be available at: `http://localhost:8000`

---


