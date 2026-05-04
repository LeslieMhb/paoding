<template>
  <div class="chat-layout">
    <aside class="sidebar">
      <div class="sidebar-header">
        <el-button type="primary" @click="handleNewSession" style="width: 100%">新建对话</el-button>
      </div>
      <div class="session-list">
        <div
          v-for="session in chatStore.sessions"
          :key="session.id"
          class="session-item"
          :class="{ active: session.id === chatStore.activeSessionId }"
          @click="chatStore.activeSessionId = session.id"
        >
          <span class="session-title">{{ session.title }}</span>
          <el-icon class="delete-btn" @click.stop="chatStore.deleteSession(session.id)">
            <Delete />
          </el-icon>
        </div>
      </div>
      <div class="sidebar-footer">
        <span>{{ authStore.username }}</span>
        <el-button text @click="handleLogout">退出</el-button>
      </div>
    </aside>

    <main class="chat-main">
      <div class="message-list" ref="messageListRef">
        <div v-if="isEmpty" class="empty-state">
          <div class="empty-icon">✈️</div>
          <h3>你好，我是庖丁</h3>
          <p>你的 AI 旅行助手，可以帮你查询酒店、交通、景点等信息</p>
          <div class="quick-actions">
            <el-button round @click="handleQuickAction('杭州有哪些好酒店？')">🏨 查酒店</el-button>
            <el-button round @click="handleQuickAction('北京到上海的机票')">🚄 查交通</el-button>
            <el-button round @click="handleQuickAction('杭州三日游攻略')">🗺️ 查景点</el-button>
          </div>
        </div>
        <template v-else>
          <div
            v-for="msg in activeSession?.messages"
            :key="msg.id"
            class="message-item"
            :class="msg.role"
          >
            <div class="message-avatar">{{ msg.role === 'user' ? '🧑' : '🤖' }}</div>
            <div class="message-bubble">
              <div v-if="msg.thinking" class="thinking-block">
                <details>
                  <summary>思考过程</summary>
                  <div class="thinking-content">{{ msg.thinking }}</div>
                </details>
              </div>
              <div class="message-content" v-html="renderMarkdown(msg.content)"></div>
            </div>
          </div>
          <div v-if="streaming" class="message-item assistant">
            <div class="message-avatar">🤖</div>
            <div class="message-bubble">
              <div v-if="thinkingText && !streamingContent" class="thinking-indicator">
                <span class="thinking-dot"></span>
                {{ thinkingText }}
              </div>
              <div v-if="streamingContent" class="message-content streaming-cursor" v-html="renderMarkdown(streamingContent)"></div>
            </div>
          </div>
        </template>
      </div>

      <div class="input-area">
        <el-input
          v-model="inputMessage"
          type="textarea"
          :rows="2"
          placeholder="输入你的问题..."
          @keydown.enter.exact.prevent="handleSend"
          :disabled="streaming"
        />
        <el-button
          type="primary"
          @click="handleSend"
          :loading="streaming"
          :disabled="!inputMessage.trim()"
        >
          发送
        </el-button>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useChatStore } from '../stores/chat'
import { streamChat } from '../api/chat'
import { Delete } from '@element-plus/icons-vue'
import MarkdownIt from 'markdown-it'

const md = new MarkdownIt({ breaks: true })

const router = useRouter()
const authStore = useAuthStore()
const chatStore = useChatStore()

const inputMessage = ref('')
const streaming = ref(false)
const streamingContent = ref('')
const thinkingText = ref('')
const messageListRef = ref<HTMLElement>()

const activeSession = computed(() => chatStore.getActiveSession())
const isEmpty = computed(
  () => !activeSession.value || activeSession.value.messages.length === 0,
)

function renderMarkdown(content: string): string {
  return md.render(content)
}

function scrollToBottom() {
  nextTick(() => {
    if (messageListRef.value) {
      messageListRef.value.scrollTop = messageListRef.value.scrollHeight
    }
  })
}

watch(
  () => activeSession.value?.messages.length,
  () => scrollToBottom(),
)

