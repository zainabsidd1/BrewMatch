import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "BrewMatch",
  description: "Find your perfect brew",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
