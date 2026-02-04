# E-commerce Chatbot

An intelligent E-commerce Chatbot designed to assist users with product queries, using **LangGraph** for orchestrating multi-turn conversations, RAG (Retrieval-Augmented Generation), and hybrid semantic routing.

## System Architecture

![Architecture Diagram](backend/app/resources/architecture-diagram.jpg)
*(High-level overview of the system components and data flow)*

## Chatbot Logic (LangGraph State Machine)

![Chatbot Logic](backend/app/resources/chat-bot-logic.jpg)
*(Detailed flow of how the chatbot processes user queries using Semantic Router and RAG)*

The chatbot uses a **StateGraph** built with `langgraph` to manage conversation flow and persistence.

- **Router Node**: Hybrid router that combines **Semantic Routing** (fast) with an **LLM Fallback** (smart) to determine user intent.
- **Service Nodes**:
  - `product_inquiry`: Generates SQL queries to search the PostgreSQL database, preserving context (e.g., "Which is cheapest?").
  - `faq`: Queries the ChromaDB vector store for general answers.
  - `small_talk`: Handles casual conversation.
- **Persistence**: Uses `MemorySaver` (in-memory) or `PostgresSaver` to maintain chat history via a unique `thread_id`.

## UI Preview

![User Interface](backend/app/resources/chat-bot-ui.png)
*(Screenshot of the React-based chat interface)*

## Features

-   **Multi-turn Conversations**: Maintains context across messages (e.g., filters "those" products from the previous turn).
-   **LangGraph Orchestration**: Robust state management for complex conversational flows.
-   **Hybrid Routing**: Combines `semantic-router` for speed and a lightweight Gemini Flash LLM for handling ambiguity.
-   **Context-Aware SQL Generation**: intelligently converts natural language to SQL, understanding follow-up filters.
-   **RAG (Retrieval-Augmented Generation):** Retrieves relevant FAQ information from ChromaDB.

## Tech Stack

### Backend
-   **Language:** Python 3.13+
-   **Framework:** FastAPI
-   **Agent Framework:** **LangGraph** & **LangChain**
-   **Database:** 
    -   PostgreSQL (Product Data)
    -   ChromaDB (Vector/FAQ)
-   **AI/ML:**
    -   `langchain_groq` (Groq LPU Inference)
    -   `google_genai` (Gemini Flash for Routing)
    -   `semantic-router`
-   **Dependency Management:** `uv`

### Frontend
-   **Framework:** React 19
-   **Build Tool:** Vite
-   **Styling:** TailwindCSS 4
-   **Language:** TypeScript
-   **State:** Maintains `thread_id` for session persistence.

## Setup & Installation

### Prererequisites
-   Python 3.13 or higher
-   Node.js and npm
-   `uv` (for Python dependency management)
-   Docker (optional, for running PostgreSQL)

### 1. Backend Setup

Navigate to the backend directory:
```bash
cd backend
```

Install dependencies using `uv`:
```bash
uv sync
```

Set up environment variables:
Copy `.env.example` to `.env` and fill in the required API keys.
```bash
cp .env.example .env
```
*Required keys*: `DATABASE_URL`, `GROQ_API_KEY`, `GOOGLE_API_KEY`. *Optional*: `CHROMA_API_KEY`, `CHROMA_TENANT` (for cloud ChromaDB).

Run the backend server:
```bash
# Using uv to run uvicorn
uv run uvicorn app.main:app --reload
```
The API will be available at `http://localhost:8000`.

### 2. Frontend Setup

Navigate to the frontend directory:
```bash
cd frontend
```

Install dependencies:
```bash
npm install
```

Run the development server:
```bash
npm run dev
```
The application will be running at `http://localhost:5173`.

### 3. Docker (Optional)

You can run the Database stack using Docker Compose:
```bash
docker compose up -d
```
## Usage
1.  Ensure backend (Port 8000) and frontend (Port 5173) are running.
2.  Open your browser to `http://localhost:5173`.
3.  Chat with the bot! It will remember your context.
    - *Example:* "Show me running shoes" -> "Which is the cheapest?"