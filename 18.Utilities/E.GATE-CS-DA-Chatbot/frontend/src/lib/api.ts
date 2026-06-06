import type {
  Analytics,
  Attachment,
  DailyQuestion,
  DonePayload,
  Meta,
  QuizQuestion,
  QuizResult,
  ReviewCard,
  Role,
  SendOpts,
  Source,
  StudyPlan,
} from "../types";

// In dev the Vite proxy maps /api/* → backend. In production set VITE_API_BASE
// to the API origin (e.g. https://api.example.com) at build time.
// `??` (not `||`) so an explicit empty string ("" = same-origin, used by the
// single-container production build) is respected; unset → dev proxy "/api".
const API_BASE = (import.meta.env.VITE_API_BASE as string | undefined) ?? "/api";

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
              confidence: typeof p.confidence === "number" ? p.confidence : 0,
              pyqLinks: (p.pyq_links as { url: string; label: string }[]) || [],
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
  opts: SendOpts = {},
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
        tutor_mode: Boolean(opts.tutorMode),
        language: opts.language ?? null,
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

// --- Study suite -------------------------------------------------------- //
async function postJSON<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`${path} ${res.status}`);
  return res.json();
}

async function getJSON<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`);
  if (!res.ok) throw new Error(`${path} ${res.status}`);
  return res.json();
}

export const generateQuiz = (body: {
  exam: string; subject: string; num: number; difficulty: string; kind: string;
}) => postJSON<{ ok: boolean; quiz_id: string; questions: QuizQuestion[]; error?: string }>(
  "/quiz/generate", body,
);

export const submitQuiz = (quiz_id: string, answers: Record<string, unknown>, duration_sec: number) =>
  postJSON<QuizResult>("/quiz/submit", { quiz_id, answers, duration_sec });

export const generateFlashcards = (body: { exam: string; topic: string; num: number }) =>
  postJSON<{ ok: boolean; cards: ReviewCard[]; error?: string }>("/flashcards/generate", body);

export const dueReviews = () => getJSON<{ ok: boolean; items: ReviewCard[] }>("/review/due");

export const gradeReview = (item_id: string, quality: number) =>
  postJSON<{ ok: boolean }>("/review/grade", { item_id, quality });

export const generatePlan = (body: {
  exam: string; exam_date: string | null; days: number; hours: number;
}) => postJSON<{ ok: boolean } & StudyPlan>("/plan/generate", body);

export const getPlan = () => getJSON<{ ok: boolean; plan: StudyPlan | null }>("/plan");

export const getDaily = () => getJSON<DailyQuestion>("/daily");

export const generateCheatsheet = (history: HistoryTurn[]) =>
  postJSON<{ ok: boolean; markdown?: string; error?: string }>("/cheatsheet", {
    history,
  });

export const getAnalytics = () => getJSON<Analytics>("/analytics");

export const planCalendarUrl = `${API_BASE}/plan/calendar.ics`;

// --- History & bookmarks ------------------------------------------------ //
export interface ConversationSummary {
  id: string;
  title: string;
  messages: number;
  updated_at: string;
}
export interface BookmarkItem {
  message_id: string;
  conversation_id: string;
  content: string;
  note: string | null;
  created_at: string;
}
export interface StoredMessage {
  id: string;
  role: Role;
  content: string;
  sources: Source[];
  in_scope: boolean | null;
  bookmarked: boolean;
}

export const listConversations = () =>
  getJSON<{ ok: boolean; conversations: ConversationSummary[] }>("/conversations");

export const getConversation = (id: string) =>
  getJSON<{ ok: boolean; conversation_id: string; messages: StoredMessage[] }>(
    `/conversations/${id}`,
  );

export const toggleBookmark = (messageId: string) =>
  postJSON<{ ok: boolean; bookmarked: boolean }>("/bookmark", {
    message_id: messageId,
  });

export const listBookmarks = () =>
  getJSON<{ ok: boolean; bookmarks: BookmarkItem[] }>("/bookmarks");

/** Regenerate a previous assistant answer (steered by any prior feedback). */
export async function streamRegenerate(
  messageId: string,
  guidance: string | null,
  cb: StreamCallbacks,
  opts: SendOpts = {},
): Promise<void> {
  let res: Response;
  try {
    res = await fetch(`${API_BASE}/regenerate/stream`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message_id: messageId,
        guidance,
        tutor_mode: Boolean(opts.tutorMode),
        language: opts.language ?? null,
      }),
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
