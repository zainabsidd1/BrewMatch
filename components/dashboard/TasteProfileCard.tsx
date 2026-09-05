"use client";

import { useEffect, useMemo, useState } from "react";

import { fetchTasteProfile, type TasteProfile } from "@/lib/api";
import LogDrinkButton from "@/components/dashboard/LogDrinkButton";

function titleCase(value: string) {
  return value.charAt(0).toUpperCase() + value.slice(1);
}

function milkTag(value: string | null) {
  if (value === "espresso-forward") return "Espresso-forward";
  if (value === "milk-forward") return "Milk-forward";
  if (value === "balanced") return "Balanced milk";
  return null;
}

function sweetnessTag(mix: TasteProfile["sweetness_mix"], fallback: string | null) {
  const winner = fallback ?? (
    mix.low >= mix.medium && mix.low >= mix.high
      ? "low"
      : mix.high >= mix.medium
        ? "high"
        : "medium"
  );
  if (winner === "low") return "Low sweetness";
  if (winner === "high") return "High sweetness";
  return "Medium sweetness";
}

function temperatureTag(mix: TasteProfile["temperature_mix"]) {
  if (mix.iced === 0 && mix.hot === 0) return null;
  if (mix.iced >= 55) return "Iced lover";
  if (mix.hot >= 55) return "Hot coffee person";
  return "Hot and iced";
}

function flavorTag(flavors: string[]) {
  const flavor = flavors[0];
  if (!flavor) return null;
  return `${titleCase(flavor)}-friendly`;
}

function profileTags(profile: TasteProfile) {
  const hasSweetness =
    profile.sweetness_mix.low +
      profile.sweetness_mix.medium +
      profile.sweetness_mix.high >
    0;
  if (
    profile.temperature_mix.iced + profile.temperature_mix.hot === 0 &&
    !hasSweetness
  ) {
    return [];
  }

  return [
    temperatureTag(profile.temperature_mix),
    hasSweetness
      ? sweetnessTag(profile.sweetness_mix, profile.sweetness)
      : null,
    milkTag(profile.milk_preference),
    flavorTag(profile.preferred_flavors),
  ].filter((tag): tag is string => Boolean(tag));
}

function MixRow({
  label,
  percent,
}: {
  label: string;
  percent: number;
}) {
  return (
    <div className="grid grid-cols-[5.5rem_1fr_2.4rem] items-center gap-3">
      <p className="text-sm text-[#F3E7DA]">{label}</p>
      <div className="h-1.5 overflow-hidden rounded-full bg-[#5C3A21]">
        <div
          className="h-full rounded-full bg-[#E8C9A8] transition-[width] duration-500"
          style={{ width: `${percent}%` }}
        />
      </div>
      <p className="text-right text-sm tabular-nums text-[#E8C9A8]">{percent}%</p>
    </div>
  );
}

export default function TasteProfileCard() {
  const [profile, setProfile] = useState<TasteProfile | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [version, setVersion] = useState(0);

  useEffect(() => {
    function handleJournalUpdated() {
      setVersion((value) => value + 1);
    }

    window.addEventListener("brewmatch:journal-updated", handleJournalUpdated);
    return () => {
      window.removeEventListener(
        "brewmatch:journal-updated",
        handleJournalUpdated,
      );
    };
  }, []);

  useEffect(() => {
    let cancelled = false;

    fetchTasteProfile()
      .then((data) => {
        if (!cancelled) {
          setProfile(data);
        }
      })
      .catch((err) => {
        if (!cancelled) {
          setError(
            err instanceof Error
              ? err.message
              : "Could not load your coffee profile.",
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
  }, [version]);

  const tags = useMemo(
    () => (profile ? profileTags(profile) : []),
    [profile],
  );
  const hasTempMix =
    (profile?.temperature_mix.iced ?? 0) + (profile?.temperature_mix.hot ?? 0) >
    0;
  const hasSweetMix =
    (profile?.sweetness_mix.low ?? 0) +
      (profile?.sweetness_mix.medium ?? 0) +
      (profile?.sweetness_mix.high ?? 0) >
    0;
  const hasData = hasTempMix || hasSweetMix;

  return (
    <article className="relative flex flex-col overflow-hidden rounded-[1.75rem] bg-[#3B2314] px-6 py-7 text-[#FBF6F0] shadow-[0_18px_40px_rgba(59,35,20,0.28)]">
      <div className="pointer-events-none absolute inset-0 rounded-[1.75rem] ring-1 ring-inset ring-[#E8C9A8]/30" />
      <div className="pointer-events-none absolute -right-10 -top-16 size-40 rounded-full bg-[#E8C9A8]/10" />
      <div className="pointer-events-none absolute -bottom-12 -left-8 size-32 rounded-full bg-[#8B5E3C]/40" />

      <div className="relative">
        <p className="text-[11px] font-semibold uppercase tracking-[0.22em] text-[#E8C9A8]">
          From your journal
        </p>

        {loading ? (
          <p className="mt-5 text-sm text-[#E8C9A8]/80">Reading your cups...</p>
        ) : error || !profile ? (
          <p className="mt-5 text-sm text-[#F3E7DA]">
            {error ?? "Could not load your coffee profile."}
          </p>
        ) : !hasData ? (
          <p className="mt-5 text-sm leading-relaxed text-[#F3E7DA]/90">
            Log a few drinks in your coffee journal and this space will fill in
            with your temperature and sweetness mix.
          </p>
        ) : (
          <>
            <p className="mt-4 text-sm leading-relaxed text-[#F3E7DA]">
              {tags.join(" · ")}
            </p>

            {hasTempMix ? (
              <div className="mt-7 space-y-3">
                <MixRow label="Iced" percent={profile.temperature_mix.iced} />
                <MixRow label="Hot" percent={profile.temperature_mix.hot} />
              </div>
            ) : null}

            <div
              className={`space-y-3 ${
                hasTempMix
                  ? "mt-6 border-t border-[#E8C9A8]/20 pt-6"
                  : "mt-7"
              }`}
            >
              <MixRow label="Low sweet" percent={profile.sweetness_mix.low} />
              <MixRow label="Medium" percent={profile.sweetness_mix.medium} />
              <MixRow label="High" percent={profile.sweetness_mix.high} />
            </div>
          </>
        )}
      </div>

      <div className="relative mt-6 border-t border-[#E8C9A8]/20 pt-6">
        <LogDrinkButton />
      </div>
    </article>
  );
}
