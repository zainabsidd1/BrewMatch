import Image from "next/image";

type QuizProgressProps = {
  currentIndex: number;
  totalSteps: number;
};

export default function QuizProgress({
  currentIndex,
  totalSteps,
}: QuizProgressProps) {
  const progressPercent =
    totalSteps <= 1 ? 100 : (currentIndex / (totalSteps - 1)) * 100;

  return (
    <div className="rounded-t-2xl border-b border-[#E8C9A8]/80 bg-[#FBF6F0] px-6 pb-4 pt-5 sm:px-9">
      <div className="mb-3 flex items-center justify-between text-xs font-semibold text-[#8B5E3C] sm:text-sm">
        <span>
          Question {currentIndex + 1} of {totalSteps}
        </span>
        <span>{Math.round(progressPercent)}%</span>
      </div>

      <div
        className="relative h-2.5 w-full rounded-full bg-[#E8C9A8]/55"
        role="progressbar"
        aria-valuemin={0}
        aria-valuemax={100}
        aria-valuenow={Math.round(progressPercent)}
        aria-label="Quiz progress"
      >
        <div
          className="absolute inset-y-0 left-0 rounded-full bg-[#8B5E3C] transition-[width] duration-500 ease-out"
          style={{ width: `${progressPercent}%` }}
        />
        <div
          className="absolute top-1/2 -translate-x-1/2 -translate-y-1/2 transition-[left] duration-500 ease-out"
          style={{
            left: `clamp(11px, ${progressPercent}%, calc(100% - 11px))`,
          }}
        >
          <Image
            src="/coffee-bean.svg"
            alt=""
            width={20}
            height={28}
            className="drop-shadow-sm"
            aria-hidden
          />
        </div>
      </div>
    </div>
  );
}
