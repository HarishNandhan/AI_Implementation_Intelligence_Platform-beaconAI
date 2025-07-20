def build_prompt(persona, company_name, category, question, answer, company_summary="", rag_context="") -> str:
    """
    Builds a smart, persona-aware insight prompt with second-person, role-based, expert tone.
    """
    # Optional content
    summary_section = f"Company background:\n{company_summary}\n" if company_summary else ""
    rag_section = f"Additional context from the company website or materials:\n{rag_context}\n" if rag_context else ""

    prompt = f"""
You are an experienced AI consultant with many years of domain-specific experience across multiple industries. You are now preparing an insight for a {persona} from the company {company_name} who has just completed an AI Readiness Diagnostic using the CARE framework (Culture, Adoption, Readiness, Evolution).

Write a message **directly to** the {persona} — using **second-person tone** ("you", "your") — as if you're advising them personally.

Use the following information:
- Category: {category}
- Question: {question}
- Answer: {answer}
{summary_section}{rag_section}

🎯 Please generate a strategic insight (3-5 sentences) that:
1. Starts with their current state based on the answer
2. Highlights risks, gaps, or inefficiencies specific to their company
3. Ends with specific, persona-relevant advice or next steps
4. Feels like direct expert advice, not a formal letter

Write in a professional, direct tone. Do NOT include greetings, closings, signatures, or formal letter formatting. Focus only on the strategic insight content.
""".strip()

    return prompt
