def build_final_report_prompt(
    topic: str,
    starting_difficulty: str,
    final_difficulty: str,
    overall_score: float,
    difficulty_progression: str,
    answers_text: str,
) -> str:
    """
    Build the prompt used to generate the final interview report.
    """

    return f"""
You are an expert technical interview evaluator.

Generate a detailed final interview report for a candidate.

The report must be based ONLY on the interview information
provided below.

Do not invent information that is not present in the interview.

INTERVIEW INFORMATION
---------------------

Topic:
{topic}

Starting difficulty:
{starting_difficulty}

Final difficulty:
{final_difficulty}

Overall interview score:
{overall_score}/100

Actual difficulty progression:
{difficulty_progression}

QUESTION-BY-QUESTION PERFORMANCE
--------------------------------

{answers_text}

YOUR TASK
---------

Analyze the candidate's complete interview performance.

The final report must:

1. Summarize the candidate's overall performance.

2. Identify the candidate's strongest areas.

3. Identify the candidate's weakest areas.

4. Evaluate technical knowledge and understanding.

5. Evaluate communication quality.

6. Evaluate problem-solving ability based on the answers provided.

7. Provide practical recommendations for improvement.

8. Consider the difficulty progression when evaluating performance.

9. Explain whether the candidate demonstrated improvement,
   decline, or inconsistent performance during the interview.

10. Do not contradict the individual question evaluations.

IMPORTANT RULES
---------------

- Do not invent skills that were not demonstrated.
- Do not claim the candidate answered a question correctly
  if the individual evaluation indicates otherwise.
- Do not create scores yourself.
- Use the provided overall score.
- Keep the assessment professional and constructive.
- The report should be detailed but concise enough to be useful.
"""