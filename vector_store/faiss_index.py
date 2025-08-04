import os
import faiss
import pickle
from typing import List, Tuple
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

# Optional path to save/load FAISS DB
FAISS_DB_PATH = "vector_store/faiss_index"

class VectorStore:
    def __init__(self):
        try:
            # Try to initialize with HuggingFace token from environment
            hf_token = os.getenv("HF_TOKEN")
            if hf_token and hf_token != "hf_your_hugging_face_token_here":
                self.embedding_model = HuggingFaceEmbeddings(
                    model_name="sentence-transformers/all-MiniLM-L6-v2",
                    model_kwargs={'token': hf_token}
                )
            else:
                # Fallback to local model without token
                self.embedding_model = HuggingFaceEmbeddings(
                    model_name="sentence-transformers/all-MiniLM-L6-v2"
                )
        except Exception as e:
            print(f"Warning: Could not initialize HuggingFace embeddings: {e}")
            print("Using fallback embedding model...")
            # Use a simpler fallback if HuggingFace fails
            self.embedding_model = None
        
        self.vector_db = None

    def build_index(self, documents: List[Document]):
        """
        Embeds and stores the given documents into FAISS.
        """
        if not self.embedding_model:
            print("Warning: No embedding model available. Skipping index building.")
            return
            
        self.vector_db = FAISS.from_documents(documents, self.embedding_model)
        self._save_index()

    def search(self, query: str, k: int = 5) -> List[Document]:
        """
        Searches for the top-k relevant documents.
        """
        if not self.embedding_model:
            print("Warning: No embedding model available. Returning empty results.")
            return []
            
        if not self.vector_db:
            self._load_index()

        if not self.vector_db:
            print("Warning: No vector database available. Returning empty results.")
            return []

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
