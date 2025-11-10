# ARCHITECTURE.md

## 1. Document Ingestion

**Endpoint:** `/ingest`  

**Functionality:**  
- Accepts `.txt` or `.md` files  
- Validates files and stores content in the database  

**Vector Storage:**  
- Uses the `pgvector` extension in PostgreSQL to store **32-dimensional embeddings**  
- Long documents are **chunked** to improve semantic search relevance and reduce noise  

**Embedding:**  
- `mock_embed` function simulates embeddings (SHA256 → vector)  
- In production, OpenAI embeddings or another LLM would be used  

---

## 2. Query / Ask Endpoint

**Endpoint:** `/ask`  

**Functionality:**  
- Accepts a user query  
- Retrieves relevant document chunks from the database  
- Generates a response  

**Semantic Search:**  
- Retrieves top-N most similar chunks using cosine similarity in the vector database  

**Response Generation:**  
- Uses `mock_generate_answer` to simulate LLM output  
- Combines context from multiple chunks for coherent answers  

---

## 3. Tool Calling

The system detects queries requiring external tools:  

- `get_current_time(tz)` → returns current UTC or local time  
- `get_exchange_rate(base, target)` → fetches exchange rate via free API  

Responses from tools are **integrated back into the conversation**.  

---

## 4. Response Validation (Anti-Hallucination Layer)

- Validates generated answers against retrieved context  
- `validate_answer(answer, context)` checks if **significant words in the answer exist in the context**  
- Prevents unrelated or unsupported answers  
- If validation fails, the system gracefully refuses to answer:  

> “Sorry, I cannot answer this question based on available information.”  

---

## 5. How to Run

**1. Build and start Docker containers**  

```bash
docker compose build
docker compose up -d
docker compose exec -it app sh -c "alembic upgrade head"