import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, it, vi } from "vitest";

import PersonalizedRecsCard from "@/components/dashboard/PersonalizedRecsCard";
import type { PersonalizedDrink, PersonalizedRecommendations } from "@/lib/api";

const fetchPersonalizedRecommendations = vi.fn();
const addCoffeeToCalendar = vi.fn();

vi.mock("@/lib/api", () => ({
  fetchPersonalizedRecommendations: (...args: unknown[]) =>
    fetchPersonalizedRecommendations(...args),
  addCoffeeToCalendar: (...args: unknown[]) => addCoffeeToCalendar(...args),
}));

const americano: PersonalizedDrink = {
  drink_id: "americano",
  base_drink: "Americano",
  display_name: "Americano",
  temperature: "hot",
  sweetness: "low",
  syrup: null,
  modifier: null,
  explanation: "A familiar classic from your journal.",
};

const coldBrew: PersonalizedDrink = {
  drink_id: "cold-brew",
  base_drink: "Cold Brew",
  display_name: "Cold Brew",
  temperature: "iced",
  sweetness: "low",
  syrup: null,
  modifier: null,
  explanation: "Something new to try.",
};

const fullPayload: PersonalizedRecommendations = {
  taste_profile: {
    preferred_temperature: "iced",
    sweetness: "low",
    preferred_flavors: ["vanilla"],
    strength: "bold",
    milk_preference: "espresso-forward",
    confidence: "full",
    rated_count: 4,
    temperature_mix: { iced: 72, hot: 28 },
    sweetness_mix: { low: 64, medium: 29, high: 7 },
  },
  what_you_might_like: americano,
  try_something_new: coldBrew,
  message: null,
};

describe("PersonalizedRecsCard", () => {
  beforeEach(() => {
    fetchPersonalizedRecommendations.mockReset();
    addCoffeeToCalendar.mockReset();
  });

  it("renders What You Might Like and Try Something New from API data", async () => {
    fetchPersonalizedRecommendations.mockResolvedValue(fullPayload);

    render(<PersonalizedRecsCard />);

    expect(
      await screen.findByText(/What You Might Like/i),
    ).toBeInTheDocument();
    expect(screen.getByText(/Americano/i)).toBeInTheDocument();
    expect(screen.getByText(/Try Something New/i)).toBeInTheDocument();
    expect(screen.getByText(/Cold Brew/i)).toBeInTheDocument();
  });

  it("shows a loading state", () => {
    fetchPersonalizedRecommendations.mockReturnValue(new Promise(() => {}));

    render(<PersonalizedRecsCard />);

    expect(screen.getByText(/Learning your taste/i)).toBeInTheDocument();
  });

  it("hides What You Might Like for empty journal history", async () => {
    fetchPersonalizedRecommendations.mockResolvedValue({
      ...fullPayload,
      what_you_might_like: null,
      taste_profile: { ...fullPayload.taste_profile, rated_count: 0 },
    });

    render(<PersonalizedRecsCard />);

    expect(await screen.findByText(/Try Something New/i)).toBeInTheDocument();
    expect(screen.queryByText(/What You Might Like/i)).not.toBeInTheDocument();
  });

  it("shows an error without crashing when the API fails", async () => {
    fetchPersonalizedRecommendations.mockRejectedValue(
      new Error("Could not load recommendations."),
    );

    render(<PersonalizedRecsCard />);

    expect(
      await screen.findByText(/Could not load recommendations/i),
    ).toBeInTheDocument();
  });

  it("updates the UI after adding a rec to the journal", async () => {
    fetchPersonalizedRecommendations.mockResolvedValue(fullPayload);
    addCoffeeToCalendar.mockResolvedValue({ id: 1 });
    const user = userEvent.setup();

    render(<PersonalizedRecsCard />);

    const addButtons = await screen.findAllByRole("button", {
      name: /Add to journal/i,
    });
    await user.click(addButtons[0]);
    await user.click(screen.getByRole("button", { name: /Rate 5 out of 5/i }));

    await waitFor(() => {
      expect(addCoffeeToCalendar).toHaveBeenCalledWith({
        drink_id: "americano",
        drink_name: "Americano",
        rating: 5,
      });
    });
    expect(
      screen.getByText(/Added to your Coffee Calendar · Rated 5\/5/i),
    ).toBeInTheDocument();
  });
});
