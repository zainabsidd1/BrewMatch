"use client";

import Image from "next/image";
import { useEffect, useState } from "react";

import {
  addCoffeeToCalendar,
  fetchPersonalizedRecommendations,
  type PersonalizedDrink,
  type PersonalizedRecommendations,
} from "@/lib/api";
import { brewButtonClassName } from "@/lib/buttonStyles";

export const JOURNAL_UPDATED_EVENT = "brewmatch:journal-updated";

function sweetnessLabel(value: string) {
  if (value === "low") return "Low sweet";
  if (value === "high") return "High sweet";
  return "Medium sweet";
}

function detailsLine(drink: PersonalizedDrink) {
  const parts = [
    sweetnessLabel(drink.sweetness),
    drink.temperature === "iced" ? "Iced" : "Hot",
  ];
  if (drink.syrup) {
    parts.push(drink.syrup.charAt(0).toUpperCase() + drink.syrup.slice(1));
  }
  if (drink.modifier) {
    parts.push(drink.modifier.charAt(0).toUpperCase() + drink.modifier.slice(1));
  }
  return parts.join(" · ");
}

function RecBlock({
  eyebrow,
  drink,
  showDetails = true,
}: {
  eyebrow: string;
  drink: PersonalizedDrink;
  showDetails?: boolean;
}) {
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
        drink_id: drink.drink_id,
        drink_name: drink.display_name,
        rating,
      });
      setPhase("saved");
      window.dispatchEvent(new Event(JOURNAL_UPDATED_EVENT));
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
    <div>
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <p className="text-xs font-semibold uppercase tracking-wide text-[#8B5E3C]">
            {eyebrow}
          </p>
          <h3 className="mt-1 text-lg font-bold text-[#3B2314]">
            {drink.display_name}
          </h3>
        </div>
        {phase === "idle" ? (
          <button
            type="button"
            onClick={() => setPhase("rating")}
            className={`${brewButtonClassName} inline-flex shrink-0 items-center gap-1.5 px-3 py-1.5 text-xs`}
          >
            <Image
              src="/coffee-cup-icon.png"
              alt=""
              width={14}
              height={14}
              className="size-3.5"
              aria-hidden
            />
            Add to journal
          </button>
        ) : null}
      </div>
      {showDetails ? (
        <p className="mt-1 text-xs font-medium text-stone-500">
          {detailsLine(drink)}
        </p>
      ) : null}
      <p className="mt-2 text-sm leading-relaxed text-stone-600">
        {drink.explanation}
      </p>

      {phase === "rating" ? (
        <div className="mt-3">
          <p className="text-sm font-semibold text-[#3B2314]">
            Rate the recommendation
          </p>
          <p className="mt-1 text-xs text-stone-500">
            Tap 1–5 to save this drink to your coffee journal.
          </p>
          <div className="mt-3 flex gap-2">
            {[1, 2, 3, 4, 5].map((value) => (
              <button
                key={value}
                type="button"
                disabled={isSaving}
                onClick={() => saveWithRating(value)}
                className={`flex size-9 items-center justify-center rounded-full border text-sm font-bold transition ${
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
            <p className="mt-2 text-sm text-stone-500">Saving to calendar...</p>
          ) : null}
        </div>
      ) : null}

      {phase === "saved" ? (
        <p className="mt-3 text-sm font-semibold text-[#3B2314]">
          Added to your Coffee Calendar · Rated {selectedRating}/5
        </p>
      ) : null}

      {error ? <p className="mt-2 text-sm text-red-700">{error}</p> : null}
    </div>
  );
}

export default function PersonalizedRecsCard() {
  const [data, setData] = useState<PersonalizedRecommendations | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;

    fetchPersonalizedRecommendations()
      .then((payload) => {
        if (!cancelled) {
          setData(payload);
        }
      })
      .catch((err) => {
        if (!cancelled) {
          setError(
            err instanceof Error
              ? err.message
              : "Could not load recommendations.",
          );
        }
      })
      .finally(() => {
        if (!cancelled) {
          setLoading(false);
        }
      });

    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <article className="rounded-2xl bg-white/95 p-5 shadow-[0_8px_32px_rgba(59,35,20,0.1)] backdrop-blur-sm sm:p-6">
      {loading ? (
        <p className="text-sm text-stone-500">Learning your taste...</p>
      ) : error || !data ? (
        <p className="text-sm text-red-700">
          {error ?? "Could not load recommendations."}
        </p>
      ) : (
        <div className="flex flex-col gap-5">
          {data.what_you_might_like ? (
            <RecBlock
              eyebrow="What You Might Like"
              drink={data.what_you_might_like}
            />
          ) : null}
          {data.what_you_might_like && data.try_something_new ? (
            <div className="border-t border-[#E8C9A8]/80" />
          ) : null}
          {data.try_something_new ? (
            <RecBlock
              eyebrow="Try Something New"
              drink={data.try_something_new}
              showDetails={false}
            />
          ) : null}
        </div>
      )}
    </article>
  );
}
