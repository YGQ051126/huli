<template>
  <el-card class="task-list">
    <template #header>
      <div class="header">
        <span>{{ title }}</span>
        <div class="toolbar">
          <el-tag type="info" effect="plain">共 {{ tasks.length }} 条</el-tag>
          <el-button size="small" :loading="loading" @click="$emit('refresh')">刷新</el-button>
        </div>
      </div>
    </template>

    <el-table :data="tasks" size="small" v-loading="loading" empty-text="暂无任务">
      <el-table-column prop="taskType" label="任务类型" min-width="120" />
      <el-table-column prop="description" label="说明" min-width="200" show-overflow-tooltip />
      <el-table-column prop="scheduledTime" label="计划时间" min-width="160">
        <template #default="scope">
          {{ formatTime(scope.row.scheduledTime) }}
        </template>
      </el-table-column>
      <el-table-column prop="priority" label="优先级" width="100">
        <template #default="scope">
          <el-tag :type="priorityType(scope.row.priority)" size="small">
            {{ priorityText(scope.row.priority) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="120">
        <template #default="scope">
          <el-tag :type="statusTag(scope.row.status)" size="small">
            {{ statusText(scope.row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="scope">
          <el-button size="small" type="success" :disabled="scope.row.status === 'completed'" @click="$emit('complete', scope.row.id)">
            完成
          </el-button>
          <el-button size="small" @click="$emit('delay', scope.row.id)">延迟</el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

<script setup lang="ts">
import dayjs from 'dayjs'
import type { CareTask } from '@/types/task'

const props = defineProps<{
  tasks: readonly CareTask[]
  loading?: boolean
  title?: string
}>()

defineEmits<{
  (e: 'refresh'): void
  (e: 'complete', id: string): void
  (e: 'delay', id: string): void
}>()

const title = props.title ?? '今日任务'

const formatTime = (value: string) => dayjs(value).format('MM-DD HH:mm')

const priorityText = (value: CareTask['priority']) => {
  const map = { low: '低', medium: '中', high: '高' }
  return map[value] ?? value
}

const priorityType = (value: CareTask['priority']) => {
  const map = { low: 'info', medium: 'warning', high: 'danger' } as const
  return map[value] || 'info'
}

const statusText = (value: CareTask['status']) => {
  const map = {
    pending: '待执行',
    in_progress: '进行中',
    completed: '已完成',
    delayed: '已延迟',
    cancelled: '已取消'
  }
  return map[value] ?? value
}

const statusTag = (value: CareTask['status']) => {
  const map = {
    pending: 'info',
    in_progress: 'warning',
    completed: 'success',
    delayed: 'danger',
    cancelled: 'default'
  } as const
  return map[value] || 'info'
}
</script>

<style scoped>
.task-list :deep(.el-card__header) {
  padding: 12px 16px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
}

.toolbar {
  display: flex;
  gap: 8px;
  align-items: center;
}
</style>


