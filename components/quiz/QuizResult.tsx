type QuizMatchProps = {
  drinkName: string;
  description: string;
  categories: string[];
  personalizedMatch: string;
};

export default function QuizResult({
  drinkName,
  description,
  categories,
  personalizedMatch,
}: QuizMatchProps) {
  return (
    <div className="flex flex-col rounded-2xl bg-white px-6 py-7 shadow-[0_8px_32px_rgba(59,35,20,0.12)] sm:px-9 sm:py-8">
      <p className="text-center text-sm font-medium uppercase tracking-wide text-[#8B5E3C]">
        Your BrewMatch
      </p>
      <h1 className="mt-2 text-center text-[1.75rem] font-bold tracking-tight text-[#3B2314] sm:text-3xl">
        {drinkName}
      </h1>

      <div className="mt-3.5 flex flex-wrap justify-center gap-2">
        {categories.map((category) => (
          <span
            key={category}
            className="rounded-full bg-[#F3E7DA] px-3 py-1 text-xs font-semibold text-[#3B2314]"
          >
            {category}
          </span>
        ))}
      </div>

      <p className="mx-auto mt-5 max-w-xl text-center text-sm leading-relaxed text-stone-600 sm:text-[0.95rem]">
        {description}
      </p>

      <div className="mx-auto mt-6 max-w-xl rounded-xl border border-[#E8C9A8] bg-[#FBF6F0]/70 px-5 py-5">
        <h2 className="text-xs font-bold uppercase tracking-wide text-[#8B5E3C] sm:text-sm">
          Why this is the perfect match
        </h2>
        <p className="mt-2.5 text-sm leading-relaxed text-[#3B2314] sm:text-[0.95rem]">
          {personalizedMatch}
        </p>
      </div>
    </div>
  );
}
