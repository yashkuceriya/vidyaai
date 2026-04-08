export const LANGUAGES = [
  { code: "hindi", label: "हिंदी", flag: "🇮🇳" },
  { code: "english", label: "English", flag: "🇬🇧" },
  { code: "marathi", label: "मराठी", flag: "🇮🇳" },
  { code: "tamil", label: "தமிழ்", flag: "🇮🇳" },
] as const;

export const SUBJECTS = [
  { code: "general", label: "General", icon: "📚" },
  { code: "math", label: "Math", icon: "🔢" },
  { code: "science", label: "Science", icon: "🔬" },
  { code: "history", label: "History", icon: "📜" },
  { code: "geography", label: "Geography", icon: "🌍" },
] as const;

export const GRADES = Array.from({ length: 7 }, (_, i) => ({
  value: i + 6,
  label: `Class ${i + 6}`,
}));
