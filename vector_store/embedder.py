from typing import List
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_text_into_documents(text: str, metadata: dict = None) -> List[Document]:
    """
    Splits a long string of text into chunks and wraps them as LangChain Documents.
    
    Args:
        text (str): Raw text from a company website
        metadata (dict): Optional metadata like company_name, source_url
    
    Returns:
        List[Document]: Chunked and wrapped as LangChain Document objects
    """
    if not metadata:
        metadata = {}

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " "]
    )

    chunks = splitter.split_text(text)

    documents = [
        Document(page_content=chunk, metadata=metadata)
        for chunk in chunks
    ]

    return documents
