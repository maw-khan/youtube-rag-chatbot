from sentence_transformers import (
    CrossEncoder
)


reranker_model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def rerank_documents(
    query,
    docs
):

    pairs = [
        (query, doc.page_content)
        for doc in docs
    ]

    scores = reranker_model.predict(
        pairs
    )

    scored_docs = list(
        zip(docs, scores)
    )

    scored_docs.sort(
        key=lambda x: x[1],
        reverse=True
    )

    reranked_docs = [
        doc for doc, score in scored_docs
    ]

    return reranked_docs
