type DashboardBackgroundProps = {
  children: React.ReactNode;
};

export default function DashboardBackground({
  children,
}: DashboardBackgroundProps) {
  return (
    <main className="relative min-h-[calc(100vh-57px)] bg-[#F3E7DA]">
      <div className="relative z-10">{children}</div>
    </main>
  );
}
