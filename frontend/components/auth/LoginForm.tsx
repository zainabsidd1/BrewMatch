"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import AuthInput from "@/components/auth/AuthInput";
import { EyeIcon, EyeOffIcon, LockIcon, MailIcon } from "@/components/auth/AuthIcons";
import { loginUser } from "@/lib/api";
import { saveToken } from "@/lib/auth";
import { validateLoginForm } from "@/lib/validateLogin";

type FormErrors = {
  email?: string;
  password?: string;
};

export default function LoginForm() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [errors, setErrors] = useState<FormErrors>({});
  const [apiError, setApiError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setApiError("");

    const validationErrors = validateLoginForm({ email, password });
    setErrors(validationErrors);

    if (Object.keys(validationErrors).length > 0) {
      return;
    }

    setIsSubmitting(true);

    try {
      const { access_token } = await loginUser(email, password);
      saveToken(access_token);
      router.push("/dashboard");
    } catch (error) {
      setApiError(
        error instanceof Error ? error.message : "Login failed. Please try again.",
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div>
      <h1 className="mb-10 text-center text-2xl font-bold text-[#3B2314]">
        Let&apos;s get brewing!
      </h1>

      <form className="space-y-6" onSubmit={handleSubmit} noValidate>
        {apiError ? (
          <p className="rounded-xl bg-red-50 px-4 py-3 text-center text-sm text-red-600">
            {apiError}
          </p>
        ) : null}

        <AuthInput
          id="email"
          label="Email"
          type="email"
          name="email"
          autoComplete="email"
          placeholder="email@gmail.com"
          icon={<MailIcon />}
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          error={errors.email}
        />

        <div>
          <AuthInput
            id="password"
            label="Password"
            type={showPassword ? "text" : "password"}
            name="password"
            autoComplete="current-password"
            placeholder="Enter your password"
            icon={<LockIcon />}
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            error={errors.password}
            rightElement={
              <button
                type="button"
                onClick={() => setShowPassword((current) => !current)}
                className="text-stone-400 transition hover:text-stone-600"
                aria-label={showPassword ? "Hide password" : "Show password"}
              >
                {showPassword ? <EyeOffIcon /> : <EyeIcon />}
              </button>
            }
          />
        </div>

        <div className="mx-auto h-px w-3/4 bg-[#C4A484]" aria-hidden />

        <p className="text-center text-sm text-stone-500">
          Don&apos;t have an account?{" "}
          <Link
            href="/register"
            className="font-semibold text-[#B8734A] transition hover:text-[#3B2314]"
          >
            Sign up
          </Link>
        </p>

        <button
          type="submit"
          disabled={isSubmitting}
          className="w-full rounded-full bg-[#E8C9A8] py-3 text-sm font-bold text-[#3B2314] transition hover:bg-[#ddb68f] disabled:cursor-not-allowed disabled:opacity-70"
        >
          {isSubmitting ? "Logging in..." : "Login"}
        </button>
      </form>
    </div>
  );
}
