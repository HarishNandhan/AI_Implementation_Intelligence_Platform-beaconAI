from scraper.selenium_scraper import scrape_company_website
from vector_store.embedder import split_text_into_documents
from llm_engine.llama_client import generate_llama_response

# Try to initialize vector store with fallback
try:
    from vector_store.faiss_index import VectorStore
    vector_store = VectorStore()
    print("✅ Vector store initialized successfully")
except Exception as e:
    print(f"⚠️ Warning: Could not initialize vector store: {e}")
    print("Using simple fallback store...")
    from vector_store.simple_store import SimpleVectorStore
    vector_store = SimpleVectorStore()

def ingest_company_site(company_name: str, url: str) -> int:
    """
    Scrapes and embeds a company's website content into the FAISS vector store.
    """
    print(f"🧠 Ingesting content for {company_name} from {url}...")

    text = scrape_company_website(url)
    if not text or len(text) < 100:
        raise ValueError("No usable content found.")

    docs = split_text_into_documents(
        text,
        metadata={"company": company_name, "source_url": url}
    )

    vector_store.build_index(docs)
    return len(docs)

def ingest_beaconai_context(name: str, urls: list[str]) -> int:
    """
    Scrapes multiple BeaconAI pages and stores them as vector context in FAISS.
    """
    all_text = ""
    for url in urls:
        text = scrape_company_website(url)
        all_text += f"\n\nFrom {url}:\n{text}"

    docs = split_text_into_documents(all_text, metadata={"company": name})
    vector_store.build_index(docs)
    return len(docs)

def retrieve_context(query: str, k: int = 4) -> list[str]:
    """
    Retrieves top-k relevant chunks from FAISS based on a user query.
    """
    try:
        relevant_docs = vector_store.search(query, k=k)
        if hasattr(relevant_docs[0], 'page_content'):
            return [doc.page_content for doc in relevant_docs]
        else:
            # Simple store returns strings directly
            return relevant_docs
    except Exception as e:
        print(f"Warning: Could not retrieve context: {e}")
        return ["BeaconAI provides AI implementation consulting and training services."]

def generate_solution_section(insight_list: list[str], company_context: str) -> str:
    """
    Generates a BeaconAI solution summary based on user's AI readiness insights and the company's website content.
    """
    summary_text = "\n".join(insight_list)
    beaconai_context = "\n".join(retrieve_context("BeaconAI services and capabilities", k=5))

    prompt = f"""
You are a BeaconAI solutions consultant.

A client has received the following AI readiness insights:

{summary_text}

These reflect the real issues they are facing in AI culture, tooling, literacy, and long-term planning.

Below is a curated extract from their company website that describes their current operations and focus areas:

{company_context}

And here’s an overview of BeaconAI’s actual services and capabilities:

{beaconai_context}

🎯 Now, write a clear 7–8 sentence solution summary that:
- Speaks directly to the client using "you" and "your" (second-person tone)
- Describes what we (BeaconAI) will do to support their AI transformation
- Connects our services directly to the gaps identified in their responses
- Provides realistic 2–3 year improvements if they adopt our solution
- Avoids vague jargon, buzzwords, or inflated promises

This will be used in their official PDF report. Begin directly with the core message.
""".strip()

    return generate_llama_response(prompt)
