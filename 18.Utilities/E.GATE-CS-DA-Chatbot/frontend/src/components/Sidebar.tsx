import type { ComponentType } from "react";
import type { View } from "../types";
import {
  CalendarIcon,
  ChartIcon,
  ChatIcon,
  ClipboardIcon,
  FlameIcon,
  LayersIcon,
} from "./icons";

const ITEMS: { key: View; label: string; Icon: ComponentType<{ width?: number; height?: number }> }[] = [
  { key: "chat", label: "Chat", Icon: ChatIcon },
  { key: "mock", label: "Mock Test", Icon: ClipboardIcon },
  { key: "review", label: "Flashcards", Icon: LayersIcon },
  { key: "planner", label: "Planner", Icon: CalendarIcon },
  { key: "dashboard", label: "Dashboard", Icon: ChartIcon },
  { key: "daily", label: "Daily", Icon: FlameIcon },
];

export default function Sidebar({
  view,
  onSelect,
  dueCount = 0,
}: {
  view: View;
  onSelect: (v: View) => void;
  dueCount?: number;
}) {
  return (
    <nav className="flex w-16 shrink-0 flex-col gap-1 border-r border-slate-200/70 bg-white/60 p-2 backdrop-blur-xl md:w-52 dark:border-white/10 dark:bg-slate-950/40">
      {ITEMS.map(({ key, label, Icon }) => {
        const active = view === key;
        return (
          <button
            key={key}
            onClick={() => onSelect(key)}
            title={label}
            className={`group relative flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition ${
              active
                ? "bg-gradient-to-r from-brand-500/15 to-accent-500/10 text-brand-600 dark:text-brand-300"
                : "text-slate-500 hover:bg-slate-100 hover:text-slate-900 dark:text-slate-400 dark:hover:bg-white/10 dark:hover:text-white"
            }`}
          >
            <span
              className={`absolute left-0 top-1/2 h-6 w-1 -translate-y-1/2 rounded-full bg-gradient-to-b from-brand-500 to-accent-500 transition ${
                active ? "opacity-100" : "opacity-0"
              }`}
            />
            <Icon width={20} height={20} />
            <span className="hidden md:inline">{label}</span>
            {key === "review" && dueCount > 0 && (
              <span className="ml-auto hidden rounded-full bg-brand-500 px-1.5 py-0.5 text-[10px] font-bold text-white md:inline">
                {dueCount}
              </span>
            )}
          </button>
        );
      })}
      <a
        href="https://gateoverflow.in"
        target="_blank"
        rel="noreferrer noopener"
        className="mt-auto hidden px-3 py-2 text-[11px] text-slate-400 hover:text-brand-500 md:block"
      >
        gateoverflow.in ↗
      </a>
    </nav>
  );
}
