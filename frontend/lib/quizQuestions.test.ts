import { describe, expect, it } from "vitest";

import {
  COFFEE_PREFERENCE_COUNT,
  COFFEE_PREFERENCE_QUESTIONS,
  QUIZ_SESSION_LENGTH,
  pickQuizSession,
} from "@/lib/quizQuestions";

describe("pickQuizSession", () => {
  it("builds a quiz with 15 questions", () => {
    const session = pickQuizSession();

    expect(session).toHaveLength(QUIZ_SESSION_LENGTH);
    expect(session).toHaveLength(15);
  });

  it("always includes the required coffee-preference questions", () => {
    const coffeeIds = new Set(
      COFFEE_PREFERENCE_QUESTIONS.map((question) => question.id),
    );

    for (let i = 0; i < 8; i += 1) {
      const session = pickQuizSession();
      const included = session.filter((question) => coffeeIds.has(question.id));
      expect(included).toHaveLength(COFFEE_PREFERENCE_COUNT);
    }
  });
});
