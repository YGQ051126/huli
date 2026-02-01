<template>
  <el-dialog
    v-model="visible"
    :title="announcement?.title || '公告详情'"
    width="600px"
    :before-close="handleClose"
  >
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="8" animated />
    </div>
    <div v-else-if="announcement" class="announcement-detail">
      <div class="detail-header">
        <div class="meta">
          <span class="publish-time">发布时间：{{ formatTime(announcement.publish_time) }}</span>
          <el-tag :type="getStatusTagType(announcement.status)">
            {{ getStatusText(announcement.status) }}
          </el-tag>
        </div>
      </div>
      <div class="detail-content" v-html="announcement.content"></div>
    </div>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleClose">关闭</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import dayjs from 'dayjs'
import type { Announcement } from '@/types/announcement'
import { getAnnouncementById } from '@/services/announcements'

const props = defineProps<{
  modelValue: boolean
  announcementId: string | number | null
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  'read': [id: string | number]
}>()

const visible = ref(props.modelValue)
const loading = ref(false)
const announcement = ref<Announcement | null>(null)

// 监听props变化
watch(() => props.modelValue, (newValue) => {
  visible.value = newValue
})

watch(() => props.announcementId, (newId) => {
  if (newId && visible.value) {
    fetchAnnouncement(newId)
  }
})

watch(() => visible.value, (newVisible) => {
  emit('update:modelValue', newVisible)
  if (newVisible && props.announcementId) {
    fetchAnnouncement(props.announcementId)
  }
})

// 获取公告详情
const fetchAnnouncement = async (id: string | number) => {
  loading.value = true
  try {
    announcement.value = await getAnnouncementById(id)
  } catch (error) {
    console.error('获取公告详情失败:', error)
  } finally {
    loading.value = false
  }
}

// 格式化时间
const formatTime = (value: string) => dayjs(value).format('YYYY-MM-DD HH:mm:ss')

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

// 关闭对话框
const handleClose = () => {
  visible.value = false
  emit('update:modelValue', false)
}



// 初始化
onMounted(() => {
  if (props.announcementId && visible.value) {
    fetchAnnouncement(props.announcementId)
  }
})
</script>

<style scoped>
.loading-container {
  padding: 20px 0;
}

.announcement-detail {
  padding: 20px 0;
}

.detail-header {
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #e4e7ed;
}

.meta {
  display: flex;
  align-items: center;
  gap: 16px;
}

.publish-time {
  font-size: 14px;
  color: #909399;
}

.detail-content {
  font-size: 15px;
  line-height: 1.8;
  color: #303133;
  white-space: pre-wrap;
  word-break: break-word;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}
</style>