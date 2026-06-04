import { useCallback, useEffect, useState } from "react";
import GuideModal from "./components/GuideModal";
import Header from "./components/Header";
import Sidebar from "./components/Sidebar";
import { useChat } from "./hooks/useChat";
import { useTheme } from "./hooks/useTheme";
import { fetchMeta, getAnalytics } from "./lib/api";
import type { Meta, View } from "./types";
import ChatView from "./views/ChatView";
import Daily from "./views/Daily";
import Dashboard from "./views/Dashboard";
import MockTest from "./views/MockTest";
import Planner from "./views/Planner";
import Review from "./views/Review";

export default function App() {
  const { theme, toggle } = useTheme();
  const chat = useChat();
  const [meta, setMeta] = useState<Meta | null>(null);
  const [connecting, setConnecting] = useState(true);
  const [view, setView] = useState<View>("chat");
  const [dueCount, setDueCount] = useState(0);
  const [showGuide, setShowGuide] = useState(false);

  // Open the guide automatically on a user's first visit.
  useEffect(() => {
    if (!localStorage.getItem("go-guide-seen")) {
      setShowGuide(true);
      localStorage.setItem("go-guide-seen", "1");
    }
  }, []);

  useEffect(() => {
    let alive = true;
    fetchMeta()
      .then((m) => alive && setMeta(m))
      .catch(() => {})
      .finally(() => alive && setConnecting(false));
    return () => { alive = false; };
  }, []);

  // Refresh the "cards due" badge when navigating (cheap, best-effort).
  useEffect(() => {
    getAnalytics().then((a) => a?.ok && setDueCount(a.due_reviews)).catch(() => {});
  }, [view]);

  const askInChat = useCallback(
    (prompt: string) => {
      setView("chat");
      chat.send(prompt);
    },
    [chat],
  );

  return (
    <div className="relative flex h-full flex-col overflow-hidden bg-gradient-to-b from-slate-50 to-slate-100 text-slate-900 dark:from-slate-950 dark:to-slate-900 dark:text-slate-100">
      <div aria-hidden className="pointer-events-none absolute -top-32 left-1/2 h-72 w-[42rem] -translate-x-1/2 rounded-full bg-brand-500/10 blur-3xl" />

      {showGuide && <GuideModal onClose={() => setShowGuide(false)} />}

      <Header
        meta={meta}
        theme={theme}
        onToggleTheme={toggle}
        onClear={chat.clear}
        onHelp={() => setShowGuide(true)}
        hasMessages={view === "chat" && chat.messages.length > 0}
      />

      <div className="flex min-h-0 flex-1">
        <Sidebar view={view} onSelect={setView} dueCount={dueCount} />

        <main className="min-w-0 flex-1">
          {view === "chat" && (
            <ChatView
              meta={meta}
              connecting={connecting}
              messages={chat.messages}
              isStreaming={chat.isStreaming}
              send={chat.send}
              stop={chat.stop}
              regenerate={chat.regenerate}
              sendFeedback={chat.sendFeedback}
            />
          )}
          {view === "mock" && <MockTest />}
          {view === "review" && <Review />}
          {view === "planner" && <Planner />}
          {view === "dashboard" && <Dashboard />}
          {view === "daily" && <Daily onAsk={askInChat} />}
        </main>
      </div>
    </div>
  );
}
