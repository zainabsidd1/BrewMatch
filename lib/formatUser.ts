export function getDisplayName(email: string) {
  const localPart = email.split("@")[0] ?? "friend";
  return localPart.charAt(0).toUpperCase() + localPart.slice(1);
}
