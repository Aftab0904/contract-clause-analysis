from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

# -------------------------------
# CLAUSE TYPES (10 REQUIRED)
# -------------------------------
CLAUSE_TYPES = [
    "Governing Law",
    "Termination",
    "Liability",
    "Non-Compete",
    "IP Ownership",
    "Audit Rights",
    "Revenue Sharing",
    "Confidentiality",
    "Indemnity",
    "Limitation of Liability"
]

# -------------------------------
# LLM SETUP
# -------------------------------
def get_llm():
    return ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.3-70b-versatile",
        temperature=0
    )

# -------------------------------
# FEW-SHOT PROMPTING EXAMPLES
# -------------------------------
EXAMPLES = """
Example 1:
Clause Type: Governing Law
Context: This agreement shall be governed by the laws of California.
Output: This agreement shall be governed by the laws of California.

Example 2:
Clause Type: Termination
Context: Either party may terminate this agreement with 30 days written notice.
Output: Either party may terminate this agreement with 30 days written notice.

Example 3:
Clause Type: Liability
Context: The company shall not be liable for indirect damages.
Output: The company shall not be liable for indirect damages.
"""

# -------------------------------
# CLAUSE EXTRACTION FUNCTION
# -------------------------------
def extract_clause(vectorstore, clause_type, contract_id=None):

    llm = get_llm()

    # Step 1: retrieve relevant chunks
    docs = vectorstore.similarity_search(clause_type, k=5)

    # Step 2: filter by contract (IMPORTANT )
    if contract_id:
        docs = [d for d in docs if d.metadata.get("source") == contract_id]

    # fallback if nothing found after filtering
    if not docs:
        return "Not Found", []

    # Step 3: build context
    context = "\n".join([d.page_content for d in docs])

    # Step 4: extract sources
    sources = [
        f"{d.metadata.get('source')} - Para {d.metadata.get('paragraph')}"
        for d in docs
    ]

    # Step 5: prompt
    prompt = f"""
You are a legal expert specializing in contract analysis.

Your task is to extract a specific clause from the contract.

{EXAMPLES}

Now extract the clause.

Clause Type: {clause_type}

Rules:
- Return ONLY the exact clause text
- Do NOT summarize
- Do NOT explain
- If not found, return "Not Found"

Context:
{context}
"""

    response = llm.invoke(prompt)

    return response.content.strip(), sources