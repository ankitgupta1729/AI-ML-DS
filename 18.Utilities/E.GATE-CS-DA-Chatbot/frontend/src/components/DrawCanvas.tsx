import { useEffect, useRef, useState } from "react";
import { XIcon } from "./icons";

/** A simple drawing pad — sketch a problem/diagram, then send it as an image
 * attachment that the vision model can read. */
export default function DrawCanvas({
  onSave,
  onClose,
}: {
  onSave: (dataUrl: string) => void;
  onClose: () => void;
}) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const drawing = useRef(false);
  const [color, setColor] = useState("#0f172a");

  useEffect(() => {
    const c = canvasRef.current;
    if (!c) return;
    const ctx = c.getContext("2d")!;
    ctx.fillStyle = "#ffffff";
    ctx.fillRect(0, 0, c.width, c.height);
  }, []);

  const pos = (e: React.PointerEvent) => {
    const c = canvasRef.current!;
    const r = c.getBoundingClientRect();
    return { x: (e.clientX - r.left) * (c.width / r.width), y: (e.clientY - r.top) * (c.height / r.height) };
  };

  const start = (e: React.PointerEvent) => {
    drawing.current = true;
    const ctx = canvasRef.current!.getContext("2d")!;
    const { x, y } = pos(e);
    ctx.beginPath();
    ctx.moveTo(x, y);
  };
  const move = (e: React.PointerEvent) => {
    if (!drawing.current) return;
    const ctx = canvasRef.current!.getContext("2d")!;
    const { x, y } = pos(e);
    ctx.strokeStyle = color;
    ctx.lineWidth = 3;
    ctx.lineCap = "round";
    ctx.lineJoin = "round";
    ctx.lineTo(x, y);
    ctx.stroke();
  };
  const end = () => (drawing.current = false);

  const clear = () => {
    const c = canvasRef.current!;
    const ctx = c.getContext("2d")!;
    ctx.fillStyle = "#ffffff";
    ctx.fillRect(0, 0, c.width, c.height);
  };

  return (
    <div className="fixed inset-0 z-50 grid place-items-center bg-black/50 p-4 backdrop-blur-sm">
      <div className="w-full max-w-2xl rounded-2xl border border-slate-200 bg-white p-4 shadow-2xl dark:border-white/10 dark:bg-slate-900">
        <div className="mb-3 flex items-center justify-between">
          <h3 className="text-sm font-bold text-slate-800 dark:text-white">
            ✏️ Sketch your question or working
          </h3>
          <button onClick={onClose} className="grid h-8 w-8 place-items-center rounded-lg text-slate-500 hover:bg-slate-100 dark:hover:bg-white/10">
            <XIcon width={18} height={18} />
          </button>
        </div>
        <canvas
          ref={canvasRef}
          width={760}
          height={420}
          onPointerDown={start}
          onPointerMove={move}
          onPointerUp={end}
          onPointerLeave={end}
          className="w-full touch-none rounded-xl border border-slate-300 dark:border-white/15"
          style={{ aspectRatio: "760 / 420" }}
        />
        <div className="mt-3 flex items-center gap-2">
          <div className="flex gap-1.5">
            {["#0f172a", "#dc2626", "#2563eb", "#16a34a"].map((c) => (
              <button
                key={c}
                onClick={() => setColor(c)}
                className={`h-6 w-6 rounded-full border-2 ${color === c ? "border-brand-500" : "border-transparent"}`}
                style={{ background: c }}
                title="Pen colour"
              />
            ))}
          </div>
          <button onClick={clear} className="rounded-lg px-3 py-1.5 text-xs text-slate-500 hover:bg-slate-100 dark:hover:bg-white/10">
            Clear
          </button>
          <button
            onClick={() => onSave(canvasRef.current!.toDataURL("image/png"))}
            className="ml-auto rounded-lg bg-gradient-to-br from-brand-500 to-accent-500 px-4 py-1.5 text-sm font-semibold text-white shadow-sm transition hover:opacity-90"
          >
            Attach sketch
          </button>
        </div>
      </div>
    </div>
  );
}
