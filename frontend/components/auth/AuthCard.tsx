type AuthCardProps = {
  children: React.ReactNode;
};

export default function AuthCard({ children }: AuthCardProps) {
  return (
    <div className="w-full max-w-md rounded-2xl bg-white px-8 py-16 shadow-[0_8px_32px_rgba(59,35,20,0.12)]">
      {children}
    </div>
  );
}
