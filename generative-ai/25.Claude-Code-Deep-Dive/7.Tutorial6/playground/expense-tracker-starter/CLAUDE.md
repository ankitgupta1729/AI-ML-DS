# Repository Guidelines

This is a course starter: a single-page React expense tracker that intentionally ships with a known bug, rough UI, and messy code so the lessons can refactor it. Treat existing imperfections as material to fix, not patterns to mirror.

## Project Structure & Module Organization

- `src/App.jsx` — the entire app. All transaction state, totals, filtering, and the form/table UI live in this one component. Splitting concerns out of `App.jsx` is a typical refactor target.
- `src/main.jsx` — React 19 entry; mounts `<App />` inside `<StrictMode>` via `createRoot`.
- `src/App.css`, `src/index.css` — global styles; no CSS modules or component-scoped styles in use.
- `src/assets/`, `public/` — static assets served by Vite.
- `index.html` — Vite's HTML entry; loads `/src/main.jsx`.

Note: amounts in the seeded `transactions` array are **strings**, but `totalIncome` / `totalExpenses` use `reduce((sum, t) => sum + t.amount, 0)`. That's the intentional bug — be aware before "refactoring" around it.

## Build, Test, and Development Commands

- `npm install` — install dependencies (required before first run).
- `npm run dev` — start Vite dev server at `http://localhost:5173`.
- `npm run build` — production build to `dist/`.
- `npm run preview` — serve the built `dist/` locally.
- `npm run lint` — run ESLint over the repo.

There is no test runner configured; do not invent `npm test`.

## Coding Style & Naming Conventions

- ESLint flat config (`eslint.config.js`) extends `@eslint/js` recommended, `eslint-plugin-react-hooks` flat recommended, and `eslint-plugin-react-refresh` (Vite preset).
- 2-space indent, single quotes, no semicolons in config files; JSX uses double quotes and trailing semicolons (match the surrounding file).
- `no-unused-vars` is an error, but vars matching `^[A-Z_]` are ignored — keep that pattern for intentionally unused constants/components.
- Components: PascalCase `.jsx`. Hooks/handlers: camelCase (`handleSubmit`).

## Commit & Pull Request Guidelines

History has only the initial commit, so no convention is established. Use short, imperative subjects (`Fix amount summation`, `Extract TransactionTable`) and describe the user-visible change in the body.
