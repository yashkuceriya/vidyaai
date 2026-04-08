"use client";

export interface Message {
  role: "user" | "assistant";
  content: string;
}

export function ChatMessage({ message }: { message: Message }) {
  const isUser = message.role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-4`}>
      <div
        className={`max-w-[80%] rounded-2xl px-4 py-3 ${
          isUser
            ? "bg-orange-500 text-white rounded-br-sm"
            : "bg-white text-gray-800 shadow-md border border-gray-100 rounded-bl-sm"
        }`}
      >
        {!isUser && (
          <div className="text-xs font-semibold text-orange-600 mb-1">
            VidyaAI
          </div>
        )}
        <div className="whitespace-pre-wrap text-sm leading-relaxed">
          {message.content}
        </div>
      </div>
    </div>
  );
}
