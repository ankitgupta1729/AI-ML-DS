import { useEffect, useRef, useState } from "react";
import MarkdownMessage from "../components/MarkdownMessage";
import { generateQuiz, submitQuiz } from "../lib/api";
import type { QuizQuestion, QuizResult } from "../types";

type Phase = "config" | "loading" | "taking" | "result";

const SUBJECTS: Record<string, string[]> = {
  CS: ["mixed topics", "Algorithms", "Data Structures", "Operating Systems", "DBMS",
       "Computer Networks", "Theory of Computation", "Compiler Design",
       "Computer Organisation", "Digital Logic", "Discrete Maths", "Aptitude"],
  DA: ["mixed topics", "Probability & Statistics", "Linear Algebra", "Calculus & Optimisation",
       "Machine Learning", "Deep Learning", "AI", "Data Structures", "Aptitude"],
};

function fmt(sec: number) {
  const m = Math.floor(sec / 60), s = sec % 60;
  return `${m}:${s.toString().padStart(2, "0")}`;
}

export default function MockTest() {
  const [phase, setPhase] = useState<Phase>("config");
  const [exam, setExam] = useState("CS");
  const [subject, setSubject] = useState("mixed topics");
  const [num, setNum] = useState(5);
  const [difficulty, setDifficulty] = useState("medium");
  const [kind, setKind] = useState("quiz");
  const [error, setError] = useState<string | null>(null);

  const [quizId, setQuizId] = useState("");
  const [questions, setQuestions] = useState<QuizQuestion[]>([]);
  const [answers, setAnswers] = useState<Record<string, unknown>>({});
  const [elapsed, setElapsed] = useState(0);
  const [result, setResult] = useState<QuizResult | null>(null);
  const timer = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => () => { if (timer.current) clearInterval(timer.current); }, []);

  const start = async () => {
    setPhase("loading");
    setError(null);
    try {
      const r = await generateQuiz({ exam, subject, num, difficulty, kind });
      if (!r.ok || !r.questions?.length) throw new Error(r.error || "generation failed");
      setQuizId(r.quiz_id);
      setQuestions(r.questions);
      setAnswers({});
      setElapsed(0);
      setPhase("taking");
      timer.current = setInterval(() => setElapsed((e) => e + 1), 1000);
    } catch {
      setError("Couldn't generate the test. Check the API/key and try again.");
      setPhase("config");
    }
  };

  const submit = async () => {
    if (timer.current) clearInterval(timer.current);
    try {
      const r = await submitQuiz(quizId, answers, elapsed);
      setResult(r);
      setPhase("result");
    } catch {
      setError("Submission failed. Try again.");
    }
  };

  const setAns = (qid: string, val: unknown) =>
    setAnswers((a) => ({ ...a, [qid]: val }));

  const toggleMsq = (qid: string, idx: number) =>
    setAnswers((a) => {
      const cur = new Set<number>(Array.isArray(a[qid]) ? (a[qid] as number[]) : []);
      cur.has(idx) ? cur.delete(idx) : cur.add(idx);
      return { ...a, [qid]: [...cur] };
    });

  // ---- Config ----
  if (phase === "config" || phase === "loading") {
    return (
      <Center>
        <div className="w-full max-w-lg rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-white/10 dark:bg-slate-900">
          <h2 className="text-xl font-extrabold">📝 Mock Test & Practice</h2>
          <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
            GATE-style MCQ / MSQ / NAT with negative marking, scoring and an
            estimated percentile. Wrong answers become flashcards automatically.
          </p>

          <div className="mt-5 grid grid-cols-2 gap-4">
            <Field label="Exam">
              <Select value={exam} onChange={(v) => { setExam(v); setSubject("mixed topics"); }}
                      options={["CS", "DA"]} />
            </Field>
            <Field label="Mode">
              <Select value={kind} onChange={setKind}
                      options={[["quiz", "Quick quiz"], ["mock", "Mock test (10+)"]]} />
            </Field>
            <Field label="Subject">
              <Select value={subject} onChange={setSubject} options={SUBJECTS[exam]} />
            </Field>
            <Field label="Difficulty">
              <Select value={difficulty} onChange={setDifficulty}
                      options={["easy", "medium", "hard"]} />
            </Field>
            <Field label={`Questions: ${num}`}>
              <input type="range" min={3} max={15} value={num}
                     onChange={(e) => setNum(Number(e.target.value))}
                     className="w-full accent-brand-500" />
            </Field>
          </div>

          {error && <p className="mt-3 text-sm text-red-500">{error}</p>}

          <button
            onClick={start}
            disabled={phase === "loading"}
            className="mt-5 w-full rounded-xl bg-gradient-to-br from-brand-500 to-accent-500 py-2.5 font-semibold text-white shadow-md transition hover:opacity-90 disabled:opacity-60"
          >
            {phase === "loading" ? "Generating questions…" : "Start"}
          </button>
        </div>
      </Center>
    );
  }

  // ---- Result ----
  if (phase === "result" && result) {
    const pct = Math.round(result.accuracy * 100);
    return (
      <Scroll>
        <div className="mx-auto max-w-3xl px-4 py-6">
          <div className="rounded-2xl border border-slate-200 bg-gradient-to-br from-brand-500/10 to-accent-500/5 p-6 text-center dark:border-white/10">
            <div className="text-sm uppercase tracking-wide text-slate-500">Your score</div>
            <div className="mt-1 text-4xl font-extrabold">
              {result.score} <span className="text-xl text-slate-400">/ {result.max_score}</span>
            </div>
            <div className="mt-2 flex flex-wrap justify-center gap-2 text-sm">
              <Stat label="Correct" value={`${result.correct}/${result.total}`} />
              <Stat label="Accuracy" value={`${pct}%`} />
              <Stat label="Est. percentile" value={`${result.percentile}`} />
              <Stat label="Time" value={fmt(elapsed)} />
            </div>
            {result.weak_areas.length > 0 && (
              <p className="mt-3 text-sm text-amber-600 dark:text-amber-400">
                Focus next on: {result.weak_areas.join(", ")}
              </p>
            )}
            {result.review_cards_created > 0 && (
              <p className="mt-1 text-xs text-slate-500">
                {result.review_cards_created} flashcard(s) added to your review deck.
              </p>
            )}
          </div>

          <div className="mt-6 space-y-4">
            {result.results.map((r, i) => (
              <div key={r.id}
                   className={`rounded-xl border p-4 ${r.is_correct
                     ? "border-emerald-300/60 bg-emerald-50/50 dark:border-emerald-500/30 dark:bg-emerald-500/5"
                     : "border-red-300/60 bg-red-50/50 dark:border-red-500/30 dark:bg-red-500/5"}`}>
                <div className="mb-2 flex items-center gap-2 text-sm font-semibold">
                  <span className={r.is_correct ? "text-emerald-600" : "text-red-600"}>
                    {r.is_correct ? "✓" : "✗"}
                  </span>
                  <span>Q{i + 1}</span>
                  <span className="rounded-full bg-slate-200 px-2 py-0.5 text-[10px] text-slate-600 dark:bg-white/10 dark:text-slate-300">
                    {r.type} · {r.marks}m · {r.subject}
                  </span>
                  <span className="ml-auto text-xs text-slate-400">{r.awarded > 0 ? "+" : ""}{r.awarded}</span>
                </div>
                <div className="text-sm"><MarkdownMessage content={r.question} /></div>
                {r.options.length > 0 && (
                  <ul className="mt-2 space-y-1 text-sm">
                    {r.options.map((o, idx) => {
                      const correct = Array.isArray(r.correct_answer)
                        ? (r.correct_answer as number[]).includes(idx)
                        : r.correct_answer === idx;
                      return (
                        <li key={idx} className={`rounded px-2 py-1 ${correct
                          ? "bg-emerald-500/15 font-medium text-emerald-700 dark:text-emerald-300" : ""}`}>
                          {String.fromCharCode(65 + idx)}. {o} {correct && "✓"}
                        </li>
                      );
                    })}
                  </ul>
                )}
                {r.type === "NAT" && (
                  <p className="mt-2 text-sm">Answer: <b>{String(r.correct_answer)}</b></p>
                )}
                {r.explanation && (
                  <div className="mt-2 rounded-lg bg-slate-100 p-2.5 text-sm dark:bg-white/5">
                    <MarkdownMessage content={r.explanation} />
                  </div>
                )}
              </div>
            ))}
          </div>

          <button onClick={() => setPhase("config")}
                  className="mt-6 w-full rounded-xl border border-slate-300 py-2.5 font-semibold transition hover:border-brand-400 dark:border-white/15">
            Take another test
          </button>
        </div>
      </Scroll>
    );
  }

  // ---- Taking ----
  return (
    <Scroll>
      <div className="mx-auto max-w-3xl px-4 py-6">
        <div className="sticky top-0 z-10 -mx-4 mb-4 flex items-center justify-between border-b border-slate-200/70 bg-white/80 px-4 py-2 backdrop-blur dark:border-white/10 dark:bg-slate-950/70">
          <span className="text-sm font-semibold">{exam} · {subject}</span>
          <span className="font-mono text-sm text-brand-600 dark:text-brand-400">⏱ {fmt(elapsed)}</span>
        </div>

        <div className="space-y-5">
          {questions.map((q, i) => (
            <div key={q.id} className="rounded-xl border border-slate-200 bg-white p-4 dark:border-white/10 dark:bg-slate-900">
              <div className="mb-2 flex items-center gap-2 text-xs text-slate-400">
                <span className="font-semibold text-slate-600 dark:text-slate-300">Q{i + 1}</span>
                <span className="rounded-full bg-slate-100 px-2 py-0.5 dark:bg-white/10">
                  {q.type} · {q.marks} mark{q.marks > 1 ? "s" : ""}
                </span>
              </div>
              <div className="text-[15px]"><MarkdownMessage content={q.question} /></div>

              {q.type === "NAT" ? (
                <input
                  type="text" inputMode="decimal" placeholder="Your numerical answer"
                  value={(answers[q.id] as string) || ""}
                  onChange={(e) => setAns(q.id, e.target.value)}
                  className="mt-3 w-48 rounded-lg border border-slate-300 bg-white px-3 py-1.5 text-sm outline-none focus:border-brand-500 dark:border-white/15 dark:bg-slate-800"
                />
              ) : (
                <ul className="mt-3 space-y-1.5">
                  {q.options.map((o, idx) => {
                    const sel = q.type === "MSQ"
                      ? Array.isArray(answers[q.id]) && (answers[q.id] as number[]).includes(idx)
                      : answers[q.id] === idx;
                    return (
                      <li key={idx}>
                        <button
                          onClick={() => q.type === "MSQ" ? toggleMsq(q.id, idx) : setAns(q.id, idx)}
                          className={`flex w-full items-center gap-2 rounded-lg border px-3 py-2 text-left text-sm transition ${sel
                            ? "border-brand-500 bg-brand-500/10 text-brand-700 dark:text-brand-200"
                            : "border-slate-200 hover:border-brand-300 dark:border-white/10"}`}>
                          <span className={`grid h-5 w-5 shrink-0 place-items-center ${q.type === "MSQ" ? "rounded" : "rounded-full"} border ${sel ? "border-brand-500 bg-brand-500 text-white" : "border-slate-300 dark:border-white/20"}`}>
                            {sel ? "✓" : String.fromCharCode(65 + idx)}
                          </span>
                          {o}
                        </button>
                      </li>
                    );
                  })}
                </ul>
              )}
            </div>
          ))}
        </div>

        <button onClick={submit}
                className="mt-6 w-full rounded-xl bg-gradient-to-br from-brand-500 to-accent-500 py-2.5 font-semibold text-white shadow-md transition hover:opacity-90">
          Submit test
        </button>
      </div>
    </Scroll>
  );
}

