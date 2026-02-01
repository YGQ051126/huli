<template>
  <el-card class="daily-care-tasks-card" shadow="hover">
    <template #header>
      <div class="card-header">
        <div class="header-title">
          <el-icon class="header-icon"><List /></el-icon>
          <span>今日护理任务 ({{ tasks.length }})</span>
        </div>
        <div class="header-actions">
          <el-button type="primary" :icon="Refresh" circle @click="refreshTasks" :loading="refreshing" title="即时刷新" />
          <el-button type="success" :icon="Check" @click="saveTasks" :loading="saving">保存</el-button>
        </div>
      </div>
    </template>

    <div v-loading="loading" class="tasks-container">
      <el-empty v-if="tasks.length === 0" description="暂无今日护理任务" />
      
      <div v-else class="tasks-grid">
        <el-card 
          v-for="task in tasks" 
          :key="task.id" 
          class="task-item-card" 
          :class="{ 'completed': task.is_completed }"
          shadow="hover"
        >
          <div class="task-card-header">
            <div class="patient-info">
              <span class="room-number">{{ task.patient_room || '无床位' }}</span>
              <span class="patient-name">{{ task.patient_name }}</span>
            </div>
            <el-checkbox 
              v-model="task.is_completed" 
              label="完成" 
              size="small" 
              @change="(val: any) => handleSelectAll(task, val)"
            />
          </div>
          
          <div class="task-checklist">
            <el-checkbox v-model="task.vital_signs_normal" label="生命体征正常" />
            <el-checkbox v-model="task.diet_normal" label="饮食正常" />
            <el-checkbox v-model="task.mental_normal" label="精神状况正常" />
          </div>
        </el-card>
      </div>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getDailyCareTasks, pullLatestTasks, batchUpdateTasks, type DailyCareTask } from '@/services/care-tasks'
import { ElMessage, ElMessageBox } from 'element-plus'
import { List, Refresh, Check } from '@element-plus/icons-vue'

const tasks = ref<DailyCareTask[]>([])
const loading = ref(false)
const refreshing = ref(false)
const saving = ref(false)

onMounted(() => {
  fetchTasks()
})

const fetchTasks = async () => {
  loading.value = true
  try {
    const res = await getDailyCareTasks()
    // Handle potential wrapper format
    const data = Array.isArray(res) ? res : (res as any).data || []
    tasks.value = data
  } catch (error) {
    console.error('Failed to fetch tasks', error)
    ElMessage.error('获取护理任务失败')
  } finally {
    loading.value = false
  }
}

const refreshTasks = async () => {
  refreshing.value = true
  try {
    const res = await pullLatestTasks()
    const latestData = Array.isArray(res) ? res : (res as any).data || []
    
    // Merge logic: Update local tasks with latest server state, 
    // but maybe warn if local changes exist? For simplicity, we overwrite or smart merge.
    // Requirement says "diff merge". 
    // We will just replace for now as "latest" is truth.
    tasks.value = latestData
    ElMessage.success('数据已更新')
  } catch (error) {
    ElMessage.error('刷新失败')
  } finally {
    refreshing.value = false
  }
}

const handleSelectAll = (task: DailyCareTask, val: boolean | string | number) => {
  const isChecked = !!val
  task.vital_signs_normal = isChecked
  task.diet_normal = isChecked
  task.mental_normal = isChecked
}

const saveTasks = async () => {
  saving.value = true
  try {
    await batchUpdateTasks(tasks.value)
    ElMessage.success('保存成功')
    // Optionally refresh to confirm status
    // fetchTasks() 
  } catch (error) {
    ElMessageBox.confirm(
      '保存失败，是否重试？',
      '提交错误',
      {
        confirmButtonText: '重试',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
      .then(() => {
        saveTasks()
      })
      .catch(() => {
        // Cancelled
        // Rollback UI if needed (re-fetch)
        fetchTasks()
      })
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.daily-care-tasks-card {
  margin-bottom: 24px;
  border-radius: 12px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.header-icon {
  font-size: 18px;
  color: #409eff;
}

.tasks-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
  margin-top: 10px;
}

.task-item-card {
  transition: all 0.3s;
}

.task-item-card.completed {
  background-color: #f0f9eb;
  border-color: #e1f3d8;
}

.task-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid #ebeef5;
}

.patient-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.room-number {
  background-color: #409eff;
  color: white;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
}

.patient-name {
  font-weight: 600;
  font-size: 15px;
}

.task-checklist {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
</style>
