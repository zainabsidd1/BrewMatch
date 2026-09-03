"use client";

import Image from "next/image";
import { useEffect, useMemo, useState } from "react";

import {
  deleteCoffeeLog,
  fetchCalendarMonth,
  fetchCoffeeJourneyStats,
  type CalendarMonth,
  type CoffeeJourneyStats,
  type CoffeeLog,
} from "@/lib/api";

const WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

function monthLabel(year: number, month: number) {
  return new Date(year, month - 1, 1).toLocaleString("en-US", {
    month: "long",
    year: "numeric",
  });
}

function buildMonthGrid(year: number, month: number) {
  const first = new Date(year, month - 1, 1);
  const startOffset = (first.getDay() + 6) % 7;
  const daysInMonth = new Date(year, month, 0).getDate();
  const cells: Array<number | null> = [];

  for (let i = 0; i < startOffset; i += 1) {
    cells.push(null);
  }
  for (let day = 1; day <= daysInMonth; day += 1) {
    cells.push(day);
  }
  while (cells.length % 7 !== 0) {
    cells.push(null);
  }

  return cells;
}

function toDateKey(year: number, month: number, day: number) {
  return `${year}-${String(month).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
}

export default function CoffeeJournalCard() {
  const now = new Date();
  const [stats, setStats] = useState<CoffeeJourneyStats | null>(null);
  const [statsError, setStatsError] = useState<string | null>(null);
  const [statsVersion, setStatsVersion] = useState(0);

  const [year, setYear] = useState(now.getFullYear());
  const [month, setMonth] = useState(now.getMonth() + 1);
  const [calendar, setCalendar] = useState<CalendarMonth | null>(null);
  const [selectedDay, setSelectedDay] = useState<string | null>(null);
  const [calendarError, setCalendarError] = useState<string | null>(null);
  const [calendarLoading, setCalendarLoading] = useState(true);
  const [calendarVersion, setCalendarVersion] = useState(0);
  const [removingId, setRemovingId] = useState<number | null>(null);

  useEffect(() => {
    let cancelled = false;

    fetchCoffeeJourneyStats()
      .then((data) => {
        if (!cancelled) {
          setStats(data);
        }
      })
      .catch((err) => {
        if (!cancelled) {
          setStatsError(
            err instanceof Error ? err.message : "Could not load journey stats.",
          );
        }
      });

    return () => {
      cancelled = true;
    };
  }, [statsVersion]);

  useEffect(() => {
    let cancelled = false;
    setCalendarLoading(true);
    setCalendarError(null);

    fetchCalendarMonth(year, month)
      .then((data) => {
        if (!cancelled) {
          setCalendar(data);
        }
      })
      .catch((err) => {
        if (!cancelled) {
          setCalendarError(
            err instanceof Error ? err.message : "Could not load calendar.",
          );
        }
      })
      .finally(() => {
        if (!cancelled) {
          setCalendarLoading(false);
        }
      });

    return () => {
      cancelled = true;
    };
  }, [year, month, calendarVersion]);

  const entriesByDate = useMemo(() => {
    const map = new Map<string, CoffeeLog[]>();
    for (const day of calendar?.days ?? []) {
      map.set(day.date, day.entries);
    }
    return map;
  }, [calendar]);

  useEffect(() => {
    if (!selectedDay) return;
    if (!entriesByDate.has(selectedDay)) {
      setSelectedDay(null);
    }
  }, [entriesByDate, selectedDay]);

  async function handleRemove(logId: number) {
    setRemovingId(logId);
    try {
      await deleteCoffeeLog(logId);
      setCalendarVersion((value) => value + 1);
      setStatsVersion((value) => value + 1);
    } catch (err) {
      setCalendarError(
        err instanceof Error ? err.message : "Could not remove this entry.",
      );
    } finally {
      setRemovingId(null);
    }
  }

  const grid = useMemo(() => buildMonthGrid(year, month), [year, month]);
  const selectedEntries = selectedDay
    ? (entriesByDate.get(selectedDay) ?? [])
    : [];
  const todayKey = toDateKey(
    now.getFullYear(),
    now.getMonth() + 1,
    now.getDate(),
  );

  function shiftMonth(delta: number) {
    const next = new Date(year, month - 1 + delta, 1);
    setYear(next.getFullYear());
    setMonth(next.getMonth() + 1);
  }

  return (
    <article className="w-full rounded-2xl bg-white/95 p-5 shadow-[0_8px_32px_rgba(59,35,20,0.1)] backdrop-blur-sm sm:p-6">
      <section>
        <h2 className="mb-3 text-lg font-bold text-[#3B2314]">
          Your Coffee Journey
        </h2>

        {statsError ? (
          <p className="text-sm text-red-700">{statsError}</p>
        ) : !stats ? (
          <p className="text-sm text-stone-500">Loading your streak...</p>
        ) : (
          <>
            <p className="flex items-center gap-2 text-xl font-bold text-[#3B2314]">
              {stats.streak_days > 0 ? (
                <Image
                  src="/streak-flame.png"
                  alt=""
                  width={22}
                  height={28}
                  className="h-6 w-auto"
                  aria-hidden
                />
              ) : null}
              {stats.streak_days} day streak
            </p>
            <p className="mt-1 text-sm leading-relaxed text-stone-600">
              {stats.streak_days > 0
                ? `You've explored coffee for ${stats.streak_days} day${stats.streak_days === 1 ? "" : "s"} in a row.`
                : "Log a recommendation to start your discovery streak."}
            </p>

            <dl className="mt-4 grid gap-2 text-sm">
              <div className="flex items-baseline justify-between gap-3">
                <dt className="text-stone-600">Coffees tried</dt>
                <dd className="font-semibold text-[#3B2314]">
                  {stats.coffees_tried}
                </dd>
              </div>
              <div className="flex items-baseline justify-between gap-3">
                <dt className="text-stone-600">Your favorite drink</dt>
                <dd className="text-right font-semibold text-[#3B2314]">
                  {stats.favorite_drink
                    ? `${stats.favorite_drink}${
                        stats.favorite_drink_avg_rating
                          ? ` (${stats.favorite_drink_avg_rating}/5)`
                          : ""
                      }`
                    : "—"}
                </dd>
              </div>
            </dl>
          </>
        )}
      </section>

      <div className="my-5 border-t border-[#E8C9A8]/80" />

      <section>
        <div className="mb-3 flex items-center justify-between gap-2">
          <h3 className="text-base font-bold text-[#3B2314]">Coffee Calendar</h3>
          <div className="flex items-center gap-1">
            <button
              type="button"
              onClick={() => shiftMonth(-1)}
              className="rounded-full px-2 py-0.5 text-sm font-semibold text-[#3B2314] hover:bg-[#F3E7DA]"
              aria-label="Previous month"
            >
              ←
            </button>
            <span className="min-w-[7.5rem] text-center text-xs font-semibold text-[#8B5E3C]">
              {monthLabel(year, month)}
            </span>
            <button
              type="button"
              onClick={() => shiftMonth(1)}
              className="rounded-full px-2 py-0.5 text-sm font-semibold text-[#3B2314] hover:bg-[#F3E7DA]"
              aria-label="Next month"
            >
              →
            </button>
          </div>
        </div>

        {calendarLoading ? (
          <p className="py-4 text-center text-sm text-stone-500">
            Loading calendar...
          </p>
        ) : calendarError ? (
          <p className="py-4 text-center text-sm text-red-700">{calendarError}</p>
        ) : (
          <>
            <div className="grid grid-cols-7 gap-0.5 text-center text-[10px] font-semibold uppercase tracking-wide text-stone-500">
              {WEEKDAYS.map((day) => (
                <div key={day} className="py-0.5">
                  {day}
                </div>
              ))}
            </div>

            <div className="mt-0.5 grid grid-cols-7 gap-0.5">
              {grid.map((day, index) => {
                if (!day) {
                  return (
                    <div key={`empty-${index}`} className="h-8 sm:h-9" />
                  );
                }

                const key = toDateKey(year, month, day);
                const hasCoffee = entriesByDate.has(key);
                const isSelected = selectedDay === key;
                const isToday = key === todayKey;

                return (
                  <button
                    key={key}
                    type="button"
                    onClick={() => setSelectedDay(hasCoffee ? key : null)}
                    className={`relative flex h-8 flex-col items-center justify-center rounded-lg text-[11px] transition sm:h-9 ${
                      isSelected
                        ? "bg-[#8B5E3C] text-white"
                        : hasCoffee
                          ? "bg-[#F3E7DA] text-[#3B2314] hover:bg-[#E8C9A8]"
                          : "text-stone-500 hover:bg-[#FBF6F0]"
                    } ${
                      isToday && !isSelected
                        ? "ring-1 ring-[#5B8C5A]"
                        : isToday && isSelected
                          ? "ring-1 ring-[#A8D5A2]"
                          : ""
                    }`}
                    aria-current={isToday ? "date" : undefined}
                  >
                    <span className="font-semibold leading-none">{day}</span>
                    {hasCoffee ? (
                      <Image
                        src="/coffee-cup-icon.png"
                        alt=""
                        width={10}
                        height={10}
                        className="mt-0.5 size-2.5"
                        aria-hidden
                      />
                    ) : null}
                    {isToday ? (
                      <span
                        className={`absolute right-1 top-1 size-1.5 rounded-full ${
                          isSelected ? "bg-[#A8D5A2]" : "bg-[#5B8C5A]"
                        }`}
                        aria-hidden
                      />
                    ) : null}
                  </button>
                );
              })}
            </div>

            {selectedDay && selectedEntries.length > 0 ? (
              <div className="mt-3 rounded-xl border border-[#E8C9A8] bg-[#FBF6F0]/80 px-3 py-2.5">
                <p className="text-[11px] font-semibold uppercase tracking-wide text-[#8B5E3C]">
                  {selectedDay}
                </p>
                <ul className="mt-1.5 space-y-1.5">
                  {selectedEntries.map((entry) => (
                    <li
                      key={entry.id}
                      className="flex items-start justify-between gap-3 text-sm text-[#3B2314]"
                    >
                      <div className="min-w-0">
                        <p className="font-semibold">{entry.drink_name}</p>
                        <p className="text-xs text-stone-600">
                          {entry.rating
                            ? `${entry.rating}/5 rating`
                            : "Not rated yet"}
                          {entry.source === "brewmatch_recommendation"
                            ? " · BrewMatch recommendation"
                            : null}
                        </p>
                      </div>
                      <button
                        type="button"
                        onClick={() => handleRemove(entry.id)}
                        disabled={removingId === entry.id}
                        className="shrink-0 px-1 text-base leading-none text-stone-400 transition hover:text-stone-600 disabled:opacity-40"
                        aria-label={`Remove ${entry.drink_name}`}
                      >
                        ×
                      </button>
                    </li>
                  ))}
                </ul>
              </div>
            ) : (
              <p className="mt-3 text-center text-[11px] text-stone-500">
                Tap a day with a cup to see what you logged.
              </p>
            )}
          </>
        )}
      </section>
    </article>
  );
}
