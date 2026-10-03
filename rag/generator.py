import os

from groq import Groq


MODEL_NAME = "openai/gpt-oss-120b"


def generate_grounded_answer(
    user_question,
    rag_context
):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is not set."
        )

    client = Groq(api_key=api_key)

    system_prompt = """
You are AwaamiAgent, a civic assistance AI.

Your job is to help citizens understand civic problems
using the provided retrieved evidence.

IMPORTANT RULES:

1. Use the retrieved evidence as the primary source of information.
2. Do not invent laws, procedures, authorities, deadlines,
   fees, addresses, phone numbers, or government departments.
3. Do not treat information as verified if its
   verification_status is not verified.
4. If the retrieved evidence does not provide enough information,
   clearly say that the information needs to be verified from
   the current official source.
5. Do not make unsupported assumptions about the user's location
   or jurisdiction.
6. Keep the answer practical and easy to understand.
7. Mention the relevant source information when available.
"""

    user_prompt = f"""
CITIZEN'S QUESTION:
{user_question}

RETRIEVED CIVIC EVIDENCE:
{rag_context}

Based only on the evidence above, provide a helpful answer.

Clearly distinguish between:
- information supported by the retrieved evidence
- information that still needs verification
"""

    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0.2
    )

    return completion.choices[0].message.content
