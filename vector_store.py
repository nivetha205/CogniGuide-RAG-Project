import chromadb


def create_vector_store(documents, embeddings, collection_name="cogniguide"):
    """Store documents in ChromaDB."""
    client = chromadb.Client()
    collection = client.get_or_create_collection(name=collection_name)


    for i, (doc, embedding) in enumerate(zip(documents, embeddings)):
        collection.add(
            ids=[f"doc_{i}"],
            embeddings=[embedding.tolist()],
            documents=[doc.page_content],
            metadatas=[doc.metadata]
        )

    return client, collection


def retrieve_similar_documents(collection, query_embedding, top_k=5):
    """Retrieve similar documents."""
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k
    )

    return results

