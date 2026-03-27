from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_documents(docs):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,      # thoda bada (legal docs)
        chunk_overlap=200     # context preserve
    )

    chunks = splitter.split_documents(docs)

    return chunks