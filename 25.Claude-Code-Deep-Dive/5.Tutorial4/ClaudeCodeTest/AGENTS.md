# Repository Guidelines

This folder contains a single, self-contained Tic Tac Toe web game. There is no build system, package manager, or test suite — everything lives in `index.html`.

## Project Structure & Module Organization

- `index.html` — the entire app. HTML markup, styles (inside `<style>`), and game logic (inside `<script>`) are all inlined. No external assets, no network calls, no dependencies.
- Game state is held in three module-scope variables in the inline script: `cells` (length-9 array), `currentPlayer` (`'X'` or `'O'`), and `gameOver` (boolean). The board is rebuilt from `cells` on every move via `render()`; do not mutate DOM nodes directly elsewhere.

## Build, Test, and Development Commands

- **Run locally:** `open index.html` (macOS) or double-click the file. No server needed.
- **Optional static server** (useful if you later add modules or fetches): `python3 -m http.server 8000`, then visit `http://localhost:8000/`.

There are no build, lint, or test commands — none are configured.

## Coding Style & Naming Conventions

No linter or formatter is configured. Match the existing file:

- 2-space indentation in HTML, CSS, and JS.
- Single quotes in JS; double quotes in HTML attributes.
- `camelCase` for JS identifiers (`currentPlayer`, `winLines`, `handleMove`).
- `kebab-case` for CSS classes (`.cell`, `.win`); IDs match their JS handles (`#board`, `#status`, `#reset`).
- Keep the app single-file unless a change genuinely needs splitting.

## Testing Guidelines

No automated tests. Verify manually in a browser:

1. X and O alternate; clicking a taken cell is a no-op.
2. Each of the 8 lines in `winLines` highlights and ends the game.
3. A full board with no winner shows "It's a draw!".
4. **New Game** resets `cells`, `currentPlayer`, `gameOver`, and the status line.

## Commit & Pull Request Guidelines

Existing history in this repo uses terse messages like `added content`. For changes here, prefer a short imperative subject that names the change (e.g., `fix draw detection`, `add keyboard input`) so future diffs are scannable. There is no PR template.
