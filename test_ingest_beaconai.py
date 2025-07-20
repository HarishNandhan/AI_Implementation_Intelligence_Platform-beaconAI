from llm_engine.rag_engine import ingest_beaconai_context

# List of BeaconAI site pages to ingest
urls = [
    "https://beaconai.consulting/",
    "https://beaconai.consulting/services",
    "https://beaconai.consulting/approach",
    "https://beaconai.consulting/about",
    "https://beaconai.consulting/resources",
    "https://beaconai.consulting/contact"
]

chunks = ingest_beaconai_context("BeaconAI", urls)
print(f"✅ Ingested {chunks} chunks from BeaconAI into FAISS.")
