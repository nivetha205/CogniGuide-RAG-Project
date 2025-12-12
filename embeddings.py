from sentence_transformers import SentenceTransformer


def get_embeddings_model():
    """Load embedding model."""
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return model


def embed_documents(documents, model):
    """Convert documents to embeddings."""
    texts = [doc.page_content for doc in documents]
    embeddings = model.encode(texts, show_progress_bar=True)
    return embeddings

