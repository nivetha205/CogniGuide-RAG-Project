class PromptBuilder:
    @staticmethod
    def build_study_guide_prompt(retrieved_context, user_profile, output_format):
        """Build personalized prompt."""
        context_text = "\n\n".join(retrieved_context)

        learning_level = user_profile.get('learning_level', 'intermediate')
        learning_style = user_profile.get('learning_style', 'visual')
        tone = user_profile.get('tone', 'formal')

        system_instruction = (
            f"You are an expert educational assistant. Create a {output_format} "
            f"for a {learning_level}-level student who prefers {learning_style} learning. "
            f"Maintain a {tone} tone."
        )

        if output_format == 'flashcards':
            format_instruction = (
                "Generate 10 flashcards:\n"
                "Q: [Question]\n"
                "A: [Answer]"
            )
        elif output_format == 'summary':
            format_instruction = (
                "Write a 300-500 word summary with:\n"
                "- Clear explanations\n"
                "- Analogies for beginners\n"
                "- Practical examples"
            )
        elif output_format == 'quiz':
            format_instruction = (
                "Generate a quiz:\n"
                "- 3 multiple-choice questions\n"
                "- 2 short-answer questions"
            )

        full_prompt = (
            f"{system_instruction}\n\n"
            f"{format_instruction}\n\n"
            f"Source material:\n\n"
            f"{context_text}\n\n"
            f"Now create the {output_format}."
        )

        return full_prompt