function handleNewSession() {
  chatStore.createSession()
}

function handleQuickAction(text: string) {
  inputMessage.value = text
  handleSend()
}

async function handleSend() {
  const message = inputMessage.value.trim()
  if (!message || streaming.value) return

  const sessionId = chatStore.activeSessionId
  if (!sessionId) return

  chatStore.addMessage(sessionId, 'user', message)
  inputMessage.value = ''
  streaming.value = true
  streamingContent.value = ''
  thinkingText.value = ''

  let fullContent = ''
  let thinkingContent = ''

  try {
    const history = chatStore.getHistory(sessionId)
    for await (const event of streamChat({
      message,
      session_id: sessionId,
      user_id: authStore.username,
      history,
    })) {
      const { event_type, data } = event

      if (event_type === 'thinking') {
        thinkingContent += (data as Record<string, string>).chunk || ''
        thinkingText.value = thinkingContent
      } else if (event_type === 'message') {
        fullContent += (data as Record<string, string>).chunk || ''
        streamingContent.value = fullContent
      } else if (event_type === 'error') {
        fullContent += `\n\n❌ ${(data as Record<string, string>).error || '出错了'}`
        streamingContent.value = fullContent
      }
      scrollToBottom()
    }
  } catch {
    fullContent += '\n\n[连接中断，请重试]'
  }

  chatStore.addMessage(sessionId, 'assistant', fullContent, thinkingContent || undefined)
  streaming.value = false
  streamingContent.value = ''
  thinkingText.value = ''
  scrollToBottom()
}

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.chat-layout {
  display: flex;
  height: 100vh;
}

.sidebar {
  width: 260px;
  background: #f5f7fa;
  border-right: 1px solid #e4e7ed;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 16px;
}

.session-list {
  flex: 1;
  overflow-y: auto;
  padding: 0 8px;
}

.session-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 12px;
  border-radius: 6px;
  cursor: pointer;
  margin-bottom: 2px;
}

.session-item:hover {
  background: #e8eaed;
}

.session-item.active {
  background: #d9ecff;
}

.session-title {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 14px;
}

.delete-btn {
  opacity: 0;
  cursor: pointer;
}

.session-item:hover .delete-btn {
  opacity: 1;
}

.sidebar-footer {
  padding: 12px 16px;
  border-top: 1px solid #e4e7ed;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
  color: #606266;
}

.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #909399;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.empty-state h3 {
  font-size: 20px;
  color: #303133;
  margin-bottom: 8px;
}

.empty-state p {
  margin-bottom: 24px;
}

.quick-actions {
  display: flex;
  gap: 12px;
}

.message-item {
  margin-bottom: 20px;
  display: flex;
  gap: 12px;
}

.message-item.user {
  justify-content: flex-end;
}

.message-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}

.message-bubble {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 12px;
  line-height: 1.6;
  font-size: 14px;
}

.message-item.user .message-bubble {
  background: #409eff;
  color: white;
  border-bottom-right-radius: 4px;
}

.message-item.assistant .message-bubble {
  background: #f4f4f5;
  color: #303133;
  border-bottom-left-radius: 4px;
}

.thinking-block {
  margin-bottom: 8px;
  padding: 8px;
  background: #ecf5ff;
  border-radius: 6px;
  font-size: 12px;
  color: #909399;
}

.thinking-content {
  white-space: pre-wrap;
  margin-top: 4px;
}

.thinking-indicator {
  color: #909399;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.thinking-dot {
  width: 6px;
  height: 6px;
  background: #409eff;
  border-radius: 50%;
  animation: pulse 1s infinite;
}

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.5;
    transform: scale(0.8);
  }
}

.streaming-cursor::after {
  content: '▊';
  animation: blink 0.7s infinite;
}

@keyframes blink {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0;
  }
}

.input-area {
  padding: 16px 20px;
  border-top: 1px solid #e4e7ed;
  display: flex;
  gap: 12px;
  align-items: flex-end;
}

.input-area .el-textarea {
  flex: 1;
}
</style>
