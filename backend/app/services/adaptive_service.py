from app.enums.question_difficulty import QuestionDifficulty


class AdaptiveDifficultyService:
    """
    Handles dynamic difficulty adjustment during
    the current interview session.
    """

    POOR_THRESHOLD = 60
    STRONG_THRESHOLD = 80
    STREAK_LIMIT = 3

    def update_performance(
        self,
        current_difficulty: QuestionDifficulty,
        poor_streak: int,
        strong_streak: int,
        score: float,
    ) -> tuple[
        QuestionDifficulty,
        int,
        int,
    ]:
        """
        Updates performance streaks and determines
        the difficulty for the next question.
        """

        # Poor answer
        if score < self.POOR_THRESHOLD:
            poor_streak += 1
            strong_streak = 0

        # Strong answer
        elif score >= self.STRONG_THRESHOLD:
            strong_streak += 1
            poor_streak = 0

        # Acceptable answer
        else:
            poor_streak = 0
            strong_streak = 0

        # Three consecutive poor answers
        if poor_streak >= self.STREAK_LIMIT:
            current_difficulty = self._decrease_difficulty(
                current_difficulty
            )

            poor_streak = 0
            strong_streak = 0

        # Three consecutive strong answers
        elif strong_streak >= self.STREAK_LIMIT:
            current_difficulty = self._increase_difficulty(
                current_difficulty
            )

            poor_streak = 0
            strong_streak = 0

        return (
            current_difficulty,
            poor_streak,
            strong_streak,
        )

    def _increase_difficulty(
        self,
        difficulty: QuestionDifficulty,
    ) -> QuestionDifficulty:

        if difficulty == QuestionDifficulty.EASY:
            return QuestionDifficulty.MEDIUM

        if difficulty == QuestionDifficulty.MEDIUM:
            return QuestionDifficulty.HARD

        return QuestionDifficulty.HARD

    def _decrease_difficulty(
        self,
        difficulty: QuestionDifficulty,
    ) -> QuestionDifficulty:

        if difficulty == QuestionDifficulty.HARD:
            return QuestionDifficulty.MEDIUM

        if difficulty == QuestionDifficulty.MEDIUM:
            return QuestionDifficulty.EASY

        return QuestionDifficulty.EASY