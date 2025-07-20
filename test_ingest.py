# test_ingest.py
from llm_engine.rag_engine import ingest_company_site

chunks = ingest_company_site("BeaconAI", "https://beaconai.consulting/about")
print(f"✅ Ingested {chunks} chunks into FAISS.")
