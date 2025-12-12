from rag_retriever import RAGRetriever
from llm_generator import LLMGenerator
from prompt_builder import PromptBuilder


class CogniGuideCore:
    def __init__(self, pdf_path):
        """Initialize CogniGuide."""
        self.retriever = RAGRetriever(pdf_path)
        self.generator = LLMGenerator()

    def generate_study_guide(self, user_query, user_profile, output_format='flashcards'):
        """Generate personalized study guide."""
        retrieved_context = self.retriever.retrieve(user_query, top_k=5)

        prompt = PromptBuilder.build_study_guide_prompt(
            retrieved_context,
            user_profile,
            output_format
        )

        study_guide = self.generator.generate(prompt)
        return study_guide
