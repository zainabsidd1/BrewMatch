"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import QuizForm from "@/components/quiz/QuizForm";
import { getToken } from "@/lib/auth";

export default function QuizPage() {
  const router = useRouter();
  const [ready, setReady] = useState(false);

  useEffect(() => {
    if (!getToken()) {
      router.replace("/login");
      return;
    }
    setReady(true);
  }, [router]);

  if (!ready) {
    return (
      <main className="relative flex min-h-[calc(100vh-57px)] items-center justify-center px-4 py-5">
        <div
          className="absolute inset-0 bg-repeat"
          style={{ backgroundImage: "url('/coffee-pattern.png')" }}
          aria-hidden
        />
        <div className="absolute inset-0 bg-white/70" aria-hidden />
        <p className="relative z-10 text-stone-500">Loading quiz...</p>
      </main>
    );
  }

  return (
    <main className="relative flex min-h-[calc(100vh-57px)] items-center justify-center px-4 py-5">
      <div
        className="absolute inset-0 bg-repeat"
        style={{ backgroundImage: "url('/coffee-pattern.png')" }}
        aria-hidden
      />
      <div className="absolute inset-0 bg-white/70" aria-hidden />
      <div className="relative z-10 w-full max-w-[46rem]">
        <QuizForm />
      </div>
    </main>
  );
}
