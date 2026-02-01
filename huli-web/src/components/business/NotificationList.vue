<template>
  <el-card class="notification-list">
    <template #header>
      <div class="header">
        <span>消息通知中心</span>
        <div class="toolbar">
          <el-tag v-if="unreadCount && unreadCount > 0" type="danger" effect="dark">
            未读 {{ unreadCount }}
          </el-tag>
          <el-button size="small" @click="$emit('refresh')">刷新</el-button>
          <el-button size="small" type="text" @click="$emit('clear')">全部已读</el-button>
        </div>
      </div>
    </template>

    <el-skeleton v-if="loading" :rows="4" animated />
    <el-empty v-else-if="!notifications.length" description="暂无通知" />
    <el-timeline v-else>
      <el-timeline-item
        v-for="item in notifications"
        :key="item.id"
        :type="item.status === 'unread' ? 'danger' : 'info'"
        :timestamp="formatTime(item.created_at)"
      >
        <div class="item" @click="$emit('read', item.id)">
          <div class="title">
            <el-tag :type="typeTag(item.type)" size="small" effect="plain">
              {{ typeText(item.type) }}
            </el-tag>
            <span class="text">{{ item.title }}</span>
          </div>
          <div class="content">
            {{ item.content }}
          </div>
        </div>
      </el-timeline-item>
    </el-timeline>
  </el-card>
</template>

<script setup lang="ts">
import dayjs from 'dayjs'
import type { Notification } from '@/types/message'

defineProps<{
  notifications: readonly Notification[]
  loading?: boolean
  unreadCount?: number
}>()

defineEmits<{
  (e: 'refresh'): void
  (e: 'clear'): void
  (e: 'read', id: string): void
}>()

const formatTime = (value: string) => dayjs(value).format('MM-DD HH:mm')

const typeText = (type: Notification['type']) => {
  const map = {
    system: '系统',
    service: '服务提醒',
    health: '健康告警',
    payment: '缴费提醒'
  } as const
  return map[type] || type
}

const typeTag = (type: Notification['type']) => {
  const map = {
    system: 'info',
    service: 'warning',
    health: 'danger',
    payment: 'success'
  } as const
  return map[type] || 'info'
}
</script>

<style scoped>
.notification-list :deep(.el-card__header) {
  padding: 12px 16px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.toolbar {
  display: flex;
  gap: 8px;
  align-items: center;
}

.item {
  cursor: pointer;
}

.title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.title .text {
  font-weight: 600;
}

.content {
  font-size: 13px;
  color: #666;
}
</style>
