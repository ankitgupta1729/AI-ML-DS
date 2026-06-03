/**
 * GateOverflow brand mark — bold "GO" with a red question mark, matching the
 * gateoverflow.in favicon. `currentColor` drives the "GO" so it adapts to
 * light/dark; the question mark stays GateOverflow red.
 */
export default function Logo({
  size = 40,
  withBackplate = true,
}: {
  size?: number;
  withBackplate?: boolean;
}) {
  const mark = (
    <svg
      viewBox="0 0 100 100"
      width={withBackplate ? size * 0.78 : size}
      height={withBackplate ? size * 0.78 : size}
      aria-hidden
    >
      <text
        x="60"
        y="50"
        textAnchor="middle"
        fontFamily="Georgia, 'Times New Roman', serif"
        fontSize="74"
        fontWeight="700"
        fill="#dc2626"
        transform="rotate(9 60 44)"
      >
        ?
      </text>
      <text
        x="49"
        y="86"
        textAnchor="middle"
        fontFamily="ui-sans-serif, system-ui, Arial, sans-serif"
        fontSize="50"
        fontWeight="900"
        fill="currentColor"
        letterSpacing="-2"
      >
        GO
      </text>
    </svg>
  );

  if (!withBackplate) {
    return (
      <span
        className="inline-grid place-items-center text-slate-900 dark:text-white"
        style={{ width: size, height: size }}
      >
        {mark}
      </span>
    );
  }

  return (
    <div
      className="grid place-items-center rounded-2xl border border-slate-200 bg-white text-slate-900 shadow-sm dark:border-white/10 dark:bg-slate-800 dark:text-white"
      style={{ width: size, height: size }}
    >
      {mark}
    </div>
  );
}
