"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import DashboardBackground from "@/components/dashboard/DashboardBackground";
import QuizCard from "@/components/dashboard/QuizCard";
import { fetchCurrentUser, type User } from "@/lib/api";
import { clearToken, getToken } from "@/lib/auth";
import { getDisplayName } from "@/lib/formatUser";

export default function DashboardPage() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const token = getToken();

    if (!token) {
      router.replace("/login");
      return;
    }

    fetchCurrentUser(token)
      .then(setUser)
      .catch(() => {
        clearToken();
        router.replace("/login");
      });
  }, [router]);

  if (!user) {
    return (
      <DashboardBackground>
        <div className="flex min-h-[calc(100vh-57px)] items-center justify-center px-[10%]">
          <p className="text-stone-500">Loading your account...</p>
        </div>
      </DashboardBackground>
    );
  }

  const displayName = getDisplayName(user.email);

  return (
    <DashboardBackground>
      <div className="flex min-h-[calc(100vh-57px)] flex-col items-start px-10 pb-10 pt-8 sm:px-14 md:px-20 md:pt-10">
        <div className="w-fit border-b border-black pb-3">
          <div className="flex flex-wrap items-baseline gap-x-4 gap-y-1 text-left">
            <h1 className="text-3xl font-bold tracking-tight text-[#3B2314] sm:text-4xl">
              Welcome, {displayName}!
            </h1>
            <p className="text-base text-stone-600 sm:text-lg">
              Discover your next favorite cup.
            </p>
          </div>
        </div>

        <section className="mt-8 w-full max-w-md">
          <QuizCard />
        </section>
      </div>
    </DashboardBackground>
  );
}
