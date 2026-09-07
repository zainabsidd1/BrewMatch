import AuthCard from "@/components/auth/AuthCard";
import LoginForm from "@/components/auth/LoginForm";
import WarmArcBackground from "@/components/auth/WarmArcBackground";

export default function LoginPage() {
  return (
    <main className="relative flex min-h-[calc(100vh-57px)] items-center justify-center px-4 py-10">
      <WarmArcBackground />
      <div className="relative z-10">
        <AuthCard>
          <LoginForm />
        </AuthCard>
      </div>
    </main>
  );
}
