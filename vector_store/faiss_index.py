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
            # Use HuggingFace embeddings with same token as LLM
            hf_token = os.getenv("HF_TOKEN")  # Same token as LLM
            
            if hf_token and hf_token not in ["hf_your_hugging_face_token_here", "your_hugging_face_token_here"]:
                # Use HuggingFace with token
                self.embedding_model = HuggingFaceEmbeddings(
                    model_name="sentence-transformers/all-MiniLM-L6-v2",
                    model_kwargs={'token': hf_token}
                )
                print("✅ HuggingFace embeddings initialized with HF_TOKEN")
            else:
                # Fallback to local model without token
                print("⚠️ HF_TOKEN not found, using local embeddings")
                self.embedding_model = HuggingFaceEmbeddings(
                    model_name="sentence-transformers/all-MiniLM-L6-v2"
                )
                print("✅ HuggingFace embeddings initialized locally")
                
        except Exception as e:
            print(f"Warning: Could not initialize HuggingFace embeddings: {e}")
            print("Embeddings will use fallback content only")
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
            print("Warning: No embedding model available. Using simple fallback.")
            # Return some default context instead of empty results
            fallback_docs = [
                Document(page_content="BeaconAI provides AI implementation consulting and strategic guidance for organizations looking to adopt artificial intelligence technologies."),
                Document(page_content="Our CARE framework evaluates Culture, Adoption, Readiness, and Evolution aspects of AI implementation."),
                Document(page_content="We help companies develop AI strategies, implement solutions, and train teams for successful AI transformation.")
            ]
            return fallback_docs[:k]
            
        if not self.vector_db:
            try:
                self._load_index()
            except:
                print("Warning: Could not load vector database. Using fallback content.")
                return self._get_fallback_content(k)

        if not self.vector_db:
            return self._get_fallback_content(k)

        try:
            return self.vector_db.similarity_search(query, k=k)
        except Exception as e:
            print(f"Warning: Vector search failed: {e}. Using fallback content.")
            return self._get_fallback_content(k)
    
    def _get_fallback_content(self, k: int = 5) -> List[Document]:
        """Return fallback content when vector search is not available"""
        fallback_docs = [
            Document(page_content="BeaconAI provides AI implementation consulting and strategic guidance."),
            Document(page_content="Our CARE framework evaluates Culture, Adoption, Readiness, and Evolution."),
            Document(page_content="We help companies develop AI strategies and implement solutions."),
            Document(page_content="AI readiness assessment helps organizations prepare for AI transformation."),
            Document(page_content="Strategic AI planning ensures successful technology adoption and ROI.")
        ]
        return fallback_docs[:k]

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
