import os
import faiss
import pickle
from typing import List, Tuple
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document

# Optional path to save/load FAISS DB
FAISS_DB_PATH = "vector_store/faiss_index"

class VectorStore:
    def __init__(self):
        self.embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.vector_db = None

    def build_index(self, documents: List[Document]):
        """
        Embeds and stores the given documents into FAISS.
        """
        self.vector_db = FAISS.from_documents(documents, self.embedding_model)
        self._save_index()

    def search(self, query: str, k: int = 5) -> List[Document]:
        """
        Searches for the top-k relevant documents.
        """
        if not self.vector_db:
            self._load_index()

        return self.vector_db.similarity_search(query, k=k)

    def _save_index(self):
        """
        Saves FAISS index and document store to disk.
        """
        if self.vector_db:
            self.vector_db.save_local(FAISS_DB_PATH)

    def _load_index(self):
        """
        Loads existing FAISS index from disk.
        """
        if os.path.exists(FAISS_DB_PATH):
            self.vector_db = FAISS.load_local(
                FAISS_DB_PATH,
                self.embedding_model,
                allow_dangerous_deserialization=True
            )
        else:
            raise ValueError("FAISS index not found. Please build it first.")
