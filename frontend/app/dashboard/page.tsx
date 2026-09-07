"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import CoffeeJournalCard from "@/components/dashboard/CoffeeJournalCard";
import DashboardBackground from "@/components/dashboard/DashboardBackground";
import PersonalizedRecsCard from "@/components/dashboard/PersonalizedRecsCard";
import QuizCard from "@/components/dashboard/QuizCard";
import TasteProfileCard from "@/components/dashboard/TasteProfileCard";
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

  const displayName = getDisplayName(user.email, user.name);

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

        <div className="mt-8 flex w-full flex-col gap-6 xl:flex-row xl:items-start xl:justify-between">
          <section className="flex w-full max-w-md flex-col gap-6">
            <QuizCard />
            <PersonalizedRecsCard />
          </section>

          <section className="w-full max-w-sm xl:mt-2 xl:max-w-[19.5rem]">
            <TasteProfileCard />
          </section>

          <section className="w-full max-w-md xl:ml-0">
            <CoffeeJournalCard />
          </section>
        </div>
      </div>
    </DashboardBackground>
  );
}
