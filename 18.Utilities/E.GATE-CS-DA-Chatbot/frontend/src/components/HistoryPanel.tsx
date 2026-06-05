import { useEffect, useState } from "react";
import {
  listBookmarks,
  listConversations,
  type BookmarkItem,
  type ConversationSummary,
} from "../lib/api";
import { ClockIcon, StarIcon, XIcon } from "./icons";

function timeAgo(iso: string): string {
  const d = (Date.now() - new Date(iso).getTime()) / 1000;
  if (d < 60) return "just now";
  if (d < 3600) return `${Math.floor(d / 60)}m ago`;
  if (d < 86400) return `${Math.floor(d / 3600)}h ago`;
  return `${Math.floor(d / 86400)}d ago`;
}

export default function HistoryPanel({
  onClose,
  onOpen,
}: {
  onClose: () => void;
  onOpen: (conversationId: string) => void;
}) {
  const [tab, setTab] = useState<"history" | "saved">("history");
  const [convs, setConvs] = useState<ConversationSummary[]>([]);
  const [marks, setMarks] = useState<BookmarkItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([listConversations(), listBookmarks()])
      .then(([c, b]) => {
        if (c.ok) setConvs(c.conversations);
        if (b.ok) setMarks(b.bookmarks);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const open = (id: string) => {
    onOpen(id);
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex justify-end bg-black/40 backdrop-blur-sm" onClick={onClose}>
      <div
        onClick={(e) => e.stopPropagation()}
        className="animate-fade-in-up flex h-full w-full max-w-md flex-col border-l border-slate-200 bg-white shadow-2xl dark:border-white/10 dark:bg-slate-900"
      >
        <div className="flex items-center justify-between border-b border-slate-200 px-4 py-3 dark:border-white/10">
          <h2 className="text-base font-bold">Your activity</h2>
          <button onClick={onClose} className="grid h-8 w-8 place-items-center rounded-lg text-slate-500 hover:bg-slate-100 dark:hover:bg-white/10">
            <XIcon width={18} height={18} />
          </button>
        </div>

        <div className="flex gap-1 px-3 pt-3">
          <Tab active={tab === "history"} onClick={() => setTab("history")}>
            <ClockIcon width={15} height={15} /> History
          </Tab>
          <Tab active={tab === "saved"} onClick={() => setTab("saved")}>
            <StarIcon width={15} height={15} /> Saved ({marks.length})
          </Tab>
        </div>

        <div className="flex-1 overflow-y-auto p-3">
          {loading ? (
            <p className="py-10 text-center text-sm text-slate-400">Loading…</p>
          ) : tab === "history" ? (
            convs.length === 0 ? (
              <Empty text="No past conversations yet. Your chats will appear here." />
            ) : (
              <ul className="space-y-2">
                {convs.map((c) => (
                  <li key={c.id}>
                    <button
                      onClick={() => open(c.id)}
                      className="w-full rounded-xl border border-slate-200 bg-white p-3 text-left transition hover:border-brand-400 hover:shadow-sm dark:border-white/10 dark:bg-slate-900/60"
                    >
                      <div className="truncate text-sm font-medium text-slate-800 dark:text-slate-100">
                        {c.title}
                      </div>
                      <div className="mt-0.5 text-xs text-slate-400">
                        {Math.floor(c.messages / 2) || 1} exchange(s) · {timeAgo(c.updated_at)}
                      </div>
                    </button>
                  </li>
                ))}
              </ul>
            )
          ) : marks.length === 0 ? (
            <Empty text="No saved answers yet. Tap the ★ on any answer to save it." />
          ) : (
            <ul className="space-y-2">
              {marks.map((b) => (
                <li key={b.message_id}>
                  <button
                    onClick={() => open(b.conversation_id)}
                    className="w-full rounded-xl border border-slate-200 bg-white p-3 text-left transition hover:border-amber-400 hover:shadow-sm dark:border-white/10 dark:bg-slate-900/60"
                  >
                    <div className="flex items-start gap-2">
                      <StarIcon width={14} height={14} fill="currentColor" className="mt-0.5 shrink-0 text-amber-500" />
                      <span className="line-clamp-3 text-sm text-slate-700 dark:text-slate-200">
                        {b.content.slice(0, 220)}
                        {b.content.length > 220 ? "…" : ""}
                      </span>
                    </div>
                    <div className="mt-1 pl-6 text-xs text-slate-400">{timeAgo(b.created_at)}</div>
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}

function Tab({ active, onClick, children }: { active: boolean; onClick: () => void; children: React.ReactNode }) {
  return (
    <button
      onClick={onClick}
      className={`inline-flex flex-1 items-center justify-center gap-1.5 rounded-lg px-3 py-2 text-sm font-medium transition ${
        active
          ? "bg-brand-500/10 text-brand-600 dark:text-brand-300"
          : "text-slate-500 hover:bg-slate-100 dark:text-slate-400 dark:hover:bg-white/10"
      }`}
    >
      {children}
    </button>
  );
}

function Empty({ text }: { text: string }) {
  return <p className="px-4 py-12 text-center text-sm text-slate-400">{text}</p>;
}
