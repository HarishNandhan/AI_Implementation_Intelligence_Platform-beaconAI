from scraper.selenium_scraper import scrape_company_website
from vector_store.embedder import split_text_into_documents
from vector_store.faiss_index import VectorStore

vector_store = VectorStore()

def ingest_company_site(company_name: str, url: str) -> int:
    """
    Scrapes and embeds a company's website content into the FAISS vector store.

    Args:
        company_name (str): Name of the company
        url (str): Company site or About page

    Returns:
        int: Number of text chunks added
    """
    print(f"🧠 Ingesting content for {company_name} from {url}...")

    text = scrape_company_website(url)
    if not text or len(text) < 100:
        raise ValueError("No usable content found.")

    # Add company + source metadata
    docs = split_text_into_documents(
        text,
        metadata={"company": company_name, "source_url": url}
    )

    # Store in vector database
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

def generate_solution_section(insight_list: list[str]) -> str:
    """
    Takes all insight texts and asks the LLM how BeaconAI can solve these issues.
    """
    from llm_engine.llama_client import generate_llama_response

    summary_text = "\n".join(insight_list)
    context = retrieve_context("BeaconAI services and capabilities", k=5)
    joined_context = "\n".join(context)

    prompt = f"""
A client has received the following AI readiness insights:

{summary_text}

You are an expert at BeaconAI. Based on the above client challenges and the following information about BeaconAI's services:

{joined_context}

Write a professional 4–5 sentence summary of how BeaconAI can help this client.
End with an encouraging tone focused on capability and partnership.
    """.strip()

    return generate_llama_response(prompt)


def retrieve_context(query: str, k: int = 4):
    """
    Retrieves top-k relevant chunks from FAISS based on a user query.
    """
    relevant_docs = vector_store.search(query, k=k)
    return [doc.page_content for doc in relevant_docs]
