"use client";

import { useState, useRef, useEffect, useCallback } from "react";
import { ChatMessage, type Message } from "@/components/ChatMessage";
import { VoiceButton } from "@/components/VoiceButton";
import { SettingsBar } from "@/components/SettingsBar";
import { sendMessage, sendVoice } from "@/lib/api";

const WELCOME_MESSAGES: Record<string, string> = {
  hindi:
    "नमस्ते! मैं VidyaAI हूँ, आपका शिक्षा सहायक। आप मुझसे हिंदी में कोई भी सवाल पूछ सकते हैं।",
  english:
    "Hello! I'm VidyaAI, your education assistant. Ask me any question about your studies!",
  marathi:
    "नमस्कार! मी VidyaAI आहे, तुमचा शिक्षण सहाय्यक. तुम्ही मला मराठीत कोणताही प्रश्न विचारू शकता.",
  tamil:
    "வணக்கம்! நான் VidyaAI, உங்கள் கல்வி உதவியாளர். உங்கள் படிப்பைப் பற்றி எந்த கேள்வியையும் கேளுங்கள்!",
};

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [language, setLanguage] = useState("hindi");
  const [subject, setSubject] = useState("general");
  const [grade, setGrade] = useState(8);
  const [conversationId, setConversationId] = useState<string | undefined>();
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    setMessages([
      { role: "assistant", content: WELCOME_MESSAGES[language] },
    ]);
    setConversationId(undefined);
  }, [language]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    const text = input.trim();
    if (!text || isLoading) return;

    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: text }]);
    setIsLoading(true);

    try {
      const res = await sendMessage({
        message: text,
        language,
        subject,
        grade,
        conversation_id: conversationId,
      });
      setConversationId(res.conversation_id);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: res.reply },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Sorry, something went wrong. Please try again.",
        },
      ]);
    } finally {
      setIsLoading(false);
      inputRef.current?.focus();
    }
  };

  const handleVoice = useCallback(
    async (blob: Blob) => {
      setIsLoading(true);
      try {
        const res = await sendVoice(
          blob,
          language,
          subject,
          grade,
          conversationId
        );
        setConversationId(res.conversation_id);
        setMessages((prev) => [
          ...prev,
          { role: "user", content: res.transcript },
          { role: "assistant", content: res.reply },
        ]);

        // Play audio response
        if (res.audio_url) {
          const audio = new Audio(res.audio_url);
          audio.play().catch(() => {});
        }
      } catch {
        setMessages((prev) => [
          ...prev,
          {
            role: "assistant",
            content: "Could not process voice input. Please try again.",
          },
        ]);
      } finally {
        setIsLoading(false);
      }
    },
    [language, subject, grade, conversationId]
  );

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-screen max-w-3xl mx-auto w-full">
      {/* Header */}
      <header className="bg-white/90 backdrop-blur-sm border-b border-gray-200 px-6 py-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-orange-400 to-orange-600 rounded-xl flex items-center justify-center text-white font-bold text-lg shadow-md">
            V
          </div>
          <div>
            <h1 className="text-xl font-bold text-gray-800">VidyaAI</h1>
            <p className="text-xs text-gray-500">
              Powered by Gemma 4 &bull; Multilingual Education Assistant
            </p>
          </div>
        </div>
      </header>

      {/* Settings */}
      <SettingsBar
        language={language}
        subject={subject}
        grade={grade}
        onLanguageChange={setLanguage}
        onSubjectChange={setSubject}
        onGradeChange={setGrade}
      />

      {/* Messages */}
      <div className="flex-1 overflow-y-auto chat-scroll px-4 py-6">
        {messages.map((msg, i) => (
          <ChatMessage key={i} message={msg} />
        ))}
        {isLoading && (
          <div className="flex justify-start mb-4">
            <div className="bg-white shadow-md border border-gray-100 rounded-2xl rounded-bl-sm px-4 py-3">
              <div className="text-xs font-semibold text-orange-600 mb-1">
                VidyaAI
              </div>
              <div className="flex gap-1">
                <span className="w-2 h-2 bg-orange-400 rounded-full animate-bounce" />
                <span
                  className="w-2 h-2 bg-orange-400 rounded-full animate-bounce"
                  style={{ animationDelay: "0.1s" }}
                />
                <span
                  className="w-2 h-2 bg-orange-400 rounded-full animate-bounce"
                  style={{ animationDelay: "0.2s" }}
                />
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="border-t border-gray-200 bg-white/90 backdrop-blur-sm p-4">
        <div className="flex items-end gap-2">
          <VoiceButton onRecordingComplete={handleVoice} disabled={isLoading} />
          <textarea
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={
              language === "hindi"
                ? "अपना सवाल यहाँ लिखें..."
                : language === "marathi"
                  ? "तुमचा प्रश्न येथे लिहा..."
                  : language === "tamil"
                    ? "உங்கள் கேள்வியை இங்கே எழுதுங்கள்..."
                    : "Type your question here..."
            }
            rows={1}
            className="flex-1 resize-none border border-gray-200 rounded-xl px-4 py-3 text-sm focus:ring-2 focus:ring-orange-300 focus:border-orange-400 outline-none"
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || isLoading}
            className="p-3 bg-orange-500 text-white rounded-xl hover:bg-orange-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
              className="w-5 h-5"
            >
              <path d="M3.478 2.404a.75.75 0 0 0-.926.941l2.432 7.905H13.5a.75.75 0 0 1 0 1.5H4.984l-2.432 7.905a.75.75 0 0 0 .926.94 60.519 60.519 0 0 0 18.445-8.986.75.75 0 0 0 0-1.218A60.517 60.517 0 0 0 3.478 2.404Z" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}
