from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    return ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.3-70b-versatile",
        temperature=0
    )


def extract_clause(vectorstore, clause_type):

    llm = get_llm()

    # Step 1: relevant chunks retrieve karo
    docs = vectorstore.similarity_search(clause_type, k=3)

    context = "\n".join([d.page_content for d in docs])

    # Step 2: LLM se extract karwao
    prompt = f"""
You are a legal expert.

Extract the {clause_type} clause from the contract.

Rules:
- Return only the clause text
- If not found, say "Not Found"

Context:
{context}
"""

    response = llm.invoke(prompt)

    return response.content



# clases extraction