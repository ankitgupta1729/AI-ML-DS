import { randomUUID } from "node:crypto";
import type { Todo } from "./types.js";

let todos: Todo[] = [];

export function list(): Todo[] {
  return todos;
}

export function create(title: string): Todo {
  const todo: Todo = { id: randomUUID(), title, completed: false };
  todos.push(todo);
  return todo;
}

export function update(
  id: string,
  patch: Partial<Pick<Todo, "title" | "completed">>,
): Todo | undefined {
  const todo = todos.find((t) => t.id === id);
  if (!todo) return undefined;
  if (patch.title !== undefined) todo.title = patch.title;
  if (patch.completed !== undefined) todo.completed = patch.completed;
  return todo;
}

export function remove(id: string): boolean {
  const before = todos.length;
  todos = todos.filter((t) => t.id !== id);
  return todos.length < before;
}
