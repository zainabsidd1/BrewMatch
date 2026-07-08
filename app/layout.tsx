import type { Metadata } from "next";
import BrandMark from "@/components/BrandMark";
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
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link
          rel="preconnect"
          href="https://fonts.gstatic.com"
          crossOrigin=""
        />
        <link
          href="https://fonts.googleapis.com/css2?family=DynaPuff:wght@400..700&display=swap"
          rel="stylesheet"
        />
      </head>
      <body>
        <header className="fixed left-4 top-4 z-50">
          <BrandMark />
        </header>
        {children}
      </body>
    </html>
  );
}
