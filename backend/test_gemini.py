from app.ai.gemini_client import GeminiEvaluationClient


client = GeminiEvaluationClient()

result = client.evaluate_answer(
    question="What is the difference between a list and a tuple in Python?",
    expected_answer=(
        "A list is mutable while a tuple is immutable. "
        "Lists use square brackets and tuples use parentheses."
    ),
    candidate_answer=(
        "A list can be changed after creation, while a tuple cannot "
        "normally be changed after creation."
    ),
)

print("\n=== Gemini Evaluation ===")
print(f"Overall Score: {result.overall_score}")
print(f"Technical Score: {result.technical_score}")
print(f"Communication Score: {result.communication_score}")
print(f"Relevance Score: {result.relevance_score}")
print(f"\nFeedback:\n{result.feedback}")
print(f"\nStrengths:\n{result.strengths}")
print(f"\nImprovements:\n{result.improvements}")