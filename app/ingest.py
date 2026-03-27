import json
from langchain_core.documents import Document

# load JSON dataset
def load_cuad_dataset(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data["data"]


# convert contracts into documents
def convert_to_documents(dataset, limit=5):

    docs = []

    for contract in dataset[:limit]:
        paragraphs = contract["paragraphs"]

        for para in paragraphs:
            text = para["context"]

            docs.append(Document(page_content=text))

    return docs