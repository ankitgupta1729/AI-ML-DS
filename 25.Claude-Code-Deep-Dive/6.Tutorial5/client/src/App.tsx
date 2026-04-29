import { useState, type FormEvent } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import {
  createTodo,
  deleteTodo,
  fetchTodos,
  updateTodo,
  type Todo,
} from './api'
import './App.css'

type MutationContext = { previous: Todo[] | undefined }

export default function App() {
  const queryClient = useQueryClient()
  const [title, setTitle] = useState('')

  const todosQuery = useQuery({
    queryKey: ['todos'],
    queryFn: fetchTodos,
  })

  const addMutation = useMutation({
    mutationFn: (newTitle: string) => createTodo(newTitle),
    onSuccess: () => {
      setTitle('')
      queryClient.invalidateQueries({ queryKey: ['todos'] })
    },
  })

  const toggleMutation = useMutation<Todo, Error, Todo, MutationContext>({
    mutationFn: (todo) => updateTodo(todo.id, { completed: !todo.completed }),
    onMutate: async (todo) => {
      await queryClient.cancelQueries({ queryKey: ['todos'] })
      const previous = queryClient.getQueryData<Todo[]>(['todos'])
      queryClient.setQueryData<Todo[]>(['todos'], (old) =>
        old?.map((t) => (t.id === todo.id ? { ...t, completed: !t.completed } : t)),
      )
      return { previous }
    },
    onError: (_err, _vars, ctx) => {
      queryClient.setQueryData(['todos'], ctx?.previous)
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['todos'] })
    },
  })

  const deleteMutation = useMutation<void, Error, string, MutationContext>({
    mutationFn: (id) => deleteTodo(id),
    onMutate: async (id) => {
      await queryClient.cancelQueries({ queryKey: ['todos'] })
      const previous = queryClient.getQueryData<Todo[]>(['todos'])
      queryClient.setQueryData<Todo[]>(['todos'], (old) =>
        old?.filter((t) => t.id !== id),
      )
      return { previous }
    },
    onError: (_err, _vars, ctx) => {
      queryClient.setQueryData(['todos'], ctx?.previous)
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['todos'] })
    },
  })

  const onSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const trimmed = title.trim()
    if (!trimmed) return
    addMutation.mutate(trimmed)
  }

  const mutationError =
    addMutation.error || toggleMutation.error || deleteMutation.error

  return (
    <main className="app">
      <h1>Todos</h1>

      <form onSubmit={onSubmit} className="add-form">
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="What needs doing?"
          aria-label="New todo title"
        />
        <button type="submit" disabled={addMutation.isPending || !title.trim()}>
          {addMutation.isPending ? 'Adding…' : 'Add'}
        </button>
      </form>

      {mutationError && (
        <p className="error">Action failed: {mutationError.message}</p>
      )}

      {todosQuery.isPending && <p>Loading…</p>}
      {todosQuery.error && (
        <p className="error">Error: {todosQuery.error.message}</p>
      )}

      {todosQuery.data && (
        <ul className="todos">
          {todosQuery.data.length === 0 && <li className="empty">No todos yet.</li>}
          {todosQuery.data.map((todo) => (
            <li key={todo.id} className={todo.completed ? 'done' : ''}>
              <label>
                <input
                  type="checkbox"
                  checked={todo.completed}
                  onChange={() => toggleMutation.mutate(todo)}
                />
                <span>{todo.title}</span>
              </label>
              <button
                type="button"
                onClick={() => deleteMutation.mutate(todo.id)}
                aria-label={`Delete ${todo.title}`}
              >
                ✕
              </button>
            </li>
          ))}
        </ul>
      )}
    </main>
  )
}
