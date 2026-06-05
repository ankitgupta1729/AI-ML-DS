import type { ChatMessage, Rating } from "../types";
import FollowUps from "./FollowUps";
import Logo from "./Logo";
import MarkdownMessage from "./MarkdownMessage";
import MessageActions from "./MessageActions";
import SourceList from "./SourceList";
import { DocIcon } from "./icons";

interface Props {
  message: ChatMessage;
  isStreaming: boolean;
  isLast: boolean;
  onRegenerate: () => void;
  onBookmark: () => void;
  onFeedback: (
    rating: Rating,
    extra?: { reason?: string; comment?: string; correctedAnswer?: string },
  ) => void;
  onFollowUp: (prompt: string) => void;
}

export default function Message({
  message,
  isStreaming,
  isLast,
  onRegenerate,
  onBookmark,
  onFeedback,
  onFollowUp,
}: Props) {
  const isUser = message.role === "user";

  if (isUser) {
    return (
      <div className="animate-fade-in-up flex flex-col items-end gap-1.5">
        {message.attachments && message.attachments.length > 0 && (
          <div className="flex max-w-[85%] flex-wrap justify-end gap-2">
            {message.attachments.map((a, i) =>
              a.isImage ? (
                <img
                  key={i}
                  src={a.data}
                  alt={a.name}
                  className="h-28 w-28 rounded-xl border border-white/20 object-cover shadow-md"
                />
              ) : (
                <div
                  key={i}
                  className="flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-3 py-2 text-xs text-slate-700 shadow-sm dark:border-white/10 dark:bg-slate-900 dark:text-slate-200"
                >
                  <DocIcon width={16} height={16} />
                  <span className="max-w-[160px] truncate">{a.name}</span>
                </div>
              ),
            )}
          </div>
        )}
        {message.content && (
          <div className="max-w-[85%] rounded-2xl rounded-br-md bg-gradient-to-br from-brand-500 to-brand-600 px-4 py-2.5 text-[15px] text-white shadow-md shadow-brand-500/20">
            <p className="whitespace-pre-wrap break-words">{message.content}</p>
          </div>
        )}
      </div>
    );
  }

  const done = !message.streaming && !!message.content && !message.error;

  return (
    <div className="animate-fade-in-up flex gap-3">
      <div className="mt-0.5 shrink-0">
        <Logo size={34} />
      </div>
      <div className="min-w-0 flex-1">
        <div
          className={`rounded-2xl rounded-tl-md border px-4 py-3 ${
            message.error
              ? "border-red-300 bg-red-50 dark:border-red-500/30 dark:bg-red-500/10"
              : "border-slate-200 bg-white dark:border-white/10 dark:bg-slate-900/60"
          }`}
        >
          {message.content ? (
            <span className={message.streaming ? "streaming-cursor" : ""}>
              <MarkdownMessage content={message.content} />
            </span>
          ) : (
            <TypingDots />
          )}
        </div>

        {done && typeof message.confidence === "number" && message.confidence > 0 && (
          <div className="mt-1.5 flex items-center gap-2">
            <span className="text-[11px] text-slate-400">Grounding</span>
            <span className="h-1.5 w-24 overflow-hidden rounded-full bg-slate-200 dark:bg-white/10">
              <span
                className="block h-full rounded-full bg-gradient-to-r from-brand-500 to-accent-500"
                style={{ width: `${Math.round(message.confidence * 100)}%` }}
              />
            </span>
            <span className="text-[11px] font-medium text-slate-500 dark:text-slate-400">
              {Math.round(message.confidence * 100)}%
            </span>
          </div>
        )}

        {message.inScope === false && done && (
          <p className="mt-1.5 text-xs text-amber-600 dark:text-amber-400">
            ⓘ Answered from general knowledge — no closely matching study
            material was found in the index.
          </p>
        )}

        {done && message.pyqLinks && message.pyqLinks.length > 0 && (
          <div className="mt-3 rounded-xl border border-brand-500/30 bg-brand-500/5 p-3">
            <div className="mb-1.5 flex items-center gap-1.5 text-xs font-bold text-brand-600 dark:text-brand-400">
              📌 See this previous-year question on GateOverflow
            </div>
            <div className="flex flex-wrap gap-2">
              {message.pyqLinks.map((l, i) => (
                <a
                  key={i}
                  href={l.url}
                  target="_blank"
                  rel="noreferrer noopener"
                  className="inline-flex items-center gap-1 rounded-full border border-brand-400/50 bg-white px-3 py-1 text-xs font-medium text-brand-700 transition hover:bg-brand-500 hover:text-white dark:bg-slate-900/60 dark:text-brand-300"
                  title={l.url}
                >
                  {l.label} ↗
                </a>
              ))}
            </div>
            <p className="mt-1.5 text-[11px] text-slate-400">
              Official discussion &amp; community answers on gateoverflow.in
            </p>
          </div>
        )}

        {message.sources && <SourceList sources={message.sources} />}

        {done && (
          <>
            <MessageActions
              message={message}
              isStreaming={isStreaming}
              onRegenerate={onRegenerate}
              onBookmark={onBookmark}
              onFeedback={onFeedback}
            />
            {isLast && (
              <FollowUps onPick={onFollowUp} disabled={isStreaming} />
            )}
          </>
        )}
      </div>
    </div>
  );
}

function TypingDots() {
  return (
    <div className="flex items-center gap-1 py-1">
      {[0, 150, 300].map((d) => (
        <span
          key={d}
          className="h-2 w-2 animate-bounce rounded-full bg-brand-400"
          style={{ animationDelay: `${d}ms` }}
        />
      ))}
    </div>
  );
}
