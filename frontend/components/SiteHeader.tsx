"use client";

import { usePathname, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import BrandMark from "@/components/BrandMark";
import { brewButtonClassName } from "@/lib/buttonStyles";
import { clearToken, getToken } from "@/lib/auth";

export default function SiteHeader() {
  const pathname = usePathname();
  const router = useRouter();
  const [showLogout, setShowLogout] = useState(false);

  useEffect(() => {
    const isAuthedPage =
      pathname === "/dashboard" || pathname.startsWith("/quiz");
    setShowLogout(isAuthedPage && Boolean(getToken()));
  }, [pathname]);

  function handleLogout() {
    clearToken();
    router.push("/login");
  }

  return (
    <header className="bg-white">
      <div className="flex items-center justify-between px-5 py-3">
        <BrandMark />
        {showLogout ? (
          <button
            type="button"
            onClick={handleLogout}
            className={`${brewButtonClassName} px-4 py-2 text-sm`}
          >
            Log out
          </button>
        ) : null}
      </div>
      <div className="h-px w-full bg-gray-300" />
    </header>
  );
}
