import AuthCard from "@/components/auth/AuthCard";
import RegisterForm from "@/components/auth/RegisterForm";
import WarmArcBackground from "@/components/auth/WarmArcBackground";

export default function RegisterPage() {
  return (
    <main className="relative flex min-h-[calc(100vh-57px)] items-center justify-center px-4 py-10">
      <WarmArcBackground />
      <div className="relative z-10">
        <AuthCard>
          <RegisterForm />
        </AuthCard>
      </div>
    </main>
  );
}
