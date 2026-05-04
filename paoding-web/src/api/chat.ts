import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor: attach token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export interface ChatRequest {
  message: string
  session_id: string
  user_id: string
}

export interface SSEEvent {
  event_type: string
  data: string
}

/**
 * Connect to SSE stream for chat messages.
 * Returns an async generator yielding SSE events.
 */
export async function* streamChat(request: ChatRequest): AsyncGenerator<SSEEvent> {
  const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
  const response = await fetch(`${baseURL}/api/chat/sendMessage`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${localStorage.getItem('token') || ''}`,
    },
    body: JSON.stringify(request),
  })

  if (!response.ok) {
    throw new Error(`Chat request failed: ${response.status}`)
  }

  const reader = response.body?.getReader()
  if (!reader) throw new Error('No response body')

  const decoder = new TextDecoder()
  let buffer = ''

  while (true) {
    const { done, value } = await reader.read()
    if (done) break

    buffer += decoder.decode(value, { stream: true })
    const lines = buffer.split('\n')
    buffer = lines.pop() || ''

    let currentEvent = ''
    let currentData = ''

    for (const line of lines) {
      if (line.startsWith('event: ')) {
        currentEvent = line.slice(7).trim()
      } else if (line.startsWith('data: ')) {
        currentData = line.slice(6)
      } else if (line === '' && currentEvent && currentData) {
        yield { event_type: currentEvent, data: currentData }
        currentEvent = ''
        currentData = ''
      }
    }
  }
}

export default api
