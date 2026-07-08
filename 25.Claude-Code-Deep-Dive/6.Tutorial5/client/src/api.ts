export type Todo = {
  id: string;
  title: string;
  completed: boolean;
};

const API = 'http://localhost:3001';

async function handle<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const text = await res.text().catch(() => res.statusText);
    throw new Error(text || `Request failed with ${res.status}`);
  }
  if (res.status === 204) return undefined as T;
  return res.json() as Promise<T>;
}

export function fetchTodos(): Promise<Todo[]> {
  return fetch(`${API}/todos`).then(handle<Todo[]>);
}

export function createTodo(title: string): Promise<Todo> {
  return fetch(`${API}/todos`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title }),
  }).then(handle<Todo>);
}

export function updateTodo(
  id: string,
  patch: Partial<Pick<Todo, 'title' | 'completed'>>,
): Promise<Todo> {
  return fetch(`${API}/todos/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(patch),
  }).then(handle<Todo>);
}

export function deleteTodo(id: string): Promise<void> {
  return fetch(`${API}/todos/${id}`, { method: 'DELETE' }).then(handle<void>);
}
