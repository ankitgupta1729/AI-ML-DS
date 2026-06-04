import { useState } from "react";
import { speak, stopSpeaking } from "../hooks/useSpeech";
import type { ChatMessage, Rating } from "../types";
import FeedbackForm from "./FeedbackForm";
import {
  CheckIcon,
  CopyIcon,
  RegenerateIcon,
  SpeakerIcon,
  ThumbsDownIcon,
  ThumbsUpIcon,
} from "./icons";

interface Props {
  message: ChatMessage;
  isStreaming: boolean;
  onRegenerate: () => void;
  onFeedback: (
    rating: Rating,
    extra?: { reason?: string; comment?: string; correctedAnswer?: string },
  ) => void;
}

export default function MessageActions({
  message,
  isStreaming,
  onRegenerate,
  onFeedback,
}: Props) {
  const [copied, setCopied] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [speaking, setSpeaking] = useState(false);

  const toggleSpeak = () => {
    if (speaking) {
      stopSpeaking();
      setSpeaking(false);
    } else {
      speak(message.content);
      setSpeaking(true);
    }
  };

  const copy = async () => {
    try {
      await navigator.clipboard.writeText(message.content);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch {
      /* clipboard not available */
    }
  };

  const like = () => onFeedback("up");
  const dislike = () => {
    if (message.rating === "down") {
      onFeedback("down"); // toggle off
      setShowForm(false);
    } else {
      onFeedback("down");
      setShowForm(true);
    }
  };

  const btn =
    "grid h-8 w-8 place-items-center rounded-lg text-slate-400 transition hover:bg-slate-100 hover:text-slate-700 disabled:opacity-40 dark:hover:bg-white/10 dark:hover:text-white";
  const active = "bg-brand-500/15 text-brand-600 dark:text-brand-300";

  return (
    <div className="mt-1.5">
      <div className="flex items-center gap-0.5">
        <button onClick={copy} title="Copy" className={btn}>
          {copied ? (
            <CheckIcon width={15} height={15} className="text-emerald-500" />
          ) : (
            <CopyIcon width={15} height={15} />
          )}
        </button>
        <button
          onClick={like}
          title="Good answer"
          className={`${btn} ${message.rating === "up" ? active : ""}`}
        >
          <ThumbsUpIcon width={15} height={15} />
        </button>
        <button
          onClick={dislike}
          title="Bad answer"
          className={`${btn} ${message.rating === "down" ? active : ""}`}
        >
          <ThumbsDownIcon width={15} height={15} />
        </button>
        <button
          onClick={onRegenerate}
          disabled={isStreaming}
          title="Regenerate"
          className={btn}
        >
          <RegenerateIcon width={15} height={15} />
        </button>
        <button
          onClick={toggleSpeak}
          title={speaking ? "Stop" : "Read aloud"}
          className={`${btn} ${speaking ? active : ""}`}
        >
          <SpeakerIcon width={15} height={15} />
        </button>
        {message.feedbackSent && message.rating === "up" && (
          <span className="ml-1 text-xs text-emerald-500">Thanks! 🎉</span>
        )}
      </div>

      {showForm && message.rating === "down" && (
        <FeedbackForm
          onCancel={() => setShowForm(false)}
          onSubmit={(data) => {
            onFeedback("down", data);
            setShowForm(false);
          }}
        />
      )}
    </div>
  );
}
