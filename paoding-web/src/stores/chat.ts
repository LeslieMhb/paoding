import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export interface ChatMessage {
  id: string
  role: 'user' | 'assistant'
  content: string
  thinking?: string
  timestamp: number
}

export interface ChatSession {
  id: string
  title: string
  messages: ChatMessage[]
  createdAt: number
}

const STORAGE_KEY = 'paoding_sessions'
const ACTIVE_KEY = 'paoding_active_session'

function loadSessions(): ChatSession[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : []
  } catch {
    return []
  }
}

function saveSessions(sessions: ChatSession[]) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(sessions))
}

export const useChatStore = defineStore('chat', () => {
  const sessions = ref<ChatSession[]>(loadSessions())
  const activeSessionId = ref<string>(localStorage.getItem(ACTIVE_KEY) || '')

  function createSession(): string {
    const session: ChatSession = {
      id: crypto.randomUUID(),
      title: '新对话',
      messages: [],
      createdAt: Date.now(),
    }
    sessions.value.unshift(session)
    activeSessionId.value = session.id
    return session.id
  }

  function addMessage(sessionId: string, role: 'user' | 'assistant', content: string, thinking?: string) {
    const session = sessions.value.find((s) => s.id === sessionId)
    if (!session) return
    session.messages.push({
      id: crypto.randomUUID(),
      role,
      content,
      thinking,
      timestamp: Date.now(),
    })
    // Update title from first user message
    if (role === 'user' && session.messages.filter((m) => m.role === 'user').length === 1) {
      session.title = content.slice(0, 30) + (content.length > 30 ? '...' : '')
    }
  }

  function updateLastAssistantMessage(sessionId: string, content: string) {
    const session = sessions.value.find((s) => s.id === sessionId)
    if (!session) return
    const lastMsg = session.messages.findLast((m) => m.role === 'assistant')
    if (lastMsg) {
      lastMsg.content = content
    }
  }

  function deleteSession(sessionId: string) {
    sessions.value = sessions.value.filter((s) => s.id !== sessionId)
    if (activeSessionId.value === sessionId) {
      activeSessionId.value = sessions.value[0]?.id || ''
    }
  }

  function getActiveSession(): ChatSession | undefined {
    return sessions.value.find((s) => s.id === activeSessionId.value)
  }

  /** Get history pairs for multi-turn context */
  function getHistory(sessionId: string): { role: string; content: string }[] {
    const session = sessions.value.find((s) => s.id === sessionId)
    if (!session) return []
    return session.messages.map((m) => ({ role: m.role, content: m.content }))
  }

  // Initialize with a session if empty
  if (sessions.value.length === 0) {
    createSession()
  } else if (!activeSessionId.value || !sessions.value.find((s) => s.id === activeSessionId.value)) {
    activeSessionId.value = sessions.value[0].id
  }

  // Persist on changes
  watch(sessions, (val) => saveSessions(val), { deep: true })
  watch(activeSessionId, (val) => localStorage.setItem(ACTIVE_KEY, val))

  return {
    sessions,
    activeSessionId,
    createSession,
    addMessage,
    updateLastAssistantMessage,
    deleteSession,
    getActiveSession,
    getHistory,
  }
})
