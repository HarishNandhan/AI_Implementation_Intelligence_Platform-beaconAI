def build_prompt(persona: str, company_name: str, category: str, question: str, answer: str, company_summary: str = "") -> str:
    """
    Builds a persona-aware, context-rich prompt for the LLM.
    """

    prompt = f"""
You are an expert AI strategy consultant.

A user from **{company_name}** has completed an AI Readiness Diagnostic using the CARE framework: Culture, Adoption, Readiness, and Evolution.
They identified themselves as a **{persona}**. Your response must be customized to their role.

Here is the question and their response:
- **Category:** {category}
- **Question:** {question}
- **Answer:** {answer}

Company background:
{company_summary or "No additional company context provided."}

---

Please follow this logic when generating your insight:

If the persona is:
- CTO → Focus on governance, data pipelines, experimentation safety, system integration
- CMO → Focus on personalization, customer engagement, AI in campaigns, ROI
- CHRO / HR → Focus on employee readiness, upskilling, policy and training gaps
- COO → Focus on operational efficiency, workflow automation, scaling processes
- CEO / Strategy → Focus on vision alignment, industry positioning, long-term transformation
- Other → Use a general tone, highlight cross-functional readiness and value impact

---

Now write a brief strategic paragraph (3–5 sentences) that includes:
1. The current state of the organization based on the answer
2. The risks or limitations of that state
3. A recommended next step — specific to the persona's role

Make the tone professional, role-aware, and insightful.

Respond in the following format:

**Insight:** [Your paragraph here]
    """.strip()

    return prompt
