import { useEffect, useState } from "react";
import MarkdownMessage from "../components/MarkdownMessage";
import { dueReviews, generateFlashcards, gradeReview } from "../lib/api";
import type { ReviewCard } from "../types";

const GRADES = [
  { q: 1, label: "Again", cls: "border-red-300 text-red-600 dark:border-red-500/40 dark:text-red-400" },
  { q: 3, label: "Hard", cls: "border-amber-300 text-amber-600 dark:border-amber-500/40 dark:text-amber-400" },
  { q: 4, label: "Good", cls: "border-sky-300 text-sky-600 dark:border-sky-500/40 dark:text-sky-400" },
  { q: 5, label: "Easy", cls: "border-emerald-300 text-emerald-600 dark:border-emerald-500/40 dark:text-emerald-400" },
];

export default function Review() {
  const [cards, setCards] = useState<ReviewCard[]>([]);
  const [idx, setIdx] = useState(0);
  const [flipped, setFlipped] = useState(false);
  const [loading, setLoading] = useState(true);
  const [reviewed, setReviewed] = useState(0);

  const [topic, setTopic] = useState("");
  const [exam, setExam] = useState("CS");
  const [busy, setBusy] = useState(false);

  const load = async () => {
    setLoading(true);
    try {
      const r = await dueReviews();
      setCards(r.items || []);
      setIdx(0);
      setFlipped(false);
    } finally {
      setLoading(false);
    }
  };
  useEffect(() => { load(); }, []);

  const grade = async (q: number) => {
    const card = cards[idx];
    if (!card) return;
    if (card.id) await gradeReview(card.id, q);
    setReviewed((n) => n + 1);
    setFlipped(false);
    if (idx + 1 < cards.length) setIdx(idx + 1);
    else setCards([]);
  };

  const create = async () => {
    if (topic.trim().length < 2) return;
    setBusy(true);
    try {
      await generateFlashcards({ exam, topic: topic.trim(), num: 8 });
      setTopic("");
      await load();
    } finally {
      setBusy(false);
    }
  };

  const card = cards[idx];

  return (
    <div className="h-full overflow-y-auto">
      <div className="mx-auto max-w-2xl px-4 py-6">
        <h2 className="text-xl font-extrabold">🃏 Flashcards & Spaced Repetition</h2>
        <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
          Reviewed on an SM-2 schedule. Wrong quiz answers and generated cards land here.
        </p>

        {/* Generator */}
        <div className="mt-4 flex flex-wrap items-end gap-2 rounded-xl border border-slate-200 bg-white p-3 dark:border-white/10 dark:bg-slate-900">
          <select value={exam} onChange={(e) => setExam(e.target.value)}
                  className="rounded-lg border border-slate-300 bg-white px-2 py-1.5 text-sm dark:border-white/15 dark:bg-slate-800">
            <option value="CS">CS</option><option value="DA">DA</option>
          </select>
          <input value={topic} onChange={(e) => setTopic(e.target.value)}
                 placeholder="Generate cards on a topic (e.g. TCP, eigenvalues)…"
                 className="min-w-[200px] flex-1 rounded-lg border border-slate-300 bg-white px-3 py-1.5 text-sm outline-none focus:border-brand-500 dark:border-white/15 dark:bg-slate-800" />
          <button onClick={create} disabled={busy || topic.trim().length < 2}
                  className="rounded-lg bg-gradient-to-br from-brand-500 to-accent-500 px-4 py-1.5 text-sm font-semibold text-white transition hover:opacity-90 disabled:opacity-50">
            {busy ? "Generating…" : "Generate"}
          </button>
        </div>

        {/* Session */}
        <div className="mt-6">
          {loading ? (
            <p className="py-10 text-center text-slate-400">Loading your review deck…</p>
          ) : !card ? (
            <div className="rounded-2xl border border-dashed border-slate-300 p-10 text-center dark:border-white/15">
              <div className="text-4xl">🎉</div>
              <p className="mt-2 font-semibold">No cards due right now.</p>
              <p className="text-sm text-slate-500 dark:text-slate-400">
                {reviewed > 0 ? `You reviewed ${reviewed} card(s). ` : ""}
                Generate a set above, or take a quiz — missed questions become cards.
              </p>
            </div>
          ) : (
            <>
              <div className="mb-2 flex justify-between text-xs text-slate-400">
                <span>{card.subject}</span>
                <span>Card {idx + 1} of {cards.length}</span>
              </div>
              <button
                onClick={() => setFlipped((f) => !f)}
                className="grid min-h-[220px] w-full place-items-center rounded-2xl border border-slate-200 bg-white p-6 text-center shadow-sm transition hover:shadow-md dark:border-white/10 dark:bg-slate-900"
              >
                <div className="w-full">
                  <div className="mb-2 text-[11px] uppercase tracking-wide text-slate-400">
                    {flipped ? "Answer" : "Question — tap to flip"}
                  </div>
                  <div className="text-left text-[15px]">
                    <MarkdownMessage content={flipped ? card.back : card.front} />
                  </div>
                </div>
              </button>

              {flipped && (
                <div className="mt-4 grid grid-cols-4 gap-2">
                  {GRADES.map((g) => (
                    <button key={g.q} onClick={() => grade(g.q)}
                            className={`rounded-xl border bg-white py-2 text-sm font-semibold transition hover:-translate-y-0.5 dark:bg-slate-900 ${g.cls}`}>
                      {g.label}
                    </button>
                  ))}
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}
