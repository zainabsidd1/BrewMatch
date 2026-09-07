import Image from "next/image";
import Link from "next/link";

import { brewButtonClassName } from "@/lib/buttonStyles";

export default function QuizCard() {
  return (
    <article className="flex h-full flex-col rounded-2xl bg-white/95 p-6 shadow-[0_8px_32px_rgba(59,35,20,0.1)] backdrop-blur-sm transition hover:shadow-[0_12px_36px_rgba(59,35,20,0.14)]">
      <div className="mb-4 flex items-center gap-3">
        <div className="flex size-12 shrink-0 items-center justify-center rounded-2xl bg-[#F3E7DA]">
          <Image
            src="/coffee-cup-icon.png"
            alt=""
            width={28}
            height={28}
            className="size-7"
            aria-hidden
          />
        </div>
        <h2 className="text-xl font-bold text-[#3B2314]">
          Coffee Personality Quiz
        </h2>
      </div>

      <p className="text-sm leading-relaxed text-stone-600">
        Answer a few fun questions about your vibe, habits, and taste. We&apos;ll
        match you with a coffee that fits your personality. Perfect if you&apos;re
        not sure where to start.
      </p>

      <Link
        href="/quiz"
        className={`${brewButtonClassName} mt-4 inline-flex self-start px-6 py-2.5 text-sm`}
      >
        Take Quiz
      </Link>
    </article>
  );
}
