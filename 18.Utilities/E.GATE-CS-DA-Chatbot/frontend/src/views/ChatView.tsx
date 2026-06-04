import { useEffect, useRef, useState } from "react";
import Composer from "../components/Composer";
import Message from "../components/Message";
import Welcome from "../components/Welcome";
import { ArrowDownIcon, BulbIcon, GlobeIcon } from "../components/icons";
import type { Attachment, ChatMessage, Meta, Rating } from "../types";

const LANGUAGES = ["English", "Hindi", "Bengali", "Telugu", "Tamil", "Marathi", "Kannada"];

interface Props {
  meta: Meta | null;
  connecting: boolean;
  messages: ChatMessage[];
  isStreaming: boolean;
  send: (text: string, attachments?: Attachment[], opts?: { tutorMode?: boolean; language?: string | null }) => void;
  stop: () => void;
  regenerate: (id: string, opts?: { tutorMode?: boolean; language?: string | null }) => void;
  sendFeedback: (id: string, rating: Rating, extra?: { reason?: string; comment?: string; correctedAnswer?: string }) => void;
}

export default function ChatView({
  meta,
  connecting,
  messages,
  isStreaming,
  send,
  stop,
  regenerate,
  sendFeedback,
}: Props) {
  const [tutorMode, setTutorMode] = useState(false);
  const [language, setLanguage] = useState("English");

  const scrollRef = useRef<HTMLDivElement>(null);
  const bottomRef = useRef<HTMLDivElement>(null);
  const atBottomRef = useRef(true);
  const [showScrollBtn, setShowScrollBtn] = useState(false);

  const opts = { tutorMode, language };
  const doSend = (text: string, attachments: Attachment[] = []) =>
    send(text, attachments, opts);

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
    <div className="relative flex h-full flex-col">
      {/* Control strip */}
      <div className="flex items-center gap-2 border-b border-slate-200/70 px-4 py-2 dark:border-white/10">
        <button
          onClick={() => setTutorMode((v) => !v)}
          title="Socratic tutor mode — hints before answers"
          className={`inline-flex items-center gap-1.5 rounded-full border px-3 py-1 text-xs font-medium transition ${
            tutorMode
              ? "border-brand-500 bg-brand-500/10 text-brand-600 dark:text-brand-300"
              : "border-slate-200 text-slate-500 hover:border-brand-400 dark:border-white/10 dark:text-slate-400"
          }`}
        >
          <BulbIcon width={14} height={14} /> Socratic {tutorMode ? "on" : "off"}
        </button>

        <label className="inline-flex items-center gap-1.5 rounded-full border border-slate-200 px-2.5 py-1 text-xs text-slate-500 dark:border-white/10 dark:text-slate-400">
          <GlobeIcon width={14} height={14} />
          <select
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            className="bg-transparent outline-none"
            title="Answer language"
          >
            {LANGUAGES.map((l) => (
              <option key={l} value={l} className="text-slate-900">
                {l}
              </option>
            ))}
          </select>
        </label>
      </div>

      <div ref={scrollRef} onScroll={onScroll} className="relative flex-1 overflow-y-auto">
        {!hasMessages ? (
          <Welcome meta={meta} onPick={doSend} />
        ) : (
          <div className="mx-auto flex max-w-4xl flex-col gap-6 px-4 py-6">
            {messages.map((m, i) => (
              <Message
                key={m.id}
                message={m}
                isStreaming={isStreaming}
                isLast={i === messages.length - 1}
                onRegenerate={() => regenerate(m.id, opts)}
                onFeedback={(rating, extra) => sendFeedback(m.id, rating, extra)}
                onFollowUp={doSend}
              />
            ))}
            <div ref={bottomRef} className="h-1" />
          </div>
        )}

        {showScrollBtn && (
          <button
            onClick={scrollToBottom}
            title="Scroll to latest"
            className="animate-fade-in-up sticky bottom-4 left-1/2 z-10 grid h-10 w-10 -translate-x-1/2 place-items-center rounded-full border border-slate-200 bg-white text-slate-600 shadow-lg transition hover:text-brand-600 dark:border-white/10 dark:bg-slate-800 dark:text-slate-300"
          >
            <ArrowDownIcon width={18} height={18} />
          </button>
        )}
      </div>

      <Composer
        onSend={doSend}
        onStop={stop}
        isStreaming={isStreaming}
        disabled={connecting && !meta}
      />
    </div>
  );
}
