import { useEffect, useRef, useState } from "react";
import Composer from "./components/Composer";
import Header from "./components/Header";
import Message from "./components/Message";
import Welcome from "./components/Welcome";
import { ArrowDownIcon } from "./components/icons";
import { useChat } from "./hooks/useChat";
import { useTheme } from "./hooks/useTheme";
import { fetchMeta } from "./lib/api";
import type { Meta } from "./types";

export default function App() {
  const { theme, toggle } = useTheme();
  const { messages, isStreaming, send, stop, clear, regenerate, sendFeedback } =
    useChat();
  const [meta, setMeta] = useState<Meta | null>(null);
  const [connecting, setConnecting] = useState(true);
  const [showScrollBtn, setShowScrollBtn] = useState(false);

  const scrollRef = useRef<HTMLDivElement>(null);
  const bottomRef = useRef<HTMLDivElement>(null);
  const atBottomRef = useRef(true);

  useEffect(() => {
    let alive = true;
    fetchMeta()
      .then((m) => alive && setMeta(m))
      .catch(() => {})
      .finally(() => alive && setConnecting(false));
    return () => {
      alive = false;
    };
  }, []);

  // Only auto-scroll when the user is already near the bottom.
  useEffect(() => {
    if (atBottomRef.current) {
      bottomRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
    }
  }, [messages]);

  const onScroll = () => {
    const el = scrollRef.current;
    if (!el) return;
    const dist = el.scrollHeight - el.scrollTop - el.clientHeight;
    atBottomRef.current = dist < 120;
    setShowScrollBtn(dist > 240);
  };

  const scrollToBottom = () => {
    atBottomRef.current = true;
    bottomRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  };

  const hasMessages = messages.length > 0;

  return (
    <div className="relative flex h-full flex-col overflow-hidden bg-gradient-to-b from-slate-50 to-slate-100 text-slate-900 dark:from-slate-950 dark:to-slate-900 dark:text-slate-100">
      {/* Decorative brand glow */}
      <div
        aria-hidden
        className="pointer-events-none absolute -top-32 left-1/2 h-72 w-[42rem] -translate-x-1/2 rounded-full bg-brand-500/15 blur-3xl dark:bg-brand-500/10"
      />
      <div
        aria-hidden
        className="pointer-events-none absolute bottom-24 right-0 h-64 w-64 rounded-full bg-accent-500/10 blur-3xl"
      />

      <Header
        meta={meta}
        theme={theme}
        onToggleTheme={toggle}
        onClear={clear}
        hasMessages={hasMessages}
      />

      <main
        ref={scrollRef}
        onScroll={onScroll}
        className="relative flex-1 overflow-y-auto"
      >
        {!hasMessages ? (
          <Welcome meta={meta} onPick={send} />
        ) : (
          <div className="mx-auto flex max-w-4xl flex-col gap-6 px-4 py-6">
            {messages.map((m, i) => (
              <Message
                key={m.id}
                message={m}
                isStreaming={isStreaming}
                isLast={i === messages.length - 1}
                onRegenerate={() => regenerate(m.id)}
                onFeedback={(rating, extra) => sendFeedback(m.id, rating, extra)}
                onFollowUp={send}
              />
            ))}
            <div ref={bottomRef} className="h-1" />
          </div>
        )}

        {showScrollBtn && (
          <button
            onClick={scrollToBottom}
            title="Scroll to latest"
            className="animate-fade-in-up fixed bottom-28 left-1/2 z-10 grid h-10 w-10 -translate-x-1/2 place-items-center rounded-full border border-slate-200 bg-white text-slate-600 shadow-lg transition hover:text-brand-600 dark:border-white/10 dark:bg-slate-800 dark:text-slate-300"
          >
            <ArrowDownIcon width={18} height={18} />
          </button>
        )}
      </main>

      <Composer
        onSend={send}
        onStop={stop}
        isStreaming={isStreaming}
        disabled={connecting && !meta}
      />
    </div>
  );
}
