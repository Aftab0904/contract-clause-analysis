import streamlit as st
from dotenv import load_dotenv
import os

from app.ingest import load_cuad_dataset, convert_to_documents
from app.chunk import chunk_documents
from app.vectorstore import create_vectorstore
from app.extract import extract_clause, get_llm

load_dotenv()

# load dataset once
@st.cache_resource
def load_pipeline():
    data = load_cuad_dataset("data/contracts/CUADv1.json")
    docs = convert_to_documents(data, limit=3)
    chunks = chunk_documents(docs)
    vectorstore = create_vectorstore(chunks)
    return vectorstore

vectorstore = load_pipeline()
llm = get_llm()

st.title("Contract Clause Analysis System")

st.sidebar.title("Options")
mode = st.sidebar.selectbox(
    "Choose functionality",
    ["Ask Question", "Extract Clause", "Risk Detection"]
)

# -------------------------------
# QA SYSTEM
# -------------------------------
if mode == "Ask Question":

    query = st.text_input("Enter your question")

    if st.button("Run Query"):

        docs = vectorstore.similarity_search(query, k=3)
        context = "\n".join([d.page_content for d in docs])

        prompt = f"""
Answer the question based on the contract.

Context:
{context}

Question:
{query}
"""

        response = llm.invoke(prompt)

        st.subheader("Answer")
        st.write(response.content)


# -------------------------------
# CLAUSE EXTRACTION
# -------------------------------
elif mode == "Extract Clause":

    clause = st.selectbox(
        "Select Clause Type",
        ["Governing Law", "Non-Compete", "Termination", "Liability"]
    )

    if st.button("Extract"):

        result = extract_clause(vectorstore, clause)

        st.subheader("Extracted Clause")
        st.write(result)


# -------------------------------
# RISK DETECTION
# -------------------------------
elif mode == "Risk Detection":

    if st.button("Check Risk"):

        prompt = """
You are a legal expert.

Analyze the contract and identify risks.

Check for:
- No cap on liability
- No termination clause
- Unbalanced obligations

Return concise risks.
"""

        docs = vectorstore.similarity_search("contract risks", k=5)
        context = "\n".join([d.page_content for d in docs])

        response = llm.invoke(prompt + "\n\nContext:\n" + context)

        st.subheader("Risk Analysis")
        st.write(response.content)