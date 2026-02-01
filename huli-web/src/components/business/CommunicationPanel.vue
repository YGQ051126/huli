<template>
  <el-card class="communication-panel">
    <template #header>
      <div class="header">
        <span>即时通讯</span>
      </div>
    </template>

    <div class="messages" v-loading="loading" ref="messagesContainer">
      <el-empty v-if="!messages.length && !loading" description="暂无消息记录" />
      <div
        v-for="msg in messages"
        :key="msg.id"
        class="message-item"
        :class="isOutgoing(msg) ? 'outgoing' : 'incoming'"
      >
        <div class="meta">
          <span class="name">{{ msg.sender_name || '未知用户' }}</span>
          <span class="time">{{ msg.created_at }}</span>
        </div>
        <div class="bubble">
          {{ msg.content }}
        </div>
      </div>
    </div>

    <div class="input-bar">
      <el-input
        v-model="content"
        type="textarea"
        :rows="2"
        placeholder="请输入消息内容..."
      />
      <div class="actions">
        <el-button type="primary" :loading="sending" @click="handleSend">发送</el-button>
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
.messages {
  max-height: 260px;
  overflow-y: auto;
  padding: 8px;
}
</style>
