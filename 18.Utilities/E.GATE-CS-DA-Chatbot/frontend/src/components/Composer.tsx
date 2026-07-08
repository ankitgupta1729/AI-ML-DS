import { useEffect, useRef, useState } from "react";
import { useSpeechInput } from "../hooks/useSpeech";
import type { Attachment } from "../types";
import DrawCanvas from "./DrawCanvas";
import { DocIcon, MicIcon, PaperclipIcon, PenIcon, SendIcon, StopIcon, XIcon } from "./icons";

interface Props {
  onSend: (text: string, attachments: Attachment[]) => void;
  onStop: () => void;
  isStreaming: boolean;
  disabled?: boolean;
}

const MAX_FILES = 4;
const MAX_SIZE = 8 * 1024 * 1024; // 8 MB per file
const ACCEPT =
  "image/*,.pdf,.txt,.md,.markdown,.csv,.json,.py,.c,.cpp,.java,.sql";

const fileToAttachment = (file: File): Promise<Attachment> =>
  new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () =>
      resolve({
        name: file.name,
        mime: file.type || "application/octet-stream",
        data: reader.result as string,
        isImage: file.type.startsWith("image/"),
      });
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });

export default function Composer({
  onSend,
  onStop,
  isStreaming,
  disabled,
}: Props) {
  const [text, setText] = useState("");
  const [files, setFiles] = useState<Attachment[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [drawing, setDrawing] = useState(false);
  const ref = useRef<HTMLTextAreaElement>(null);
  const fileRef = useRef<HTMLInputElement>(null);
  const voice = useSpeechInput((t) =>
    setText((prev) => (prev ? prev + " " : "") + t),
  );

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = `${Math.min(el.scrollHeight, 200)}px`;
  }, [text]);

  const addFiles = async (list: FileList | null) => {
    if (!list) return;
    setError(null);
    const incoming = Array.from(list);
    const room = MAX_FILES - files.length;
    if (incoming.length > room) {
      setError(`You can attach up to ${MAX_FILES} files.`);
    }
    const accepted: Attachment[] = [];
    for (const f of incoming.slice(0, Math.max(room, 0))) {
      if (f.size > MAX_SIZE) {
        setError(`"${f.name}" is larger than 8 MB.`);
        continue;
      }
      accepted.push(await fileToAttachment(f));
    }
    setFiles((prev) => [...prev, ...accepted]);
    if (fileRef.current) fileRef.current.value = "";
  };

  const removeFile = (i: number) =>
    setFiles((prev) => prev.filter((_, idx) => idx !== i));

  const submit = () => {
    if ((!text.trim() && files.length === 0) || isStreaming) return;
    onSend(text, files);
    setText("");
    setFiles([]);
    setError(null);
  };

  const onKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      submit();
    }
  };

  const onPaste = (e: React.ClipboardEvent) => {
    const imgs = Array.from(e.clipboardData.files).filter((f) =>
      f.type.startsWith("image/"),
    );
    if (imgs.length) {
      e.preventDefault();
      const dt = new DataTransfer();
      imgs.forEach((f) => dt.items.add(f));
      addFiles(dt.files);
    }
  };

  const addDrawing = (dataUrl: string) => {
    if (files.length >= MAX_FILES) {
      setError(`You can attach up to ${MAX_FILES} files.`);
    } else {
      setFiles((prev) => [
        ...prev,
        { name: `sketch-${Date.now()}.png`, mime: "image/png", data: dataUrl, isImage: true },
      ]);
    }
    setDrawing(false);
  };

  return (
    <>
      {drawing && <DrawCanvas onSave={addDrawing} onClose={() => setDrawing(false)} />}
    <div className="border-t border-slate-200/70 bg-white/70 backdrop-blur-xl dark:border-white/10 dark:bg-slate-950/60">
      <div className="mx-auto max-w-4xl px-4 py-3">
        {files.length > 0 && (
          <div className="mb-2 flex flex-wrap gap-2">
            {files.map((f, i) => (
              <div
                key={i}
                className="group relative flex items-center gap-2 rounded-xl border border-slate-200 bg-white p-1.5 pr-7 shadow-sm dark:border-white/10 dark:bg-slate-900"
              >
                {f.isImage ? (
                  <img
                    src={f.data}
                    alt={f.name}
                    className="h-10 w-10 rounded-lg object-cover"
                  />
                ) : (
                  <div className="grid h-10 w-10 place-items-center rounded-lg bg-brand-500/10 text-brand-600 dark:text-brand-400">
                    <DocIcon width={18} height={18} />
                  </div>
                )}
                <span className="max-w-[140px] truncate text-xs text-slate-600 dark:text-slate-300">
                  {f.name}
                </span>
                <button
                  onClick={() => removeFile(i)}
                  className="absolute right-1 top-1 grid h-5 w-5 place-items-center rounded-full bg-slate-200 text-slate-600 opacity-0 transition group-hover:opacity-100 dark:bg-white/15 dark:text-white"
                  title="Remove"
                >
                  <XIcon width={12} height={12} />
                </button>
              </div>
            ))}
          </div>
        )}

        {error && (
          <p className="mb-1.5 text-xs text-red-500">{error}</p>
        )}

        <div className="flex items-end gap-2 rounded-2xl border border-slate-300 bg-white p-2 shadow-sm transition focus-within:border-brand-500 focus-within:ring-2 focus-within:ring-brand-500/30 dark:border-white/10 dark:bg-slate-900">
          <input
            ref={fileRef}
            type="file"
            multiple
            accept={ACCEPT}
            className="hidden"
            onChange={(e) => addFiles(e.target.files)}
          />
          <button
            onClick={() => fileRef.current?.click()}
            disabled={disabled || files.length >= MAX_FILES}
            title="Attach images or files"
            className="grid h-10 w-10 shrink-0 place-items-center rounded-xl text-slate-500 transition hover:bg-slate-100 hover:text-brand-600 disabled:opacity-40 dark:text-slate-400 dark:hover:bg-white/10"
          >
            <PaperclipIcon width={19} height={19} />
          </button>
          <button
            onClick={() => setDrawing(true)}
            disabled={disabled || files.length >= MAX_FILES}
            title="Draw / sketch a question"
            className="grid h-10 w-10 shrink-0 place-items-center rounded-xl text-slate-500 transition hover:bg-slate-100 hover:text-brand-600 disabled:opacity-40 dark:text-slate-400 dark:hover:bg-white/10"
          >
            <PenIcon width={18} height={18} />
          </button>
          {voice.supported && (
            <button
              onClick={voice.toggle}
              disabled={disabled}
              title={voice.listening ? "Stop listening" : "Speak your question"}
              className={`grid h-10 w-10 shrink-0 place-items-center rounded-xl transition disabled:opacity-40 ${
                voice.listening
                  ? "animate-pulse bg-brand-500/15 text-brand-600 dark:text-brand-300"
                  : "text-slate-500 hover:bg-slate-100 hover:text-brand-600 dark:text-slate-400 dark:hover:bg-white/10"
              }`}
            >
              <MicIcon width={18} height={18} />
            </button>
          )}

          <textarea
            ref={ref}
            value={text}
            onChange={(e) => setText(e.target.value)}
            onKeyDown={onKeyDown}
            onPaste={onPaste}
            rows={1}
            placeholder={
              disabled
                ? "Connecting to the server…"
                : "Ask anything about GATE CS / DA — or attach a question image / PDF…"
            }
            disabled={disabled}
            className="max-h-[200px] flex-1 resize-none bg-transparent px-1 py-1.5 text-[15px] text-slate-900 outline-none placeholder:text-slate-400 disabled:opacity-60 dark:text-white"
          />

          {isStreaming ? (
            <button
              onClick={onStop}
              title="Stop generating"
              className="grid h-10 w-10 shrink-0 place-items-center rounded-xl bg-slate-200 text-slate-700 transition hover:bg-slate-300 dark:bg-white/10 dark:text-white dark:hover:bg-white/20"
            >
              <StopIcon width={18} height={18} />
            </button>
          ) : (
            <button
              onClick={submit}
              disabled={(!text.trim() && files.length === 0) || disabled}
              title="Send"
              className="grid h-10 w-10 shrink-0 place-items-center rounded-xl bg-gradient-to-br from-brand-500 to-accent-500 text-white shadow-md shadow-brand-500/30 transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-40"
            >
              <SendIcon width={18} height={18} />
            </button>
          )}
        </div>
        <p className="mt-1.5 text-center text-[11px] text-slate-400">
          {isStreaming
            ? "Generating… press stop to interrupt."
            : "Enter to send · Shift+Enter for a new line · 📎 attach images (solved/asked) or PDFs. Verify critical facts."}
        </p>
      </div>
    </div>
    </>
  );
}
