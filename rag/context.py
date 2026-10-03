def build_rag_context(results):
    if not results:
        return "No relevant civic evidence was retrieved."

    context_parts = []

    for i, result in enumerate(results, start=1):
        entry = result.get("entry", result)

        context_parts.append(
            f"""
SOURCE {i}

Title: {entry.get("title", "")}
Authority: {entry.get("authority", "")}
Source Name: {entry.get("source_name", "")}
Source URL: {entry.get("source_url", "")}
Source Type: {entry.get("source_type", "")}
Verification Status: {entry.get("verification_status", "")}
Similarity Score: {result.get("score", 0):.4f}

Content:
{entry.get("content", "")}
"""
        )

    return "\n".join(context_parts)
