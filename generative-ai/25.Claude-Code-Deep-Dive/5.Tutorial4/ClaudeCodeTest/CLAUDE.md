# CLAUDE.md

Project context for Claude Code. See `AGENTS.md` for the full repository guidelines (structure, conventions, manual test checklist) — this file complements it with Claude-specific notes.

## What this is

A single-file Tic Tac Toe web game. Everything — markup, styles, and logic — lives inline in `index.html`. No build, no dependencies, no tests.

## Code map (`index.html`)

- **State:** `cells` (length-9 array), `currentPlayer` (`'X'`/`'O'`), `gameOver` (boolean) — module-scope in the inline `<script>`.
- **Win detection:** `winLines` array (8 lines) consumed by `checkWinner()`.
- **Render model:** `render()` rebuilds the board from `cells` on every move. Do not mutate cell DOM nodes elsewhere — the only exception is `handleMove()` adding the `.win` class after a winning render.
- **Entry points:** `handleMove(i)` (cell click), `reset()` (New Game button), and `render()` called once on load.

## Working in this repo

- Run with `open index.html` — no server needed.
- Keep the app single-file unless a change genuinely needs splitting (per `AGENTS.md`).
- Match existing style: 2-space indent, single quotes in JS, double quotes in HTML, `camelCase` JS, `kebab-case` CSS.
- No automated tests — verify changes manually in a browser against the checklist in `AGENTS.md`.

## Commit style

History uses terse `added content` messages. For new commits, prefer short imperative subjects (e.g. `fix draw detection`, `add keyboard input`).
