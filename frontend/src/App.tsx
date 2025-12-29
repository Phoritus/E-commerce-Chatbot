import React, { useEffect, useMemo, useRef, useState } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";

type Role = "user" | "bot";

type MessageType = "text" | "loading" | "error";

type Message = {
  id: string;
  role: Role;
  type: MessageType;
  content: React.ReactNode;
  createdAt: number; // epoch ms
  markdown?: string;
};


const CHAT_STORAGE_KEY = "chat_history_v1";
const THREAD_ID_KEY = "chat_thread_id_v1";


const formatTime = (ts: number) => {
  const d = new Date(ts);
  return d.toLocaleTimeString("en-US", {
    hour: "2-digit",
    minute: "2-digit",
    timeZone: "Asia/Bangkok"
  });
};

export default function App() {
  const [messages, setMessages] = useState<Message[]>(() => {
    try {
      const raw = localStorage.getItem(CHAT_STORAGE_KEY);
      if (raw) {
        const parsed = JSON.parse(raw) as Array<{
          role: Role;
          type: MessageType;
          content: string;
          markdown?: string;
        }>;
        return parsed.map((m) => {
          if (m.role === "bot" && m.markdown) {
            return {
              id: crypto.randomUUID(),
              role: m.role,
              type: m.type,
              content: (
                <ReactMarkdown
                  components={{
                    a: ({ node, ...props }) => (
                      <a
                        {...props}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="underline text-indigo-300 hover:text-indigo-200"
                      />
                    ),
                  }}
                >
                  {m.markdown}
                </ReactMarkdown>
              ),
              markdown: m.markdown,
              createdAt: Date.now(),
            };
          }
          return {
            id: crypto.randomUUID(),
            role: m.role,
            type: m.type,
            content: m.content,
            createdAt: Date.now(),
          };
        });
      }
    } catch {
      // ignore and fall back to default
    }
    return [
      {
        id: crypto.randomUUID(),
        role: "bot",
        type: "text",
        content:
          "Hello! I'm your shopping assistant 😊 Type your question to get started.",
        createdAt: Date.now(),
      },
    ];
  });

  const [input, setInput] = useState("");
  const [isSending, setIsSending] = useState(false);
  const inputRef = useRef<HTMLTextAreaElement | null>(null);

  const canSend = useMemo(() => input.trim().length > 0 && !isSending, [
    input,
    isSending,
  ]);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  // Persist chat history (only role/type/plain-text content) to localStorage
  useEffect(() => {
    try {
      const payload = messages.map((m) => ({
        role: m.role,
        type: m.type,
        content:
          typeof m.content === "string" ? m.content : m.markdown ?? "",
        markdown: m.markdown,
      }));
      localStorage.setItem(CHAT_STORAGE_KEY, JSON.stringify(payload));
    } catch {
      // ignore storage errors
    }
  }, [messages]);

  const pushMessage = (m: Omit<Message, "id" | "createdAt">) => {
    setMessages((prev) => [
      ...prev,
      { id: crypto.randomUUID(), createdAt: Date.now(), ...m },
    ]);
  };

  const handleResetChat = () => {
    const initial: Message = {
      id: crypto.randomUUID(),
      role: "bot",
      type: "text",
      content:
        "Hello! I'm your shopping assistant 😊 Type your question to get started.",
      createdAt: Date.now(),
    };
    setMessages([initial]);
    try {
      localStorage.removeItem(CHAT_STORAGE_KEY);
      localStorage.removeItem(THREAD_ID_KEY);
    } catch {
      // ignore
    }
  };

  const simulateBotReply = (_userText: string) => {
    const loadingId = crypto.randomUUID();
    const axiosInstance = axios.create({
      baseURL: 'http://localhost:8000'
    });

    // Show loading bubble immediately
    setMessages((prev) => [
      ...prev,
      {
        id: loadingId,
        role: "bot",
        type: "loading",
        content: "Typing…",
        createdAt: Date.now(),
      },
    ]);
    // Get or Create Thread ID
    let threadId = localStorage.getItem(THREAD_ID_KEY);
    if (!threadId) {
      threadId = crypto.randomUUID();
      localStorage.setItem(THREAD_ID_KEY, threadId);
    }

    // Backend return with markdown formatted reply
    axiosInstance.post('/api/v1/chat', { question: _userText, thread_id: threadId })
      .then((res) => {
        const botReply = res.data.answer;
        const repylRendered = (
          <ReactMarkdown
            components={{
              a: ({ node, ...props }) => (
                <a
                  {...props}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="underline text-indigo-300 hover:text-indigo-200"
                />
              ),
            }}
          >
            {botReply}
          </ReactMarkdown>
        );

        // Remove loading bubble then push the real reply
        setMessages((prev) => prev.filter((m) => m.id !== loadingId));
        pushMessage({
          role: 'bot',
          type: 'text',
          content: repylRendered,
          markdown: botReply,
        });
      })
      .catch((err) => {
        // Remove loading bubble then push an error bubble
        setMessages((prev) => prev.filter((m) => m.id !== loadingId));
        const msg = err?.response?.data?.detail || err?.message || 'Request failed';
        pushMessage({ role: 'bot', type: 'error', content: `Error: ${msg}` });
      });
  };

  const handleSend = () => {
    if (!canSend) return;
    const text = input.trim();
    setIsSending(true);
    pushMessage({ role: "user", type: "text", content: text });
    setInput("");
    simulateBotReply(text);
    setIsSending(false);
  };

  const handleKeyDown: React.KeyboardEventHandler<HTMLTextAreaElement> = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="min-h-dvh flex flex-col bg-black text-zinc-100">
      {/* Main */}
      <div className="flex flex-col min-h-dvh">
        <header className="border-b border-zinc-800 bg-zinc-950/80 backdrop-blur-sm">
          <div className="mx-auto flex w-full max-w-3xl items-center justify-between px-4 py-3">
            <h1 className="text-base font-semibold text-zinc-100">
              E-Commerce Chat Bot
            </h1>
          </div>
        </header>
        <main className="flex-1 overflow-auto">
          <div className="mx-auto w-full max-w-3xl px-4 py-6">
            {messages.map((m) => (
              <MessageBubble key={m.id} msg={m} />
            ))}
          </div>
        </main>

        {/* Prompt bar */}
        <div className="sticky bottom-0 w-full bg-linear-to-t from-black via-black/80 to-transparent pt-4">
          <div className="mx-auto w-full max-w-3xl px-4 pb-6">
            <div className="rounded-2xl border border-zinc-800 bg-zinc-950 focus-within:ring-2 focus-within:ring-indigo-600/60">
              <textarea
                ref={inputRef}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask anything… (Enter to send)"
                rows={1}
                className="w-full bg-transparent px-4 py-3 resize-none leading-relaxed max-h-[35dvh] placeholder:text-zinc-500 focus:outline-none"
              />
              <div className="flex items-center justify-end px-2 pb-2">
                <button
                  onClick={handleSend}
                  disabled={!canSend}
                  className="rounded-lg px-3 py-1.5 text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 disabled:cursor-not-allowed"
                >
                  Send
                </button>
                <button
                  onClick={handleResetChat}
                  className="ml-2 rounded-lg px-3 py-1.5 text-sm font-medium text-zinc-200 bg-zinc-800 hover:bg-zinc-700"
                >
                  Reset chat
                </button>
              </div>
            </div>
            <p className="mt-2 text-center text-xs text-zinc-500">AI assistant may produce inaccurate info. Verify important details.</p>
          </div>
        </div>
      </div>
    </div>
  );
}

function MessageBubble({ msg }: { msg: Message }) {
  const isUser = msg.role === "user";
  return (
    <div className={`flex my-1.5 ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[85%] rounded-2xl border px-3 py-2 shadow-sm ${isUser
          ? "border-indigo-500/40 bg-indigo-600 text-white"
          : "border-zinc-800 bg-zinc-900 text-zinc-100"
          }`}
      >
        <div className="flex items-baseline justify-between gap-2 text-xs text-zinc-400">
          <span className={isUser ? "text-white/90" : "text-zinc-300"}>
            {isUser ? "You" : "Assistant"}
          </span>
          <time>{formatTime(msg.createdAt)}</time>
        </div>
        <div className="mt-1 whitespace-pre-wrap leading-relaxed text-sm">
          {msg.content}
        </div>
        {msg.type === "loading" ? (
          <div className="mt-2 flex justify-end">
            <img
              src="/loading.svg"
              alt="Loading"
              className="w-6 h-6 animate-spin-slow"
            />
          </div>
        ) : null}
      </div>
    </div>
  );
}

// Removed TypingDots in favor of loading.svg spinner


