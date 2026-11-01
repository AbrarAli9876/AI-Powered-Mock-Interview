from collections.abc import Sequence

from app.enums.question_difficulty import QuestionDifficulty


class AdaptiveDifficultyService:
    """Select the next interview difficulty from three consecutive scores."""

    EASY_MIN = 0
    EASY_MAX = 59
    MEDIUM_MIN = 60
    MEDIUM_MAX = 84
    HARD_MIN = 85
    HARD_MAX = 100
    STREAK_LIMIT = 3

    @classmethod
    def score_to_difficulty(cls, score: float) -> QuestionDifficulty:
        """Map one overall score to its corresponding difficulty band."""
        if not cls.EASY_MIN <= score <= cls.HARD_MAX:
            raise ValueError(f"Score must be between 0 and 100; received {score}.")

        if score <= cls.EASY_MAX:
            return QuestionDifficulty.EASY
        if score <= cls.MEDIUM_MAX:
            return QuestionDifficulty.MEDIUM
        return QuestionDifficulty.HARD

    def update_performance(
        self,
        current_difficulty: QuestionDifficulty,
        recent_scores: Sequence[float],
    ) -> QuestionDifficulty:
        """
        Change difficulty only when the latest three consecutive answers
        all fall into the same score band.

        Mixed score bands do not change the current difficulty. The latest
        three answers are evaluated as a rolling window, so a new sequence
        can begin immediately after a score-band change.
        """
        if len(recent_scores) < self.STREAK_LIMIT:
            return current_difficulty

        last_three = recent_scores[:self.STREAK_LIMIT]
        target_difficulties = [
            self.score_to_difficulty(float(score))
            for score in last_three
        ]

        if target_difficulties[0] == target_difficulties[1] == target_difficulties[2]:
            return target_difficulties[0]

        return current_difficulty
