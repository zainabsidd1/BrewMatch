import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, it, vi } from "vitest";

import QuizForm from "@/components/quiz/QuizForm";
import {
  COFFEE_PREFERENCE_QUESTIONS,
  QUIZ_QUESTIONS,
} from "@/lib/quizQuestions";

vi.mock("@/lib/quizQuestions", async (importOriginal) => {
  const actual = await importOriginal<typeof import("@/lib/quizQuestions")>();
  return {
    ...actual,
    pickQuizSession: () => [
      actual.QUIZ_QUESTIONS[0],
      actual.COFFEE_PREFERENCE_QUESTIONS[0],
    ],
  };
});

vi.mock("@/lib/api", () => ({
  matchQuizAnswers: vi.fn(),
}));

describe("QuizForm", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders the quiz", () => {
    render(<QuizForm />);

    expect(screen.getByText(/Question 1 of 2/i)).toBeInTheDocument();
    expect(screen.getByText(QUIZ_QUESTIONS[0].prompt)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /Next Question/i })).toBeDisabled();
  });

  it("advances progress after answering a question", async () => {
    const user = userEvent.setup();
    render(<QuizForm />);

    await user.click(
      screen.getByRole("button", {
        name: new RegExp(QUIZ_QUESTIONS[0].options[0].label, "i"),
      }),
    );
    await user.click(screen.getByRole("button", { name: /Next Question/i }));

    expect(screen.getByText(/Question 2 of 2/i)).toBeInTheDocument();
    expect(
      screen.getByText(COFFEE_PREFERENCE_QUESTIONS[0].prompt),
    ).toBeInTheDocument();
  });
});
