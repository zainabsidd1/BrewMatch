"use client";

import Link from "next/link";
import { useState } from "react";

import QuizProgress from "@/components/quiz/QuizProgress";
import QuizResult from "@/components/quiz/QuizResult";
import { brewButtonClassName } from "@/lib/buttonStyles";
import { matchQuizAnswers, type QuizMatchResult } from "@/lib/api";
import {
  pickQuizSession,
  type QuizOptionKey,
} from "@/lib/quizQuestions";

export default function QuizForm() {
  const [questions] = useState(() => pickQuizSession());
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<number, QuizOptionKey>>({});
  const [matchResult, setMatchResult] = useState<QuizMatchResult | null>(null);
  const [isMatching, setIsMatching] = useState(false);
  const [matchError, setMatchError] = useState<string | null>(null);

  const question = questions[currentIndex];
  const selected = answers[question.id];
  const isFirst = currentIndex === 0;
  const isLast = currentIndex === questions.length - 1;
  const canContinue = Boolean(selected);

  function selectOption(key: QuizOptionKey) {
    setAnswers((prev) => ({ ...prev, [question.id]: key }));
  }

  function goNext() {
    if (!canContinue || isLast) return;
    setCurrentIndex((index) => index + 1);
  }

  function goPrevious() {
    if (!isFirst) {
      setCurrentIndex((index) => index - 1);
    }
  }

  async function finishQuiz() {
    if (!canContinue || isMatching) return;

    setIsMatching(true);
    setMatchError(null);

    const payload = questions.map((item) => {
      const optionKey = answers[item.id];
      const option = item.options.find((entry) => entry.key === optionKey);

      return {
        question_id: item.id,
        question: item.prompt,
        option_key: optionKey,
        option_label: option?.label ?? "",
      };
    });

    try {
      const result = await matchQuizAnswers(payload);
      setMatchResult(result);
    } catch (error) {
      setMatchError(
        error instanceof Error
          ? error.message
          : "Could not find your coffee match. Please try again.",
      );
    } finally {
      setIsMatching(false);
    }
  }

  if (isMatching) {
    return (
      <div className="flex w-full max-w-[46rem] flex-col gap-3.5">
        <div className="flex min-h-[32rem] flex-col items-center justify-center rounded-2xl bg-white px-8 py-14 text-center shadow-[0_8px_32px_rgba(59,35,20,0.12)]">
          <div
            className="size-10 animate-spin rounded-full border-4 border-[#E8C9A8] border-t-[#8B5E3C]"
            aria-hidden
          />
          <h1 className="mt-6 text-2xl font-bold tracking-tight text-[#3B2314]">
            Finding your brew match
          </h1>
        </div>

        <Link
          href="/dashboard"
          className="self-start text-sm font-semibold text-black underline underline-offset-2 transition-opacity hover:opacity-70"
        >
          ← Back to Dashboard
        </Link>
      </div>
    );
  }

  if (matchResult) {
    return (
      <div className="flex w-full max-w-[46rem] flex-col gap-3.5">
        <QuizResult
          drinkId={matchResult.drink_id}
          drinkName={matchResult.drink_name}
          description={matchResult.description}
          categories={matchResult.categories}
          personalizedMatch={matchResult.personalized_match}
        />

        <Link
          href="/dashboard"
          className="self-start text-sm font-semibold text-black underline underline-offset-2 transition-opacity hover:opacity-70"
        >
          ← Back to Dashboard
        </Link>
      </div>
    );
  }

  return (
    <div className="flex w-full max-w-[46rem] flex-col gap-3.5">
      <div className="flex flex-col rounded-2xl bg-white shadow-[0_8px_32px_rgba(59,35,20,0.12)]">
        <QuizProgress
          currentIndex={currentIndex}
          totalSteps={questions.length}
        />

        <div className="flex flex-col px-6 py-6 sm:px-9 sm:py-7">
          <div className="mx-auto w-full max-w-xl">
            <p className="text-center text-sm font-medium uppercase tracking-wide text-[#8B5E3C]">
              Question {currentIndex + 1}
            </p>
            <h1 className="mt-2 text-center text-xl font-bold tracking-tight text-[#3B2314] sm:text-[1.35rem]">
              {question.prompt}
            </h1>

            <fieldset className="mt-5 space-y-2.5">
              <legend className="sr-only">Answer choices</legend>
              {question.options.map((option) => {
                const isSelected = selected === option.key;

                return (
                  <button
                    key={option.key}
                    type="button"
                    onClick={() => selectOption(option.key)}
                    className={`flex w-full items-center gap-3 rounded-xl border px-3.5 py-2.5 text-left transition ${
                      isSelected
                        ? "border-[#8B5E3C] bg-[#F3E7DA] shadow-sm"
                        : "border-[#E8C9A8] bg-white hover:border-[#8B5E3C]/50 hover:bg-[#FBF6F0]"
                    }`}
                  >
                    <span
                      className={`flex size-7 shrink-0 items-center justify-center rounded-full text-sm font-bold ${
                        isSelected
                          ? "bg-[#8B5E3C] text-white"
                          : "bg-[#F3E7DA] text-[#3B2314]"
                      }`}
                    >
                      {option.key}
                    </span>
                    <span className="text-sm leading-snug text-[#3B2314] sm:text-[0.95rem]">
                      {option.label}
                    </span>
                  </button>
                );
              })}
            </fieldset>
          </div>

          {matchError ? (
            <p className="mx-auto mt-3.5 max-w-xl text-center text-sm text-red-700">
              {matchError}
            </p>
          ) : null}

          <div className="mt-6 flex items-center justify-between gap-4 border-t border-[#E8C9A8]/60 pt-5">
            {!isFirst ? (
              <button
                type="button"
                onClick={goPrevious}
                disabled={isMatching}
                className="text-sm font-semibold text-stone-600 transition-colors hover:text-[#3B2314] disabled:opacity-45"
              >
                ← Previous
              </button>
            ) : (
              <span />
            )}

            {!isLast ? (
              <button
                type="button"
                onClick={goNext}
                disabled={!canContinue}
                className={`${brewButtonClassName} px-6 py-2.5 text-sm disabled:cursor-not-allowed disabled:opacity-45 disabled:hover:bg-[#E8C9A8] disabled:hover:text-[#3B2314]`}
              >
                Next Question →
              </button>
            ) : (
              <button
                type="button"
                onClick={finishQuiz}
                disabled={!canContinue || isMatching}
                className={`${brewButtonClassName} px-6 py-2.5 text-sm disabled:cursor-not-allowed disabled:opacity-45 disabled:hover:bg-[#E8C9A8] disabled:hover:text-[#3B2314]`}
              >
                Finish
              </button>
            )}
          </div>
        </div>
      </div>

      <Link
        href="/dashboard"
        className="self-start text-sm font-semibold text-black underline underline-offset-2 transition-opacity hover:opacity-70"
      >
        ← Back to Dashboard
      </Link>
    </div>
  );
}
