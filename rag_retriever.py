from document_loader import load_pdf
from text_splitter import split_documents
from embeddings import get_embeddings_model, embed_documents
from vector_store import create_vector_store, retrieve_similar_documents


class RAGRetriever:
    def __init__(self, pdf_path):
        """Initialize RAG retriever."""
        self.model = get_embeddings_model()

        docs = load_pdf(pdf_path)
        split_docs = split_documents(docs)
        embeddings = embed_documents(split_docs, self.model)

        self.client, self.collection = create_vector_store(split_docs, embeddings)

    def retrieve(self, query, top_k=5):
        """Retrieve relevant documents."""
        query_embedding = self.model.encode(query)
        results = retrieve_similar_documents(self.collection, query_embedding, top_k)
        return results['documents'][0]


