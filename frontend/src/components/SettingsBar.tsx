"use client";

import { LANGUAGES, SUBJECTS, GRADES } from "@/lib/constants";

interface SettingsBarProps {
  language: string;
  subject: string;
  grade: number;
  onLanguageChange: (lang: string) => void;
  onSubjectChange: (subject: string) => void;
  onGradeChange: (grade: number) => void;
}

export function SettingsBar({
  language,
  subject,
  grade,
  onLanguageChange,
  onSubjectChange,
  onGradeChange,
}: SettingsBarProps) {
  return (
    <div className="flex flex-wrap items-center gap-3 p-3 bg-white/80 backdrop-blur-sm border-b border-gray-200">
      {/* Language */}
      <div className="flex items-center gap-2">
        <label className="text-xs font-medium text-gray-500 uppercase tracking-wide">
          Language
        </label>
        <select
          value={language}
          onChange={(e) => onLanguageChange(e.target.value)}
          className="text-sm border border-gray-200 rounded-lg px-3 py-1.5 bg-white focus:ring-2 focus:ring-orange-300 focus:border-orange-400 outline-none"
        >
          {LANGUAGES.map((lang) => (
            <option key={lang.code} value={lang.code}>
              {lang.flag} {lang.label}
            </option>
          ))}
        </select>
      </div>

      {/* Subject */}
      <div className="flex items-center gap-2">
        <label className="text-xs font-medium text-gray-500 uppercase tracking-wide">
          Subject
        </label>
        <select
          value={subject}
          onChange={(e) => onSubjectChange(e.target.value)}
          className="text-sm border border-gray-200 rounded-lg px-3 py-1.5 bg-white focus:ring-2 focus:ring-orange-300 focus:border-orange-400 outline-none"
        >
          {SUBJECTS.map((s) => (
            <option key={s.code} value={s.code}>
              {s.icon} {s.label}
            </option>
          ))}
        </select>
      </div>

      {/* Grade */}
      <div className="flex items-center gap-2">
        <label className="text-xs font-medium text-gray-500 uppercase tracking-wide">
          Grade
        </label>
        <select
          value={grade}
          onChange={(e) => onGradeChange(Number(e.target.value))}
          className="text-sm border border-gray-200 rounded-lg px-3 py-1.5 bg-white focus:ring-2 focus:ring-orange-300 focus:border-orange-400 outline-none"
        >
          {GRADES.map((g) => (
            <option key={g.value} value={g.value}>
              {g.label}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}
