export default function WarmArcBackground() {
  return (
    <>
      <div
        className="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style={{ backgroundImage: "url('/warm-arcs.svg')" }}
        aria-hidden
      />
      <div className="absolute inset-0 bg-white/30" aria-hidden />
    </>
  );
}
