import { XIcon } from "./icons";

interface Entry {
  icon: string;
  title: string;
  why: string; // purpose + benefit + how it differs
  how: string[]; // step-by-step usage
  tip?: string;
}

const SECTIONS: { group: string; items: Entry[] }[] = [
  {
    group: "Chat & answers",
    items: [
      {
        icon: "💬",
        title: "Ask anything (grounded answers)",
        why: "Answers are retrieved from real PYQs and your own material, not generic web text — so they're exam-aligned and trustworthy. Unlike ChatGPT/Claude, every answer can cite its source.",
        how: [
          "Type a question and press Enter (Shift+Enter for a new line).",
          "Watch the answer stream in with formatted maths and code.",
          "Expand “Sources” to see the file, page and match score.",
        ],
        tip: "Be specific: “Explain conflict serializability with a precedence-graph example.”",
      },
      {
        icon: "📈",
        title: "Grounding-confidence meter",
        why: "The bar under each answer shows how strongly it’s backed by your indexed material — a transparency feature general chatbots don’t offer.",
        how: ["Higher % = well-grounded in sources.", "Low % shows an “answered from general knowledge” note — verify those."],
      },
      {
        icon: "🔁",
        title: "Follow-up chips & actions",
        why: "Keep a topic going in one click, and act on any answer (copy, like, dislike, regenerate, read-aloud).",
        how: [
          "Click a follow-up chip under the latest answer.",
          "Use 👍/👎 to rate; 👎 opens a quick feedback form.",
          "↻ regenerates; 🔊 reads the answer aloud.",
        ],
      },
    ],
  },
  {
    group: "Practice & revision",
    items: [
      {
        icon: "📝",
        title: "Mock Test & Practice",
        why: "Exam-style MCQ/MSQ/NAT, scored on the server with real GATE negative marking and an estimated percentile — something no general chatbot does.",
        how: [
          "Open Mock Test → pick exam, subject, difficulty and count.",
          "Answer the questions (a timer runs); click Submit.",
          "Review your score, percentile, explanations and weak areas.",
        ],
        tip: "Wrong answers automatically become flashcards for revision.",
      },
      {
        icon: "🃏",
        title: "Flashcards & Spaced Repetition",
        why: "Uses the proven SM-2 algorithm to schedule reviews at the optimal moment, so you actually remember concepts for the exam.",
        how: [
          "Open Flashcards → review cards that are due.",
          "Flip the card, then grade yourself: Again / Hard / Good / Easy.",
          "Generate a new deck on any topic from the box at the top.",
        ],
        tip: "The sidebar badge shows how many cards are due.",
      },
      {
        icon: "🔥",
        title: "Daily question & streaks",
        why: "One fresh question a day builds a consistent habit — and habit is what cracks GATE.",
        how: ["Open Daily → read the question, reveal the hint if needed.", "Click “Solve with GO Buddy” to work through it in chat."],
      },
    ],
  },
  {
    group: "Plan & track",
    items: [
      {
        icon: "🗓️",
        title: "Study Planner",
        why: "Generates a day-by-day plan to your exam date, prioritising high-weight subjects — and exports to your calendar.",
        how: [
          "Open Planner → set exam, date (or number of days) and hours/day.",
          "Click Build plan to get a daily schedule.",
          "Use “Export to calendar (.ics)” to add it to your calendar app.",
        ],
      },
      {
        icon: "📊",
        title: "Performance Dashboard",
        why: "Turns your attempts into insight: an exam-readiness score, accuracy by subject, weak-area detection and streaks.",
        how: ["Open Dashboard after a few quizzes.", "Read the readiness ring and subject bars.", "Focus on the highlighted weak areas next."],
      },
    ],
  },
  {
    group: "Input & accessibility",
    items: [
      {
        icon: "📎",
        title: "Attachments (image / PDF)",
        why: "Stuck on a question in a screenshot or PDF? Attach it — the vision model reads images and text is extracted from documents.",
        how: ["Click 📎 in the composer (or paste an image).", "Add up to 4 files (≤ 8 MB each).", "Ask your question about the attachment."],
      },
      {
        icon: "✏️",
        title: "Sketch a question",
        why: "Draw a diagram or your working when typing is awkward; it’s sent as an image the model can read.",
        how: ["Click the ✏️ pen icon in the composer.", "Draw on the canvas, pick a colour, then “Attach sketch”."],
      },
      {
        icon: "🎙️",
        title: "Voice in & out",
        why: "Ask by speaking and listen to answers — great for revising on the go.",
        how: ["Click the 🎙️ mic and speak your question.", "Click 🔊 on any answer to have it read aloud."],
        tip: "Works in Chrome, Edge and Safari.",
      },
      {
        icon: "🌐",
        title: "Multilingual & 💡 Socratic mode",
        why: "Get explanations in Hindi and other languages, or switch on Socratic mode to get hints before the full solution — building real understanding.",
        how: ["Pick a language from the dropdown above the chat.", "Toggle “Socratic” on for hints-first tutoring."],
      },
    ],
  },
  {
    group: "It learns from you",
    items: [
      {
        icon: "🛠️",
        title: "Feedback → RLHF",
        why: "Your 👎 + reason regenerates a better answer immediately, and your corrections build a dataset to improve the model over time. General chatbots forget your corrections.",
        how: ["Dislike a weak answer and pick a reason / add a correction.", "Click ↻ to regenerate, steered by your feedback."],
      },
    ],
  },
];

