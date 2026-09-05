"use client";

import { useEffect, useMemo, useState } from "react";

import {
  addCoffeeToCalendar,
  fetchDrinkCatalog,
  type CatalogDrink,
} from "@/lib/api";
import { brewButtonClassName } from "@/lib/buttonStyles";

function titleCase(value: string) {
  return value.charAt(0).toUpperCase() + value.slice(1);
}

function loggedDrinkName(
  drink: CatalogDrink,
  temperature: "hot" | "iced",
  syrup: string,
) {
  const flavor = syrup ? `${titleCase(syrup)} ` : "";
  if (temperature === "iced" && !drink.name.toLowerCase().startsWith("iced")) {
    return `Iced ${flavor}${drink.name}`.replace(/\s+/g, " ").trim();
  }
  return `${flavor}${drink.name}`.trim();
}

export default function LogDrinkButton() {
  const [open, setOpen] = useState(false);
  const [drinks, setDrinks] = useState<CatalogDrink[]>([]);
  const [syrups, setSyrups] = useState<string[]>([]);
  const [catalogError, setCatalogError] = useState<string | null>(null);
  const [drinkId, setDrinkId] = useState("");
  const [syrup, setSyrup] = useState("");
  const [temperature, setTemperature] = useState<"hot" | "iced">("hot");
  const [rating, setRating] = useState<number | null>(null);
  const [saving, setSaving] = useState(false);
  const [saveError, setSaveError] = useState<string | null>(null);

  const selectedDrink = useMemo(
    () => drinks.find((drink) => drink.id === drinkId) ?? null,
    [drinks, drinkId],
  );
  const temperatures = selectedDrink?.temperatures ?? ["hot", "iced"];
  const syrupOptions = syrups;

  useEffect(() => {
    if (!open) return;

    function onKeyDown(event: KeyboardEvent) {
      if (event.key === "Escape") {
        setOpen(false);
      }
    }

    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [open]);

  useEffect(() => {
    if (!open) return;

    let cancelled = false;
    setCatalogError(null);
    setSaveError(null);
    setRating(null);
    setSyrup("");

    fetchDrinkCatalog()
      .then((catalog) => {
        if (cancelled) return;
        setDrinks(catalog.drinks);
        setSyrups(catalog.syrups);
        const first = catalog.drinks[0];
        if (first) {
          setDrinkId(first.id);
          setTemperature(first.temperatures[0] ?? "hot");
        }
      })
      .catch((err) => {
        if (!cancelled) {
          setCatalogError(
            err instanceof Error ? err.message : "Could not load drinks.",
          );
        }
      });

    return () => {
      cancelled = true;
    };
  }, [open]);

  useEffect(() => {
    if (!selectedDrink) return;
    if (!selectedDrink.temperatures.includes(temperature)) {
      setTemperature(selectedDrink.temperatures[0] ?? "hot");
    }
  }, [selectedDrink, temperature]);

  async function handleSave() {
    if (!selectedDrink || rating == null) return;
    setSaving(true);
    setSaveError(null);

    try {
      await addCoffeeToCalendar({
        drink_id: selectedDrink.id,
        drink_name: loggedDrinkName(selectedDrink, temperature, syrup),
        rating,
        temperature,
        source: "manual",
      });
      window.dispatchEvent(new Event("brewmatch:journal-updated"));
      setOpen(false);
    } catch (err) {
      setSaveError(
        err instanceof Error ? err.message : "Could not save this drink.",
      );
    } finally {
      setSaving(false);
    }
  }

  return (
    <>
      <button
        type="button"
        onClick={() => setOpen(true)}
        className={`${brewButtonClassName} w-full px-4 py-2.5 text-sm`}
      >
        Log a drink
      </button>

      {open ? (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-[#3B2314]/50 px-4"
          onClick={() => setOpen(false)}
          role="presentation"
        >
          <div
            role="dialog"
            aria-labelledby="log-drink-title"
            className="w-full max-w-sm rounded-2xl bg-[#FBF6F0] p-5 text-[#3B2314] shadow-[0_16px_40px_rgba(59,35,20,0.28)]"
            onClick={(event) => event.stopPropagation()}
          >
            <h3 id="log-drink-title" className="text-lg font-bold">
              Log a drink
            </h3>
            <p className="mt-1 text-sm text-stone-600">
              Pick a drink, syrup, and temperature, then rate it to add it to
              your journal.
            </p>

            {catalogError ? (
              <p className="mt-4 text-sm text-red-700">{catalogError}</p>
            ) : (
              <div className="mt-4 space-y-3">
                <label className="block text-sm font-semibold">
                  Drink
                  <select
                    value={drinkId}
                    onChange={(event) => setDrinkId(event.target.value)}
                    className="mt-1 w-full rounded-xl border border-[#E8C9A8] bg-white px-3 py-2 text-sm font-medium"
                  >
                    {drinks.map((drink) => (
                      <option key={drink.id} value={drink.id}>
                        {drink.name}
                      </option>
                    ))}
                  </select>
                </label>

                <label className="block text-sm font-semibold">
                  Syrup
                  <select
                    value={syrup}
                    onChange={(event) => setSyrup(event.target.value)}
                    className="mt-1 w-full rounded-xl border border-[#E8C9A8] bg-white px-3 py-2 text-sm font-medium"
                  >
                    <option value="">None</option>
                    {syrupOptions.map((item) => (
                      <option key={item} value={item}>
                        {titleCase(item)}
                      </option>
                    ))}
                  </select>
                </label>

                <fieldset>
                  <legend className="text-sm font-semibold">Temperature</legend>
                  <div className="mt-2 flex gap-2">
                    {temperatures.map((option) => (
                      <button
                        key={option}
                        type="button"
                        onClick={() => setTemperature(option)}
                        className={`flex-1 rounded-full px-3 py-2 text-sm font-bold ${
                          temperature === option
                            ? "bg-[#8B5E3C] text-white"
                            : "border border-[#E8C9A8] bg-white text-[#3B2314]"
                        }`}
                      >
                        {option === "iced" ? "Iced" : "Hot"}
                      </button>
                    ))}
                  </div>
                </fieldset>

                <fieldset>
                  <legend className="text-sm font-semibold">Rating</legend>
                  <div className="mt-2 flex gap-2">
                    {[1, 2, 3, 4, 5].map((value) => (
                      <button
                        key={value}
                        type="button"
                        onClick={() => setRating(value)}
                        className={`flex size-9 items-center justify-center rounded-full border text-sm font-bold ${
                          rating === value
                            ? "border-[#8B5E3C] bg-[#8B5E3C] text-white"
                            : "border-[#E8C9A8] bg-white text-[#3B2314]"
                        }`}
                        aria-label={`Rate ${value} out of 5`}
                      >
                        {value}
                      </button>
                    ))}
                  </div>
                </fieldset>
              </div>
            )}

            {saveError ? (
              <p className="mt-3 text-sm text-red-700">{saveError}</p>
            ) : null}

            <div className="mt-5 flex justify-end gap-2">
              <button
                type="button"
                onClick={() => setOpen(false)}
                className="px-4 py-2 text-sm font-semibold text-stone-600"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleSave}
                disabled={!selectedDrink || rating == null || saving}
                className={`${brewButtonClassName} px-4 py-2 text-sm disabled:opacity-45`}
              >
                {saving ? "Saving..." : "Add to journal"}
              </button>
            </div>
          </div>
        </div>
      ) : null}
    </>
  );
}
