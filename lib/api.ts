import { getToken } from "@/lib/auth";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

type ApiErrorBody = {
  detail?: string | { msg: string }[];
};

export type User = {
  id: number;
  email: string;
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

  return "Something went wrong. Please try again.";
}

export async function registerUser(email: string, password: string) {
  const response = await fetch(`${API_URL}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    throw new Error(await parseApiError(response));
  }

  return response.json() as Promise<User>;
}

export async function loginUser(email: string, password: string) {
  const response = await fetch(`${API_URL}/auth/login`, {
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

  const response = await fetch(`${API_URL}/auth/me`, {
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

  const response = await fetch(`${API_URL}/quiz/match`, {
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
  },
  token = getToken(),
) {
  if (!token) {
    throw new Error("Not authenticated");
  }

  const response = await fetch(`${API_URL}/calendar/logs`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      ...payload,
      source: "brewmatch_recommendation",
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

  const response = await fetch(`${API_URL}/calendar/logs/${logId}`, {
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

  const response = await fetch(
    `${API_URL}/calendar/month?year=${year}&month=${month}`,
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

  const response = await fetch(`${API_URL}/calendar/stats`, {
    headers: { Authorization: `Bearer ${token}` },
  });

  if (!response.ok) {
    throw new Error(await parseApiError(response));
  }

  return response.json() as Promise<CoffeeJourneyStats>;
}
