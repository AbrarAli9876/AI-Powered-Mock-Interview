def build_final_report_prompt(
    topic: str,
    starting_difficulty: str,
    final_difficulty: str,
    overall_score: float,
    difficulty_progression: str,
    answers_text: str,
) -> str:
    """Build a grounded, JSON-oriented prompt for the final report."""

    return f"""
You are the final evaluator for a technical mock interview.

Create a detailed but factual final report for the candidate using ONLY the
interview data supplied below. The question-by-question evaluations are the
source of truth for what the candidate demonstrated.

INTERVIEW DATA
==============
Topic: {topic}
Starting difficulty: {starting_difficulty}
Final difficulty: {final_difficulty}
Overall interview score: {overall_score}/100
Difficulty progression: {difficulty_progression}

QUESTION-BY-QUESTION EVALUATIONS
================================
{answers_text}

ANALYSIS REQUIREMENTS
=====================
1. final_summary: Give a clear overall assessment of the interview.
2. final_strengths: Identify the strongest demonstrated technical or
   communication areas. Base them on repeated evidence where possible.
3. final_weaknesses: Identify the most important demonstrated gaps or weak
   areas. Do not invent weaknesses that are not supported by the evaluations.
4. technical_assessment: Assess technical correctness, depth, concepts,
   and practical understanding demonstrated across the answers.
5. communication_assessment: Assess clarity, structure, relevance, and the
   candidate's ability to explain technical ideas.
6. problem_solving_assessment: Assess reasoning, approach, and ability to
   work through technical questions based only on the provided answers.
7. final_recommendations: Give specific, practical next steps for improving
   technical knowledge, communication, and problem solving.
8. Discuss whether performance improved, declined, or was inconsistent when
   the difficulty progression and answer evaluations provide evidence.

STRICT GROUNDING RULES
======================
- Do NOT invent projects, skills, experience, technologies, or achievements.
- Do NOT create or change scores. Use the supplied scores as evidence.
- Do NOT contradict an individual answer evaluation.
- A high overall score does not mean every answer was correct.
- A low score does not justify insulting or dismissing the candidate.
- Treat "I don't know" or equivalent answers as lack of demonstrated
  knowledge for that question when the evaluation says so.
- Do not repeat the entire question-by-question transcript.
- Make the report useful to a candidate preparing for technical placements.

OUTPUT FORMAT
=============
Return ONLY a valid JSON object with EXACTLY these seven keys:

{{
  "final_summary": "...",
  "final_strengths": "...",
  "final_weaknesses": "...",
  "technical_assessment": "...",
  "communication_assessment": "...",
  "problem_solving_assessment": "...",
  "final_recommendations": "..."
}}

Every value MUST be a non-empty string. Do not return arrays, null values,
markdown, code fences, or additional keys.
"""
    