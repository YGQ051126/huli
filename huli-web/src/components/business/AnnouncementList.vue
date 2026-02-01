<template>
  <el-card class="announcement-list">
    <template #header>
      <div class="header">
        <span>公告中心</span>
        <div class="toolbar">
          <el-button size="small" @click="$emit('refresh')">刷新</el-button>
        </div>
      </div>
    </template>

    <el-skeleton v-if="props.loading" :rows="4" animated />
    <el-empty v-else-if="!props.announcements.length" description="暂无公告" />
    <div v-else class="announcements">
      <div
        v-for="announcement in props.announcements"
        :key="announcement.id"
        class="announcement-item"
        @click="$emit('read', announcement.id)"
      >
        <div class="item-header">
          <div class="title">
            <span class="text">{{ announcement.title }}</span>
          </div>
          <div class="meta">
            <span class="publish-time">{{ formatTime(announcement.publish_time) }}</span>
            <el-tag :type="getStatusTagType(announcement.status)" size="small">
              {{ getStatusText(announcement.status) }}
            </el-tag>
          </div>
        </div>
        <div class="content">
          {{ truncateContent(announcement.content) }}
        </div>
      </div>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import dayjs from 'dayjs'
import type { Announcement } from '@/types/announcement'

const props = defineProps<{
  announcements: readonly Announcement[]
  loading?: boolean
}>()

// 调试日志
console.log('公告列表组件props:', {
  announcementsLength: props.announcements.length,
  loading: props.loading
})

const emit = defineEmits<{
  (e: 'refresh'): void
  (e: 'read', id: string | number): void
}>()

// 格式化时间
const formatTime = (value: string) => dayjs(value).format('YYYY-MM-DD HH:mm')

// 获取状态文本
const getStatusText = (status: Announcement['status']) => {
  const map = {
    published: '已发布',
    draft: '草稿',
    retracted: '已撤回'
  } as const
  return map[status] || status
}

// 获取状态标签类型
const getStatusTagType = (status: Announcement['status']) => {
  const map = {
    published: 'success',
    draft: 'warning',
    retracted: 'info'
  } as const
  return map[status] || 'info'
}

// 截断内容
const truncateContent = (content: string, maxLength = 100) => {
  if (content.length <= maxLength) return content
  return content.substring(0, maxLength) + '...'
}
</script>

<style scoped>
.announcement-list :deep(.el-card__header) {
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

.announcements {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.announcement-item {
  padding: 16px;
  border-radius: 8px;
  background-color: #fafafa;
  transition: all 0.3s ease;
  cursor: pointer;
  border-left: 3px solid transparent;
}

.announcement-item:hover {
  background-color: #f0f2f5;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.announcement-item.unread {
  background-color: #f0f9ff;
  border-left-color: #409eff;
  font-weight: 500;
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
  flex-wrap: wrap;
  gap: 8px;
}

.title {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
  min-width: 0;
}

.title .text {
  font-weight: 600;
  font-size: 16px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
}

.meta {
  display: flex;
  align-items: center;
  gap: 8px;
}

.publish-time {
  font-size: 13px;
  color: #909399;
}

.content {
  font-size: 14px;
  color: #606266;
  line-height: 1.6;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-clamp: 2; /* 添加标准属性以兼容现代浏览器 */
}
</style>