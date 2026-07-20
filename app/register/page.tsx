import AuthCard from "@/components/auth/AuthCard";
import RegisterForm from "@/components/auth/RegisterForm";

export default function RegisterPage() {
  return (
    <main className="relative flex min-h-[calc(100vh-57px)] items-center justify-center px-4 py-10">
      <div
        className="absolute inset-0 bg-repeat"
        style={{ backgroundImage: "url('/coffee-pattern.png')" }}
        aria-hidden
      />
      <div className="absolute inset-0 bg-white/70" aria-hidden />
      <div className="relative z-10">
        <AuthCard>
          <RegisterForm />
        </AuthCard>
      </div>
    </main>
  );
}
