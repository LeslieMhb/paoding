import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '',
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
  history?: { role: string; content: string }[]
}

export type SSEEventType =
  | 'start_thinking'
  | 'thinking'
  | 'end_thinking'
  | 'start_message'
  | 'message'
  | 'end_message'
  | 'error'
  | 'conversation_ending'

export interface SSEEvent {
  event_type: SSEEventType
  data: Record<string, unknown>
}

/**
 * Connect to SSE stream for chat messages.
 * Returns an async generator yielding SSE events.
 */
export async function* streamChat(request: ChatRequest): AsyncGenerator<SSEEvent> {
  const baseURL = import.meta.env.VITE_API_BASE_URL || ''
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
  let currentEvent = ''
  let currentData = ''

  while (true) {
    const { done, value } = await reader.read()
    if (done) break

    buffer += decoder.decode(value, { stream: true })
    const lines = buffer.split('\n')
    buffer = lines.pop() || ''

    for (const line of lines) {
      const trimmed = line.trimEnd()  // handle \r\n line endings
      if (trimmed.startsWith('event: ')) {
        currentEvent = trimmed.slice(7).trim()
      } else if (trimmed.startsWith('data: ')) {
        currentData = trimmed.slice(6)
      } else if (trimmed === '' && currentEvent && currentData) {
        try {
          const parsedData = JSON.parse(currentData)
          yield { event_type: currentEvent as SSEEventType, data: parsedData }
        } catch {
          yield { event_type: currentEvent as SSEEventType, data: { raw: currentData } }
        }
        currentEvent = ''
        currentData = ''
      }
    }
  }
}

export default api
