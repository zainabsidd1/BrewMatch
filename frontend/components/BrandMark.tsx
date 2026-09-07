import Image from "next/image";

export default function BrandMark() {
  return (
    <div className="flex items-center gap-2">
      <Image
        src="/logo.png"
        alt="BrewMatch logo"
        width={40}
        height={40}
        priority
        className="size-10 shrink-0"
      />
      <span className="font-brand font-dynapuff text-lg font-semibold tracking-wide text-[#3B2314]">
        BrewMatch
      </span>
    </div>
  );
}
