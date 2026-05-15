import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaLLM

CHROMA_DIR = "data/metadata/chroma_db"
OLLAMA_MODEL = "llama3.2:3b"

def get_answer(question):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
    docs = vectorstore.similarity_search(question, k=6)

    context_parts = []
    for i, doc in enumerate(docs):
        source = doc.metadata.get('source', 'unknown')
        label = os.path.splitext(os.path.basename(source))[0][:40]
        content = doc.page_content[:1000]
        if len(doc.page_content) > 1000:
            content += "..."
        context_parts.append(f"[Document: {label}]\n{content}")
    context = "\n\n---\n\n".join(context_parts)

    prompt = f"""You are given excerpts from several documents. Answer the user's question based ONLY on these excerpts. Do not add external knowledge.

Excerpts:
{context}

User question: {question}

Follow the user's instructions exactly. If the user asks for a table, produce a markdown table. If they ask for bullet points, use bullets. If they ask to compare specific entities, use the names as they appear in the excerpts. If the information is not present, say "Not mentioned in the provided documents."

Answer:
"""
    llm = OllamaLLM(model=OLLAMA_MODEL, temperature=0.0)
    answer = llm.invoke(prompt)
    return answer

if __name__ == "__main__":
    q = input("Ask a question: ")
    ans = get_answer(q)
    print("\nAnswer:", ans)