import "@testing-library/jest-dom/vitest";
import { cleanup } from "@testing-library/react";
import { afterEach, vi } from "vitest";

afterEach(() => {
  cleanup();
});

vi.mock("next/image", () => ({
  default: function MockImage({
    alt = "",
    ...props
  }: {
    alt?: string;
    [key: string]: unknown;
  }) {
    return <img alt={alt} {...props} />;
  },
}));
