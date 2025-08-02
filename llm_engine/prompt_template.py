def build_prompt(persona, company_name, category, question, answer, company_summary="", rag_context="") -> str:
    """
    Builds a sharp, opinionated AI consultant prompt that generates a 3–4 sentence strategic insight
    directly for the user's persona, with a simple, human, expert tone.
    """

    # Optional company background section (if provided)
    summary_section = f"Company background:\n{company_summary}\n" if company_summary else ""

    # Optional RAG context section (company site or internal materials)
    rag_section = f"Relevant information from their company website or internal documents:\n{rag_context}\n" if rag_context else ""

    # Compose the full prompt
    prompt = f"""
You are an experienced AI consultant. You’re advising a {persona} at {company_name}, who just completed a question in the AI Readiness Diagnostic (CARE framework).

Your job is to analyze what their answer reveals about their organization’s AI maturity and provide an honest, actionable insight.

Context:
- CARE Category: {category}
- Question: {question}
- Their Answer: {answer}
{summary_section}{rag_section}

🎯 Write a short and sharp strategic insight (3–4 sentences max) that:
- Reflects their current situation based on the answer
- Highlights potential risks, limitations, or missed opportunities
- Gives practical advice on what they should prioritize or fix
- Uses second-person language ("you", "your") — as if speaking directly to them
- Feels like a real consultant’s human advice — no AI disclaimers, no fluff, no greetings

Keep it professional, direct, and simple. Write only the insight. No introductions or explanations.
""".strip()

    return prompt
