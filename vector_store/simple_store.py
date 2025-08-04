"""
Simple fallback vector store that doesn't require HuggingFace
"""
import os
from typing import List

class SimpleVectorStore:
    def __init__(self):
        # Simple keyword-based search as fallback
        self.documents = []
        
    def build_index(self, documents):
        """Store documents for simple keyword search"""
        self.documents = [doc.page_content if hasattr(doc, 'page_content') else str(doc) for doc in documents]
        
    def search(self, query: str, k: int = 5) -> List[str]:
        """Simple keyword-based search"""
        if not self.documents:
            return []
            
        # Simple keyword matching
        query_words = query.lower().split()
        scored_docs = []
        
        for doc in self.documents:
            doc_lower = doc.lower()
            score = sum(1 for word in query_words if word in doc_lower)
            if score > 0:
                scored_docs.append((score, doc))
        
        # Sort by score and return top k
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in scored_docs[:k]]