"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import AuthInput from "@/components/auth/AuthInput";
import { EyeIcon, EyeOffIcon, LockIcon, MailIcon, UserIcon } from "@/components/auth/AuthIcons";
import { registerUser } from "@/lib/api";
import { validateRegisterForm } from "@/lib/validateRegister";

type FormErrors = {
  name?: string;
  email?: string;
  password?: string;
  confirmPassword?: string;
};

export default function RegisterForm() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [errors, setErrors] = useState<FormErrors>({});
  const [apiError, setApiError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setApiError("");

    const validationErrors = validateRegisterForm({
      name,
      email,
      password,
      confirmPassword,
    });
    setErrors(validationErrors);

    if (Object.keys(validationErrors).length > 0) {
      return;
    }

    setIsSubmitting(true);

    try {
      await registerUser(email, password, name);
      router.push("/login");
    } catch (error) {
      setApiError(
        error instanceof Error
          ? error.message
          : "Registration failed. Please try again.",
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div>
      <h1 className="mb-10 text-center text-2xl font-bold text-[#3B2314]">
        Join BrewMatch
      </h1>

      <form className="space-y-6" onSubmit={handleSubmit} noValidate>
        {apiError ? (
          <p className="rounded-xl bg-red-50 px-4 py-3 text-center text-sm text-red-600">
            {apiError}
          </p>
        ) : null}

        <AuthInput
          id="name"
          label="Name"
          type="text"
          name="name"
          autoComplete="name"
          placeholder="Your name"
          icon={<UserIcon />}
          value={name}
          onChange={(event) => setName(event.target.value)}
          error={errors.name}
        />

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

        <AuthInput
          id="password"
          label="Password"
          type={showPassword ? "text" : "password"}
          name="password"
          autoComplete="new-password"
          placeholder="Create a password"
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

        <AuthInput
          id="confirmPassword"
          label="Confirm Password"
          type={showConfirmPassword ? "text" : "password"}
          name="confirmPassword"
          autoComplete="new-password"
          placeholder="Confirm your password"
          icon={<LockIcon />}
          value={confirmPassword}
          onChange={(event) => setConfirmPassword(event.target.value)}
          error={errors.confirmPassword}
          rightElement={
            <button
              type="button"
              onClick={() => setShowConfirmPassword((current) => !current)}
              className="text-stone-400 transition hover:text-stone-600"
              aria-label={showConfirmPassword ? "Hide password" : "Show password"}
            >
              {showConfirmPassword ? <EyeOffIcon /> : <EyeIcon />}
            </button>
          }
        />

        <p className="pt-2 text-center text-sm text-stone-500">
          Already have an account?{" "}
          <Link
            href="/login"
            className="font-semibold text-[#B8734A] transition hover:text-[#3B2314]"
          >
            Log in
          </Link>
        </p>

        <button
          type="submit"
          disabled={isSubmitting}
          className="w-full rounded-full bg-[#E8C9A8] py-3 text-sm font-bold text-[#3B2314] transition hover:bg-[#ddb68f] disabled:cursor-not-allowed disabled:opacity-70"
        >
          {isSubmitting ? "Creating account..." : "Sign up"}
        </button>
      </form>
    </div>
  );
}
