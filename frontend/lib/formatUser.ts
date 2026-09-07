export function getDisplayName(email: string, name?: string | null) {
  const trimmedName = name?.trim();
  if (trimmedName) {
    return trimmedName;
  }
  const localPart = email.split("@")[0] ?? "friend";
  return localPart.charAt(0).toUpperCase() + localPart.slice(1);
}
