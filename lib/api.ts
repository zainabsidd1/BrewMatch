import { getToken } from "@/lib/auth";

const API_URL = (process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000").replace(
  /\/$/,
  "",
);

type ApiErrorBody = {
  detail?: string | { msg: string }[];
};

export type User = {
  id: number;
  email: string;
  name: string | null;
  created_at: string;
};

export type TokenResponse = {
  access_token: string;
  token_type: string;
};

async function parseApiError(response: Response) {
  const data: ApiErrorBody = await response.json().catch(() => ({}));

  if (typeof data.detail === "string") {
    return data.detail;
  }

  if (Array.isArray(data.detail) && data.detail[0]?.msg) {
    return data.detail[0].msg;
  }

  return `Request failed (${response.status}). Check that NEXT_PUBLIC_API_URL points at the FastAPI backend.`;
}

async function apiFetch(path: string, init?: RequestInit) {
  try {
    return await fetch(`${API_URL}${path}`, init);
  } catch {
    throw new Error(
      `Can't reach the API at ${API_URL}. Start the backend locally or set NEXT_PUBLIC_API_URL to your Render URL.`,
    );
  }
}

export async function registerUser(email: string, password: string, name: string) {
  const response = await apiFetch("/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password, name }),
  });

  if (!response.ok) {
    throw new Error(await parseApiError(response));
  }

  return response.json() as Promise<User>;
}

export async function loginUser(email: string, password: string) {
  const response = await apiFetch("/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    throw new Error(await parseApiError(response));
  }

  return response.json() as Promise<TokenResponse>;
}

export async function fetchCurrentUser(token = getToken()) {
  if (!token) {
    throw new Error("Not authenticated");
  }

  const response = await apiFetch("/auth/me", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error(await parseApiError(response));
  }

  return response.json() as Promise<User>;
}

export type QuizAnswerPayload = {
  question_id: number;
  question: string;
  option_key: string;
  option_label: string;
};

export type QuizMatchResult = {
  drink_id: string;
  drink_name: string;
  description: string;
  categories: string[];
  personalized_match: string;
};

export async function matchQuizAnswers(
  answers: QuizAnswerPayload[],
  token = getToken(),
) {
  if (!token) {
    throw new Error("Not authenticated");
  }

  const response = await apiFetch("/quiz/match", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ answers }),
  });

  if (!response.ok) {
    throw new Error(await parseApiError(response));
  }

  return response.json() as Promise<QuizMatchResult>;
}

export type CoffeeLog = {
  id: number;
  drink_id: string;
  drink_name: string;
  date_added: string;
  date_tried: string;
  rating: number | null;
  notes: string | null;
  is_favorite: boolean;
  source: string;
  temperature_tag?: "iced" | "hot" | null;
};

export type CalendarMonth = {
  year: number;
  month: number;
  days: {
    date: string;
    entries: CoffeeLog[];
  }[];
};

export type CoffeeJourneyStats = {
  streak_days: number;
  coffees_tried: number;
  favorite_drink: string | null;
  favorite_drink_avg_rating: number | null;
};

export async function addCoffeeToCalendar(
  payload: {
    drink_id: string;
    drink_name: string;
    rating: number;
    notes?: string;
    source?: string;
    temperature?: "hot" | "iced";
  },
  token = getToken(),
) {
  if (!token) {
    throw new Error("Not authenticated");
  }

  const response = await apiFetch("/calendar/logs", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      ...payload,
      source: payload.source ?? "brewmatch_recommendation",
    }),
  });

  if (!response.ok) {
    throw new Error(await parseApiError(response));
  }

  return response.json() as Promise<CoffeeLog>;
}

export async function deleteCoffeeLog(logId: number, token = getToken()) {
  if (!token) {
    throw new Error("Not authenticated");
  }

  const response = await apiFetch(`/calendar/logs/${logId}`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${token}` },
  });

  if (!response.ok) {
    throw new Error(await parseApiError(response));
  }
}

export async function fetchCalendarMonth(
  year: number,
  month: number,
  token = getToken(),
) {
  if (!token) {
    throw new Error("Not authenticated");
  }

  const response = await apiFetch(
    `/calendar/month?year=${year}&month=${month}`,
    {
      headers: { Authorization: `Bearer ${token}` },
    },
  );

  if (!response.ok) {
    throw new Error(await parseApiError(response));
  }

  return response.json() as Promise<CalendarMonth>;
}

export async function fetchCoffeeJourneyStats(token = getToken()) {
  if (!token) {
    throw new Error("Not authenticated");
  }

  const response = await apiFetch("/calendar/stats", {
    headers: { Authorization: `Bearer ${token}` },
  });

  if (!response.ok) {
    throw new Error(await parseApiError(response));
  }

  return response.json() as Promise<CoffeeJourneyStats>;
}

export type TasteProfile = {
  preferred_temperature: string | null;
  sweetness: string | null;
  preferred_flavors: string[];
  strength: string | null;
  milk_preference: string | null;
  confidence: "none" | "low" | "full";
  rated_count: number;
  temperature_mix: {
    iced: number;
    hot: number;
  };
  sweetness_mix: {
    low: number;
    medium: number;
    high: number;
  };
};

export type PersonalizedDrink = {
  drink_id: string;
  base_drink: string;
  display_name: string;
  temperature: string;
  sweetness: string;
  syrup: string | null;
  modifier: string | null;
  explanation: string;
};

export type PersonalizedRecommendations = {
  taste_profile: TasteProfile;
  what_you_might_like: PersonalizedDrink | null;
  try_something_new: PersonalizedDrink | null;
  message: string | null;
};

export async function fetchPersonalizedRecommendations(token = getToken()) {
  if (!token) {
    throw new Error("Not authenticated");
  }

  const response = await apiFetch("/recommendations/personalized", {
    headers: { Authorization: `Bearer ${token}` },
  });

  if (!response.ok) {
    throw new Error(await parseApiError(response));
  }

  return response.json() as Promise<PersonalizedRecommendations>;
}

export async function fetchTasteProfile(token = getToken()) {
  if (!token) {
    throw new Error("Not authenticated");
  }

  const response = await apiFetch("/recommendations/taste-profile", {
    headers: { Authorization: `Bearer ${token}` },
  });

  if (!response.ok) {
    throw new Error(await parseApiError(response));
  }

  return response.json() as Promise<TasteProfile>;
}

export type CatalogDrink = {
  id: string;
  name: string;
  temperatures: Array<"hot" | "iced">;
  compatible_syrups: string[];
};

export type DrinkCatalog = {
  drinks: CatalogDrink[];
  syrups: string[];
};

export async function fetchDrinkCatalog(token = getToken()) {
  if (!token) {
    throw new Error("Not authenticated");
  }

  const response = await apiFetch("/catalog/drinks", {
    headers: { Authorization: `Bearer ${token}` },
  });

  if (!response.ok) {
    throw new Error(await parseApiError(response));
  }

  return response.json() as Promise<DrinkCatalog>;
}
