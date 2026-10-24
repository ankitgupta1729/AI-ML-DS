export type Role = "user" | "assistant";

export type View = "chat" | "mock" | "review" | "planner" | "dashboard" | "daily";

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
  confidence?: number;
  pyqLinks?: PyqLink[];
  bookmarked?: boolean;
}

export interface PyqLink {
  url: string;
  label: string;
}

export interface SendOpts {
  tutorMode?: boolean;
  language?: string | null;
}

// --- Study suite -------------------------------------------------------- //
export type QType = "MCQ" | "MSQ" | "NAT";

export interface QuizQuestion {
  id: string;
  type: QType;
  question: string;
  options: string[];
  marks: number;
  subject: string;
}

export interface QuizResultItem {
  id: string;
  type: QType;
  question: string;
  options: string[];
  your_answer: unknown;
  correct_answer: unknown;
  is_correct: boolean;
  awarded: number;
  marks: number;
  explanation: string;
  subject: string;
}

export interface QuizResult {
  ok: boolean;
  attempt_id?: string;
  score: number;
  max_score: number;
  correct: number;
  answered: number;
  total: number;
  accuracy: number;
  percentile: number;
  subject_breakdown: Record<string, { correct: number; total: number; accuracy: number }>;
  results: QuizResultItem[];
  weak_areas: string[];
  review_cards_created: number;
}

export interface ReviewCard {
  id: string;
  front: string;
  back: string;
  subject: string;
  repetitions?: number;
}

export interface PlanDay {
  day: number;
  focus: string;
  tasks: string[];
  hours: number;
}

export interface StudyPlan {
  summary: string;
  days: PlanDay[];
  exam?: string;
  exam_date?: string | null;
}

export interface Analytics {
  ok: boolean;
  attempts: number;
  avg_accuracy: number;
  avg_percentile: number;
  streak: number;
  due_reviews: number;
  review_items: number;
  readiness: number;
  rank_band?: string;
  last7?: { attempts: number; avg_accuracy: number };
  percentile_trend?: { at: string; percentile: number; accuracy: number }[];
  by_subject: Record<string, { correct: number; total: number; accuracy: number }>;
  weak_areas: string[];
  recent: {
    kind: string; subject: string; score: number; max_score: number;
    accuracy: number; percentile: number; at: string;
  }[];
}

export interface PlanAdherence {
  days_since: number;
  active_days: number;
  expected: number;
  total_days: number;
  on_track: boolean;
  message: string;
}

export interface DailyQuestion {
  ok: boolean;
  date: string;
  topic: string;
  question: string;
  hint: string;
  streak: number;
}

export interface CoachReport {
  ok: boolean;
  reason?: string;
  message?: string;
  readiness?: number;
  headline?: string;
  strengths?: string[];
  focus_areas?: string[];
  this_week?: string[];
  rank_advice?: string;
  habit?: string;
  encouragement?: string;
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
  confidence: number;
  pyqLinks: PyqLink[];
}