// ---- small UI helpers ----
function Center({ children }: { children: React.ReactNode }) {
  return <div className="grid h-full place-items-center overflow-y-auto p-4">{children}</div>;
}
function Scroll({ children }: { children: React.ReactNode }) {
  return <div className="h-full overflow-y-auto">{children}</div>;
}
function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <label className="block text-sm">
      <span className="mb-1 block text-xs font-medium text-slate-500 dark:text-slate-400">{label}</span>
      {children}
    </label>
  );
}
function Select({ value, onChange, options }: {
  value: string; onChange: (v: string) => void; options: (string | [string, string])[];
}) {
  return (
    <select value={value} onChange={(e) => onChange(e.target.value)}
            className="w-full rounded-lg border border-slate-300 bg-white px-3 py-1.5 text-sm outline-none focus:border-brand-500 dark:border-white/15 dark:bg-slate-800">
      {options.map((o) => {
        const [val, lab] = Array.isArray(o) ? o : [o, o];
        return <option key={val} value={val}>{lab}</option>;
      })}
    </select>
  );
}
function Stat({ label, value }: { label: string; value: string }) {
  return (
    <span className="rounded-full bg-white/70 px-3 py-1 dark:bg-white/10">
      <b>{value}</b> <span className="text-slate-500">{label}</span>
    </span>
  );
}
