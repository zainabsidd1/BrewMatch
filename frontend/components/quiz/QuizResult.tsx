"use client";

import Image from "next/image";
import { useState } from "react";

import { addCoffeeToCalendar } from "@/lib/api";
import { brewButtonClassName } from "@/lib/buttonStyles";

type QuizResultProps = {
  drinkId: string;
  drinkName: string;
  description: string;
  categories: string[];
  personalizedMatch: string;
};

export default function QuizResult({
  drinkId,
  drinkName,
  description,
  categories,
  personalizedMatch,
}: QuizResultProps) {
  const [phase, setPhase] = useState<"idle" | "rating" | "saved">("idle");
  const [selectedRating, setSelectedRating] = useState<number | null>(null);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function saveWithRating(rating: number) {
    setSelectedRating(rating);
    setIsSaving(true);
    setError(null);

    try {
      await addCoffeeToCalendar({
        drink_id: drinkId,
        drink_name: drinkName,
        rating,
      });
      setPhase("saved");
      window.dispatchEvent(new Event("brewmatch:journal-updated"));
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Could not save this drink. Please try again.",
      );
    } finally {
      setIsSaving(false);
    }
  }

  return (
    <div className="flex flex-col rounded-2xl bg-white px-6 py-7 shadow-[0_8px_32px_rgba(59,35,20,0.12)] sm:px-9 sm:py-8">
      <p className="text-center text-sm font-medium uppercase tracking-wide text-[#8B5E3C]">
        Your BrewMatch
      </p>
      <h1 className="mt-2 text-center text-[1.75rem] font-bold tracking-tight text-[#3B2314] sm:text-3xl">
        {drinkName}
      </h1>

      <div className="mt-3.5 flex flex-wrap justify-center gap-2">
        {categories.map((category) => (
          <span
            key={category}
            className="rounded-full bg-[#F3E7DA] px-3 py-1 text-xs font-semibold text-[#3B2314]"
          >
            {category}
          </span>
        ))}
      </div>

      <p className="mx-auto mt-5 max-w-xl text-center text-sm leading-relaxed text-stone-600 sm:text-[0.95rem]">
        {description}
      </p>

      <div className="mx-auto mt-6 max-w-xl rounded-xl border border-[#E8C9A8] bg-[#FBF6F0]/70 px-5 py-5">
        <h2 className="text-xs font-bold uppercase tracking-wide text-[#8B5E3C] sm:text-sm">
          Why this is the perfect match
        </h2>
        <p className="mt-2.5 text-sm leading-relaxed text-[#3B2314] sm:text-[0.95rem]">
          {personalizedMatch}
        </p>
      </div>

      <div className="mx-auto mt-6 w-full max-w-xl border-t border-[#E8C9A8]/70 pt-5 text-center">
        {phase === "idle" ? (
          <button
            type="button"
            onClick={() => setPhase("rating")}
            className={`${brewButtonClassName} inline-flex items-center gap-2 px-6 py-2.5 text-sm`}
          >
            <Image
              src="/coffee-cup-icon.png"
              alt=""
              width={18}
              height={18}
              className="size-[18px]"
              aria-hidden
            />
            Add to Coffee Calendar
          </button>
        ) : null}

        {phase === "rating" ? (
          <div>
            <p className="text-sm font-semibold text-[#3B2314]">
              Rate the recommendation
            </p>
            <p className="mt-1 text-xs text-stone-500">
              Tap 1–5 to save this drink to your coffee journal.
            </p>
            <div className="mt-4 flex justify-center gap-2">
              {[1, 2, 3, 4, 5].map((value) => (
                <button
                  key={value}
                  type="button"
                  disabled={isSaving}
                  onClick={() => saveWithRating(value)}
                  className={`flex size-10 items-center justify-center rounded-full border text-sm font-bold transition ${
                    selectedRating === value
                      ? "border-[#8B5E3C] bg-[#8B5E3C] text-white"
                      : "border-[#E8C9A8] bg-[#FBF6F0] text-[#3B2314] hover:border-[#8B5E3C]"
                  } disabled:opacity-50`}
                  aria-label={`Rate ${value} out of 5`}
                >
                  {value}
                </button>
              ))}
            </div>
            {isSaving ? (
              <p className="mt-3 text-sm text-stone-500">Saving to calendar...</p>
            ) : null}
          </div>
        ) : null}

        {phase === "saved" ? (
          <div>
            <p className="text-sm font-semibold text-[#3B2314]">
              Added to your Coffee Calendar
            </p>
            <p className="mt-1 text-sm text-stone-600">
              Rated {selectedRating}/5 · logged from BrewMatch recommendation
            </p>
          </div>
        ) : null}

        {error ? (
          <p className="mt-3 text-sm text-red-700">{error}</p>
        ) : null}
      </div>
    </div>
  );
}
