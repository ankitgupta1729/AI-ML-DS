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

        {message.inScope === false && done && (
          <p className="mt-1.5 text-xs text-amber-600 dark:text-amber-400">
            ⓘ Answered from general knowledge — no closely matching study
            material was found in the index.
          </p>
        )}

        {message.sources && <SourceList sources={message.sources} />}

        {done && (
          <>
            <MessageActions
              message={message}
              isStreaming={isStreaming}
              onRegenerate={onRegenerate}
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