export default function GuideModal({ onClose }: { onClose: () => void }) {
  return (
    <div className="fixed inset-0 z-50 grid place-items-center bg-black/50 p-4 backdrop-blur-sm">
      <div className="flex max-h-[88vh] w-full max-w-3xl flex-col overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-2xl dark:border-white/10 dark:bg-slate-900">
        <div className="flex items-center justify-between border-b border-slate-200 px-5 py-3 dark:border-white/10">
          <div>
            <h2 className="text-lg font-extrabold">How to use GateOverflow Chatbot 🎯</h2>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              A quick guide to every feature — what it’s for and how to use it.
            </p>
          </div>
          <button onClick={onClose} className="grid h-9 w-9 place-items-center rounded-lg text-slate-500 hover:bg-slate-100 dark:hover:bg-white/10">
            <XIcon width={18} height={18} />
          </button>
        </div>

        <div className="overflow-y-auto px-5 py-4">
          {SECTIONS.map((sec) => (
            <div key={sec.group} className="mb-5">
              <div className="mb-2 text-xs font-bold uppercase tracking-wide text-brand-600 dark:text-brand-400">
                {sec.group}
              </div>
              <div className="space-y-3">
                {sec.items.map((e) => (
                  <div key={e.title} className="rounded-xl border border-slate-200 bg-slate-50/60 p-4 dark:border-white/10 dark:bg-white/[0.03]">
                    <div className="flex items-start gap-3">
                      <span className="text-2xl leading-none">{e.icon}</span>
                      <div className="min-w-0 flex-1">
                        <h3 className="font-bold text-slate-800 dark:text-white">{e.title}</h3>
                        <p className="mt-0.5 text-sm text-slate-600 dark:text-slate-300">{e.why}</p>
                        <div className="mt-2 text-xs font-semibold uppercase tracking-wide text-slate-400">How to use</div>
                        <ol className="mt-1 list-decimal space-y-0.5 pl-5 text-sm text-slate-600 dark:text-slate-300">
                          {e.how.map((h, i) => <li key={i}>{h}</li>)}
                        </ol>
                        {e.tip && (
                          <p className="mt-2 rounded-lg bg-brand-500/10 px-2.5 py-1.5 text-xs text-brand-700 dark:text-brand-300">
                            💡 {e.tip}
                          </p>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>

        <div className="flex items-center justify-between border-t border-slate-200 px-5 py-3 dark:border-white/10">
          <a href="https://gateoverflow.in" target="_blank" rel="noreferrer noopener"
             className="text-xs text-slate-400 hover:text-brand-500">
            Powered by GateOverflow ↗
          </a>
          <button onClick={onClose}
                  className="rounded-xl bg-gradient-to-br from-brand-500 to-accent-500 px-5 py-2 text-sm font-semibold text-white shadow-md transition hover:opacity-90">
            Got it — let’s study!
          </button>
        </div>
      </div>
    </div>
  );
}
