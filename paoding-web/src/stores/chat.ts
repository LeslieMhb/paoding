import { defineStore } from 'pinia'
import { ref } from 'vue'

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

export const useChatStore = defineStore('chat', () => {
  const sessions = ref<ChatSession[]>([])
  const activeSessionId = ref<string>('')

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

  // Initialize with a session
  if (sessions.value.length === 0) {
    createSession()
  }

  return {
    sessions,
    activeSessionId,
    createSession,
    addMessage,
    updateLastAssistantMessage,
    deleteSession,
    getActiveSession,
  }
})
