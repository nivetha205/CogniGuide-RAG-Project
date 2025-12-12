from pypdf import PdfReader
from langchain_core.documents import Document

def load_pdf(pdf_path):
    """Load PDF and extract text."""
    pdf_reader = PdfReader(pdf_path)
    documents = []

    for page_num, page in enumerate(pdf_reader.pages):
        text = page.extract_text()

        doc = Document(
            page_content=text,
            metadata={"page": page_num + 1, "source": pdf_path}
        )

        documents.append(doc)

    return documents


