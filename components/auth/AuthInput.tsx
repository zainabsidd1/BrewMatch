import type { InputHTMLAttributes, ReactNode } from "react";

type AuthInputProps = {
  id: string;
  label: string;
  icon: ReactNode;
  rightElement?: ReactNode;
  error?: string;
} & InputHTMLAttributes<HTMLInputElement>;

export default function AuthInput({
  id,
  label,
  icon,
  rightElement,
  error,
  className = "",
  ...inputProps
}: AuthInputProps) {
  return (
    <div className="relative">
      <label
        htmlFor={id}
        className="absolute -top-2.5 left-6 z-10 bg-white px-1 text-xs font-semibold text-stone-600"
      >
        {label}
      </label>
      <div
        className={`flex items-center gap-3 rounded-full border px-5 py-3 text-stone-500 ${
          error ? "border-red-400" : "border-stone-300"
        }`}
      >
        {icon}
        <input
          id={id}
          className={`flex-1 bg-transparent text-sm text-stone-800 outline-none placeholder:text-stone-400 ${className}`}
          {...inputProps}
        />
        {rightElement}
      </div>
      {error ? <p className="mt-1 px-2 text-xs text-red-500">{error}</p> : null}
    </div>
  );
}
