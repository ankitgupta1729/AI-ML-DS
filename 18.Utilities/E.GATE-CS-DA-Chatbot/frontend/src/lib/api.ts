import type { Attachment, DonePayload, Meta, Role, Source } from "../types";

// In dev the Vite proxy maps /api/* → backend. In production set VITE_API_BASE
// to the API origin (e.g. https://api.example.com) at build time.
const API_BASE = (import.meta.env.VITE_API_BASE as string | undefined) || "/api";

export interface HistoryTurn {
  role: Role;
  content: string;
}

export async function fetchMeta(): Promise<Meta> {
  const res = await fetch(`${API_BASE}/meta`);
  if (!res.ok) throw new Error(`meta ${res.status}`);
  return res.json();
}

interface StreamCallbacks {
  onToken: (token: string) => void;
  onDone: (payload: DonePayload) => void;
  onError: (message: string) => void;
  signal?: AbortSignal;
}

async function consumeSSE(res: Response, cb: StreamCallbacks): Promise<void> {
  if (!res.ok || !res.body) {
    cb.onError(`Server returned ${res.status}. Please try again.`);
    return;
  }
  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  try {
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });

      let sep: number;
      while ((sep = buffer.indexOf("\n\n")) !== -1) {
        const frame = buffer.slice(0, sep);
        buffer = buffer.slice(sep + 2);
        const line = frame.split("\n").find((l) => l.startsWith("data:"));
        if (!line) continue;
        const json = line.slice(5).trim();
        if (!json) continue;
        try {
          const p = JSON.parse(json);
          if (p.type === "token") {
            cb.onToken(p.content as string);
          } else if (p.type === "done") {
            cb.onDone({
              sources: (p.sources as Source[]) || [],
              inScope: Boolean(p.in_scope),
              conversationId: (p.conversation_id as string) ?? null,
              messageId: (p.message_id as string) ?? null,
            });
          }
        } catch {
          /* ignore malformed frame */
        }
      }
    }
  } catch (e) {
    if ((e as Error).name === "AbortError") return;
    cb.onError("The connection was interrupted.");
  }
}

/** Stream an answer from POST /chat/stream. */
export async function streamChat(
  question: string,
  history: HistoryTurn[],
  conversationId: string | null,
  attachments: Attachment[],
  cb: StreamCallbacks,
): Promise<void> {
  let res: Response;
  try {
    res = await fetch(`${API_BASE}/chat/stream`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question,
        history,
        conversation_id: conversationId,
        attachments: attachments.map((a) => ({
          name: a.name,
          mime: a.mime,
          data: a.data,
        })),
      }),
      signal: cb.signal,
    });
  } catch {
    cb.onError("Couldn't reach the server. Is the API running on port 8000?");
    return;
  }
  await consumeSSE(res, cb);
}

/** Regenerate a previous assistant answer (steered by any prior feedback). */
export async function streamRegenerate(
  messageId: string,
  guidance: string | null,
  cb: StreamCallbacks,
): Promise<void> {
  let res: Response;
  try {
    res = await fetch(`${API_BASE}/regenerate/stream`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message_id: messageId, guidance }),
      signal: cb.signal,
    });
  } catch {
    cb.onError("Couldn't reach the server to regenerate.");
    return;
  }
  await consumeSSE(res, cb);
}

export interface FeedbackInput {
  messageId: string;
  rating: "up" | "down";
  reason?: string;
  comment?: string;
  correctedAnswer?: string;
}

export async function submitFeedback(fb: FeedbackInput): Promise<boolean> {
  try {
    const res = await fetch(`${API_BASE}/feedback`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message_id: fb.messageId,
        rating: fb.rating,
        reason: fb.reason ?? null,
        comment: fb.comment ?? null,
        corrected_answer: fb.correctedAnswer ?? null,
      }),
    });
    if (!res.ok) return false;
    const data = await res.json();
    return Boolean(data.ok);
  } catch {
    return false;
  }
}
