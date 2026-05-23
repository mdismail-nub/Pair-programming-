from functools import lru_cache

import chromadb
from sentence_transformers import SentenceTransformer

CONCEPT_DOCS = {
    "python": "Python concepts: variables store values, loops repeat actions, functions encapsulate reusable logic, lists are ordered collections, dicts are key-value maps, classes model objects and behaviors, error handling uses try/except to manage runtime issues.",
    "javascript": "JavaScript concepts: variables with let/const hold data, arrays store ordered values, functions define reusable behavior, async/await simplifies asynchronous code, DOM manipulation updates web pages, promises handle async results.",
    "c++": "C++ concepts: variables define typed data, loops repeat execution, functions organize logic, arrays hold fixed-size sequences, pointers store memory addresses, classes define object-oriented structures and methods.",
}


@lru_cache(maxsize=1)
def _init_store():
    client = chromadb.Client()
    collection = client.get_or_create_collection("codemate_concepts")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    for lang, text in CONCEPT_DOCS.items():
        emb = model.encode([text])[0].tolist()
        collection.upsert(
            ids=[lang],
            embeddings=[emb],
            documents=[text],
            metadatas=[{"language": lang}],
        )

    return collection, model


def get_relevant_context(query: str, language: str) -> list[str]:
    try:
        collection, model = _init_store()
        query_emb = model.encode([query])[0].tolist()
        result = collection.query(
            query_embeddings=[query_emb],
            n_results=3,
            where={"language": language.lower()},
        )
        docs = result.get("documents", [[]])[0]
        return docs[:3]
    except Exception:
        # RAG is optional; fail gracefully.
        return [CONCEPT_DOCS.get(language.lower(), "")]
