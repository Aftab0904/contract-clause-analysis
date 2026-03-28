import streamlit as st
from dotenv import load_dotenv
import os

from app.ingest import load_cuad_dataset, convert_to_documents
from app.chunk import chunk_documents
from app.vectorstore import create_vectorstore
from app.extract import extract_clause, get_llm, CLAUSE_TYPES

# -------------------------------
# FAITHFULNESS EVALUATION FUNCTION
# -------------------------------
def evaluate_faithfulness(context, answer, llm):
    prompt = f"""
You are an evaluator.

Check if the answer is fully supported by the context.

Context:
{context}

Answer:
{answer}

Score from 0 to 1:
0 = completely incorrect
1 = fully supported

Return ONLY a number.
"""
    score = llm.invoke(prompt).content.strip()
    return score

# -------------------------------
# SAMPLE CONTRACTS FUNCTION
# -------------------------------
@st.cache_data
def get_sample_contracts():
    data = load_cuad_dataset("data/contracts/CUADv1.json")
    return data[:5]

# -------------------------------
# LOAD ENV
# -------------------------------
load_dotenv()

# -------------------------------
# LOAD PIPELINE
# -------------------------------
@st.cache_resource
def load_pipeline():
    data = load_cuad_dataset("data/contracts/CUADv1.json")
    docs = convert_to_documents(data, limit=20)
    chunks = chunk_documents(docs)
    vectorstore = create_vectorstore(chunks)
    return vectorstore

vectorstore = load_pipeline()
llm = get_llm()

# -------------------------------
# UI TITLE
# -------------------------------
st.title("Contract Clause Analysis System")
st.markdown("### AI-powered contract analysis system")

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.title("Options")

mode = st.sidebar.selectbox(
    "Choose functionality",
    ["Ask Question", "Extract Clause", "Risk Detection"]
)

show_contracts = st.sidebar.button("Show Sample Contracts")

# -------------------------------
# SHOW SAMPLE CONTRACTS
# -------------------------------
if show_contracts:
    contracts = get_sample_contracts()

    st.subheader("Sample Contracts (First 5 from dataset)")

    for i, contract in enumerate(contracts):
        st.markdown(f"### Contract {i+1}")

        paragraphs = contract["paragraphs"]

        for para in paragraphs[:2]:
            st.write(para["context"])

        st.markdown("---")

# -------------------------------
# QA SYSTEM
# -------------------------------
if mode == "Ask Question":

    contract_id = st.selectbox(
        "Select Contract",
        [f"Contract_{i}" for i in range(20)]
    )

    query = st.text_input("Enter your question")

    if st.button("Run Query"):

        docs = vectorstore.similarity_search(query, k=20)

        filtered_docs = [d for d in docs if d.metadata.get("source") == contract_id]

        if not filtered_docs:
            st.warning("No relevant context found for this contract. Showing general results.")
            docs = docs[:5]
        else:
            docs = filtered_docs

        context = "\n".join([d.page_content for d in docs])

        prompt = f"""
You are a legal assistant.

Answer the question ONLY using the provided contract context.

If the answer is not present, say "Not Found".

Context:
{context}

Question:
{query}
"""

        response = llm.invoke(prompt)

        st.subheader("Answer")
        st.write(response.content)

        # -------------------------------
        # FAITHFULNESS SCORE DISPLAY
        # -------------------------------
        score = evaluate_faithfulness(context, response.content, llm)

        st.subheader("Faithfulness Score")
        st.write(score)

# -------------------------------
# CLAUSE EXTRACTION
# -------------------------------
elif mode == "Extract Clause":

    contract_id = st.selectbox(
        "Select Contract",
        [f"Contract_{i}" for i in range(20)]
    )

    clause = st.selectbox("Select Clause Type", CLAUSE_TYPES)

    if st.button("Extract"):

        result, sources = extract_clause(vectorstore, clause, contract_id)

        st.subheader("Extracted Clause")
        st.info(result)

        st.markdown("---")
        st.write("Source Locations:")

        for s in sources:
            st.caption(f"- {s}")

# -------------------------------
# RISK DETECTION
# -------------------------------
elif mode == "Risk Detection":

    contract_id = st.selectbox(
        "Select Contract",
        [f"Contract_{i}" for i in range(20)]
    )

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

        docs = vectorstore.similarity_search("contract risks", k=20)

        filtered_docs = [d for d in docs if d.metadata.get("source") == contract_id]

        if not filtered_docs:
            docs = docs[:5]
        else:
            docs = filtered_docs

        context = "\n".join([d.page_content for d in docs])

        response = llm.invoke(prompt + "\n\nContext:\n" + context)

        st.subheader("Risk Analysis")
        st.write(response.content)