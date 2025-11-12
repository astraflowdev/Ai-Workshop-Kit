"""
Project 4: Simple RAG System
Document Q&A using Retrieval Augmented Generation

This is a starter template. You'll build this in weeks 2-4!
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config import Config
from utils.helpers import print_colored

print_colored("=" * 70, "cyan")
print_colored("SIMPLE RAG SYSTEM - Project 4 (Starter Template)", "green")
print_colored("=" * 70, "cyan")
print("\nThis is a starter template for your RAG system.")
print("Follow the README.md for step-by-step instructions!\n")

# TODO: Install required packages
# pip install langchain chromadb pypdf tiktoken

try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.embeddings import OpenAIEmbeddings
    from langchain.vectorstores import Chroma
    from openai import OpenAI

    client = Config.get_openai_client()

    print_colored("✓ All dependencies installed!", "green")

except ImportError as e:
    print_colored(f"✗ Missing dependency: {e}", "red")
    print("\nPlease install required packages:")
    print("pip install langchain chromadb pypdf tiktoken")
    sys.exit(1)


# STEP 1: Prepare sample documents
print_colored("\n[STEP 1] Preparing sample documents...", "yellow")

sample_documents = [
    {
        "content": "Our company offers 20 days of paid vacation per year. "
        "Employees must request vacation at least 2 weeks in advance. "
        "Unused vacation days can be carried over to the next year.",
        "metadata": {"source": "handbook", "page": 1},
    },
    {
        "content": "The remote work policy allows employees to work from home "
        "up to 3 days per week. A proper home office setup is required. "
        "Core hours are 10 AM to 4 PM local time.",
        "metadata": {"source": "handbook", "page": 2},
    },
    {
        "content": "Health insurance is provided to all full-time employees. "
        "Coverage includes medical, dental, and vision. "
        "Dependents can be added for an additional fee.",
        "metadata": {"source": "handbook", "page": 3},
    },
]

print_colored(f"✓ Loaded {len(sample_documents)} document chunks", "green")


# STEP 2: Create embeddings and vector store
print_colored("\n[STEP 2] Creating embeddings and vector store...", "yellow")

try:
    # Initialize embeddings
    embeddings = OpenAIEmbeddings()

    # Create text list and metadata list
    texts = [doc["content"] for doc in sample_documents]
    metadatas = [doc["metadata"] for doc in sample_documents]

    # Create vector store
    vectorstore = Chroma.from_texts(
        texts=texts, metadatas=metadatas, embedding=embeddings
    )

    print_colored("✓ Vector store created successfully!", "green")

except Exception as e:
    print_colored(f"✗ Error creating vector store: {e}", "red")
    sys.exit(1)


# STEP 3: Query the system
print_colored("\n[STEP 3] Ready to answer questions!", "green")
print_colored("=" * 70, "cyan")
print("\nTry asking:")
print("  - What is the vacation policy?")
print("  - How many days can I work from home?")
print("  - Tell me about health insurance")
print("\nType 'quit' to exit\n")


def answer_question(question: str) -> str:
    """Query the RAG system"""

    # Step 1: Retrieve relevant chunks
    relevant_docs = vectorstore.similarity_search(question, k=2)

    # Step 2: Create context from retrieved chunks
    context = "\n\n".join([doc.page_content for doc in relevant_docs])

    # Show what was retrieved
    print_colored(f"\n[Retrieved {len(relevant_docs)} relevant chunks]", "yellow")

    # Step 3: Query LLM with context
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. Answer the question based "
                "on the provided context. If the answer is not in the context, "
                "say 'I don't have information about that in the documents.'",
            },
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
    )

    return response.choices[0].message.content


# Main loop
while True:
    user_question = input("Your Question: ")

    if user_question.lower() in ["quit", "exit"]:
        print_colored("\nGoodbye!", "green")
        break

    if not user_question.strip():
        continue

    try:
        answer = answer_question(user_question)
        print_colored(f"\nAnswer: {answer}\n", "green")

    except Exception as e:
        print_colored(f"\nError: {e}", "red")


print_colored("\n" + "=" * 70, "cyan")
print_colored("Next Steps:", "yellow")
print("1. Load real PDFs instead of sample documents")
print("2. Implement better chunking strategies")
print("3. Add metadata filtering")
print("4. Build a web interface with Streamlit")
print("\nSee README.md for detailed instructions!")
print_colored("=" * 70, "cyan")
