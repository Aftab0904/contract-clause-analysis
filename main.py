from app.ingest import load_cuad_dataset, convert_to_documents
from app.chunk import chunk_documents

# Step 1: Load dataset
data = load_cuad_dataset("data/contracts/CUADv1.json")

# Step 2: Convert to documents
docs = convert_to_documents(data, limit=20)

print("Total docs:", len(docs))
print("Sample doc:\n", docs[0].page_content[:300])

# Step 3: Chunking
chunks = chunk_documents(docs)

print("\nTotal chunks:", len(chunks))
print("Sample chunk:\n", chunks[0].page_content[:300])


# step 4:
from app.vectorstore import create_vectorstore

# Step 4: Create vector DB
vectorstore = create_vectorstore(chunks)

print("\nVector DB created successfully")

# Test retrieval
results = vectorstore.similarity_search("termination clause", k=5)

print("\nTop result:\n", results[0].page_content[:300])

from app.extract import extract_clause

print("\n--- Clause Extraction ---")

result = extract_clause(vectorstore, "Governing Law")

print("\nGoverning Law Clause:\n", result)