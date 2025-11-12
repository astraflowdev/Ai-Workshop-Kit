# Project 4: RAG System (Document Q&A)

**Timeline:** 2-4 weeks to complete
**Difficulty:** 🌶️🌶️🌶️ Intermediate+

## What is RAG?

**RAG = Retrieval Augmented Generation**

It solves a key problem: LLMs can't answer questions about YOUR specific documents.

### The Problem
```
You: "What does page 47 of our company handbook say about vacation policy?"
ChatGPT: "I don't have access to your company handbook."
```

### The Solution: RAG
```
Your Documents → Chunk & Embed → Store in Vector DB
                                        ↓
User Question → Find Similar Chunks → Send to LLM → Get Answer!
```

## How RAG Works

### 1. Document Processing (One-time Setup)
```
1. Load documents (PDF, DOCX, TXT, etc.)
2. Split into chunks (500-1000 characters each)
3. Create embeddings (convert text → vectors)
4. Store in vector database
```

### 2. Query Processing (Each Question)
```
1. User asks a question
2. Convert question to embedding
3. Search for similar chunks (semantic search)
4. Send relevant chunks + question to LLM
5. LLM generates answer using the chunks
```

## Architecture

```
┌─────────────────────┐
│  Your Documents     │
│  (PDF/DOCX/TXT)     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Text Extraction    │
│  & Chunking         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Embeddings         │
│  (OpenAI ada-002)   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Vector Database    │
│  (Pinecone/Chroma)  │
└─────────────────────┘
           │
           ▼
┌─────────────────────┐
│  User Question      │ ────┐
└─────────────────────┘     │
                            │
                            ▼
                ┌───────────────────┐
                │  Similarity Search│
                └─────────┬─────────┘
                          │
                          ▼
                ┌───────────────────┐
                │  Relevant Chunks  │
                └─────────┬─────────┘
                          │
                          ▼
                ┌───────────────────┐
                │  LLM + Context    │
                │  Generate Answer  │
                └─────────┬─────────┘
                          │
                          ▼
                ┌───────────────────┐
                │  Final Answer     │
                └───────────────────┘
```

## Tech Stack

### Embeddings
- **OpenAI `text-embedding-ada-002`** (Recommended)
- Cost: $0.0001 per 1K tokens (very cheap!)

### Vector Databases
1. **ChromaDB** - Local, free, great for learning
2. **Pinecone** - Cloud, free tier (1 index, 100K vectors)
3. **FAISS** - Facebook's library, local, fast

### Document Processing
- **LangChain** - Document loaders and text splitters
- **PyPDF2** - PDF processing
- **python-docx** - Word documents
- **tiktoken** - Token counting

### Frontend (Optional)
- **Streamlit** - Quick web UI
- **Gradio** - Alternative UI
- **React** - For production apps

## Files

- `simple_rag.py` - Basic RAG implementation
- `rag_with_chromadb.py` - Using ChromaDB
- `rag_streamlit_app.py` - Web interface
- `document_processor.py` - Document loading utilities

## Quick Start

```bash
# Install dependencies
pip install langchain chromadb openai pypdf tiktoken streamlit

# Run simple RAG
python simple_rag.py

# Run web app
streamlit run rag_streamlit_app.py
```

## Code Example

### Step 1: Load and Chunk Documents

```python
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load PDF
loader = PyPDFLoader("document.pdf")
documents = loader.load()

# Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = text_splitter.split_documents(documents)
```

### Step 2: Create Embeddings and Store

```python
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

# Create embeddings
embeddings = OpenAIEmbeddings()

# Store in ChromaDB
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)
```

### Step 3: Query

```python
# User question
question = "What is the vacation policy?"

# Similarity search
relevant_docs = vectorstore.similarity_search(question, k=3)

# Create context from retrieved chunks
context = "\n\n".join([doc.page_content for doc in relevant_docs])

# Query LLM with context
from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": "Answer the question based on the context provided. "
                      "If the answer is not in the context, say so."
        },
        {
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {question}"
        }
    ]
)

print(response.choices[0].message.content)
```

## Best Practices

### 1. Chunking Strategy
```python
# Good chunk size: 500-1000 characters
# Good overlap: 100-200 characters

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150,
    separators=["\n\n", "\n", " ", ""]  # Split on paragraphs first
)
```

### 2. Metadata
```python
# Add metadata to chunks for filtering
chunks = text_splitter.create_documents(
    texts=[doc.page_content for doc in documents],
    metadatas=[{"source": doc.metadata["source"], "page": i}
               for i, doc in enumerate(documents)]
)
```

### 3. Hybrid Search
```python
# Combine semantic search with keyword search
results = vectorstore.similarity_search(
    question,
    k=5,
    filter={"source": "handbook.pdf"}  # Filter by source
)
```

## Use Cases

1. **Customer Support** - Answer questions from documentation
2. **Legal** - Search contracts and legal documents
3. **Research** - Query research papers
4. **Internal Knowledge Base** - Company wikis and handbooks
5. **Education** - Textbook Q&A systems

## Performance Tips

### 1. Choose Right Chunk Size
- Small chunks (300-500): Precise, but might miss context
- Large chunks (1000-1500): More context, but less precise

### 2. Optimize Retrieval
```python
# Retrieve more chunks, re-rank later
initial_docs = vectorstore.similarity_search(question, k=10)

# Re-rank using a reranker model (optional)
final_docs = reranker.rerank(initial_docs, question)[:3]
```

### 3. Cost Optimization
```python
# Embeddings are cheap, but add up
# Cache embeddings for static documents
# Use smaller chunks to reduce LLM context cost
```

## Common Challenges

### 1. Context Window Limits
- Solution: Retrieve fewer, more relevant chunks
- Use summarization for very long documents

### 2. Answer Quality
- Solution: Improve chunk quality
- Add metadata and filters
- Use better prompts

### 3. Speed
- Solution: Use FAISS for faster search
- Implement caching
- Use async processing

## Learning Resources

- **LangChain Docs**: https://python.langchain.com/docs/use_cases/question_answering/
- **Pinecone Learning Center**: RAG tutorials
- **"Retrieval Augmented Generation" paper**: Original RAG research

## Next Steps

1. **Week 1**: Build basic RAG with single PDF
2. **Week 2**: Add web interface with Streamlit
3. **Week 3**: Implement advanced features (metadata filtering, re-ranking)
4. **Week 4**: Deploy to production

After mastering RAG, move on to **Project 5: Multi-Agent Systems**!

---

**Starter Code**: See `simple_rag.py` to get started
**Web App**: Run `streamlit run rag_streamlit_app.py`
**Documentation**: Full code comments and examples included
