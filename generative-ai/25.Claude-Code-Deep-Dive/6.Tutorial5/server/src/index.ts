import cors from "cors";
import express from "express";
import type { ErrorRequestHandler } from "express";
import * as store from "./store.js";

const app = express();
const PORT = 3001;
const MAX_TITLE_LENGTH = 200;

app.use(cors());
app.use(express.json());

app.get("/health", (_req, res) => {
  res.json({ status: "ok" });
});

app.get("/todos", (_req, res) => {
  res.json(store.list());
});

app.post("/todos", (req, res) => {
  const title = typeof req.body?.title === "string" ? req.body.title.trim() : "";
  if (!title) {
    res.status(400).json({ error: "title is required" });
    return;
  }
  if (title.length > MAX_TITLE_LENGTH) {
    res.status(400).json({ error: `title must be ${MAX_TITLE_LENGTH} characters or fewer` });
    return;
  }
  const todo = store.create(title);
  res.status(201).json(todo);
});

app.patch("/todos/:id", (req, res) => {
  const { title, completed } = req.body ?? {};
  const patch: { title?: string; completed?: boolean } = {};
  if (typeof title === "string") {
    const trimmed = title.trim();
    if (!trimmed) {
      res.status(400).json({ error: "title cannot be empty" });
      return;
    }
    if (trimmed.length > MAX_TITLE_LENGTH) {
      res.status(400).json({ error: `title must be ${MAX_TITLE_LENGTH} characters or fewer` });
      return;
    }
    patch.title = trimmed;
  }
  if (typeof completed === "boolean") patch.completed = completed;
  const updated = store.update(req.params.id, patch);
  if (!updated) {
    res.status(404).json({ error: "todo not found" });
    return;
  }
  res.json(updated);
});

app.delete("/todos/:id", (req, res) => {
  const ok = store.remove(req.params.id);
  if (!ok) {
    res.status(404).json({ error: "todo not found" });
    return;
  }
  res.status(204).end();
});

const errorHandler: ErrorRequestHandler = (err, _req, res, _next) => {
  if (err?.type === "entity.parse.failed") {
    res.status(400).json({ error: "invalid JSON body" });
    return;
  }
  console.error("Unhandled error:", err);
  res.status(500).json({ error: "internal server error" });
};

app.use(errorHandler);

app.listen(PORT, () => {
  console.log(`Server listening on http://localhost:${PORT}`);
});
