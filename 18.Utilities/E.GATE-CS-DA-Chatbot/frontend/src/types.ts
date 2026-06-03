export type Role = "user" | "assistant";

export type Rating = "up" | "down" | null;

export interface Attachment {
  name: string;
  mime: string;
  data: string; // data URL (base64)
  isImage: boolean;
}

export interface Source {
  source: string;
  subject: string;
  score: number;
  locator: string;
  snippet: string;
}

export interface ChatMessage {
  id: string; // client-side id
  role: Role;
  content: string;
  sources?: Source[];
  inScope?: boolean;
  streaming?: boolean;
  error?: boolean;
  // Server-side id (assigned when the turn is persisted); needed for feedback.
  messageId?: string | null;
  rating?: Rating;
  feedbackSent?: boolean;
  attachments?: Attachment[];
}

export interface Meta {
  app_name: string;
  assistant_name: string;
  tagline: string;
  scope: string;
  model: string;
  indexed_chunks: number;
  key_configured: boolean;
}

export interface DonePayload {
  sources: Source[];
  inScope: boolean;
  conversationId: string | null;
  messageId: string | null;
}
