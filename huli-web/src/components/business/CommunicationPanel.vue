<template>
  <el-card class="communication-panel" :body-style="{ padding: '0', display: 'flex', flexDirection: 'column', height: '100%' }">
    <template #header>
      <div class="header">
        <span class="title">即时通讯</span>
        <div class="status-dot"></div>
      </div>
    </template>

    <div class="messages-container" v-loading="loading" ref="messagesContainer">
      <el-empty v-if="!messages.length && !loading" description="暂无消息记录" :image-size="120" />
      
      <transition-group name="message-list" tag="div" class="message-list-wrapper">
        <div
          v-for="msg in messages"
          :key="msg.id"
          class="message-row"
          :class="isOutgoing(msg) ? 'outgoing' : 'incoming'"
        >
          <el-avatar 
            class="avatar" 
            :size="40" 
            :src="msg.sender_avatar"
            :style="{ backgroundColor: isOutgoing(msg) ? '#409EFF' : '#909399' }"
          >
            {{ (msg.sender_name || 'U').charAt(0).toUpperCase() }}
          </el-avatar>
          
          <div class="message-content">
            <div class="meta">
              <span class="name">{{ msg.sender_name || '未知用户' }}</span>
              <span class="time">{{ formatTime(msg.created_at) }}</span>
            </div>
            <div class="bubble">
              {{ msg.content }}
            </div>
          </div>
        </div>
      </transition-group>
    </div>

    <div class="input-area">
      <el-input
        v-model="content"
        type="textarea"
        :rows="3"
        placeholder="输入消息..."
        resize="none"
        class="custom-textarea"
        @keydown.enter.prevent="handleSend"
      />
      <div class="actions">
        <el-button type="primary" :loading="sending" @click="handleSend" round>发送</el-button>
      </div>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'
import type { Message, CreateMessageData } from '@/services/messages'
import { useUserStore } from '@/stores/user'

const props = defineProps<{
  messages: Message[]
  loading?: boolean
  receiverId: string
}>()

const emit = defineEmits<{
  (e: 'send', data: CreateMessageData): void
}>()

const userStore = useUserStore()
const content = ref('')
const sending = ref(false)
const messagesContainer = ref<HTMLElement | null>(null)

const isOutgoing = (msg: Message) => {
  return msg.sender === userStore.user?.id
}

const formatTime = (timeStr?: string) => {
  if (!timeStr) return ''
  const date = new Date(timeStr)
  return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

// Auto scroll to bottom when messages change
watch(() => props.messages, () => {
  scrollToBottom()
}, { deep: true })

function scrollToBottom() {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

async function handleSend() {
  if (!content.value.trim()) return
  sending.value = true
  try {
    const payload: CreateMessageData = {
      receiver: Number(props.receiverId),
      content: content.value.trim(),
      type: 'text'
    }
    emit('send', payload)
    content.value = ''
  } finally {
    sending.value = false
  }
}
</script>

<style scoped>
.communication-panel {
  border: none;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  height: 700px; /* Fixed height for better scrolling */
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
}

.header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.title {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
}

.status-dot {
  width: 8px;
  height: 8px;
  background-color: #67C23A;
  border-radius: 50%;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 16px 24px 80px; /* Bottom padding for scroll space */
  background-color: #F5F7FA;
  scroll-behavior: smooth;
}

.message-list-wrapper {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.message-row {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  opacity: 1;
}

.message-row.outgoing {
  flex-direction: row-reverse;
}

.avatar {
  flex-shrink: 0;
  font-size: 14px;
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.message-content {
  display: flex;
  flex-direction: column;
  max-width: 70%;
}

.message-row.outgoing .message-content {
  align-items: flex-end;
}

.meta {
  margin-bottom: 4px;
  font-size: 12px;
  color: #909399;
  display: flex;
  gap: 8px;
}

.bubble {
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.6;
  position: relative;
  word-break: break-word;
  box-shadow: 0 1px 4px rgba(0,0,0,0.05);
  transition: all 0.2s ease-out;
}

.message-row.incoming .bubble {
  background-color: #ffffff;
  color: #303133;
  border-top-left-radius: 2px;
}

.message-row.outgoing .bubble {
  background-color: #409EFF;
  color: #ffffff;
  border-top-right-radius: 2px;
}

.input-area {
  padding: 16px 24px;
  background-color: #ffffff;
  border-top: 1px solid #EBEEF5;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.actions {
  display: flex;
  justify-content: flex-end;
}

/* Animations */
.message-list-enter-active {
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.5, 1);
  animation: flash 0.6s ease-out;
}

.message-list-enter-from {
  opacity: 0;
  transform: translateY(20px);
  max-height: 0;
}

.message-list-enter-to {
  opacity: 1;
  transform: translateY(0);
  max-height: 500px; /* Approximate max height for a single message */
}

@keyframes flash {
  0% { background-color: rgba(255, 249, 196, 0.8); }
  100% { background-color: transparent; }
}

/* Scrollbar Styling */
.messages-container::-webkit-scrollbar {
  width: 6px;
}
.messages-container::-webkit-scrollbar-thumb {
  background-color: #DCDFE6;
  border-radius: 3px;
}
.messages-container::-webkit-scrollbar-track {
  background-color: transparent;
}
</style>
