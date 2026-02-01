<template>
  <div class="staff-dashboard">
    <div class="dashboard-header">
      <div class="header-content">
        <h2>工作台</h2>
        <p class="subtitle">欢迎回来，祝您今天工作愉快！</p>
      </div>
      <el-button type="primary" circle :icon="Refresh" @click="fetch" :loading="loading" />
    </div>

    <div class="dashboard-grid">
      <!-- 左侧主内容区 -->
      <div class="main-column">
        <!-- 告警信息 -->
        <transition name="el-zoom-in-top">
          <el-card v-if="alerts.length > 0" class="dashboard-card alert-card" shadow="hover">
            <template #header>
              <div class="card-header-wrapper danger">
                <el-icon class="header-icon"><BellFilled /></el-icon>
                <span>重要提醒</span>
                <el-tag type="danger" effect="dark" round size="small" class="count-tag">{{ alerts.length }}</el-tag>
              </div>
            </template>
            <div class="alert-list">
              <div v-for="alert in alerts" :key="alert.id" class="alert-item">
                <div class="alert-icon-wrapper">
                  <el-icon><Warning /></el-icon>
                </div>
                <div class="alert-content-wrapper">
                  <div class="alert-type">{{ alert.type }}</div>
                  <div class="alert-text">{{ alert.content }}</div>
                </div>
              </div>
            </div>
          </el-card>
        </transition>

        <!-- 个性化服务任务 -->
        <div class="service-task-section" style="margin-bottom: 24px;">
           <el-card class="dashboard-card" shadow="hover">
             <template #header>
               <div class="card-header-wrapper primary">
                 <el-icon class="header-icon"><Service /></el-icon>
                 <span>个性化服务任务</span>
                 <el-tag type="primary" effect="plain" round size="small" class="count-tag">{{ serviceTasks.length }}</el-tag>
               </div>
             </template>
             <div v-if="serviceTasks.length > 0" class="service-task-list">
               <el-card v-for="task in serviceTasks" :key="task.id" class="service-task-item" shadow="never">
                 <div class="task-header">
                   <span class="patient-name">{{ task.patient_name }}</span>
                   <el-tag size="small" :type="task.status === 'processing' ? 'success' : 'warning'">
                     {{ task.status === 'processing' ? '进行中' : '待处理' }}
                   </el-tag>
                 </div>
                 <div class="task-content">
                   <el-tag v-for="item in task.items" :key="item.id" size="small" class="service-tag">
                     {{ item.service_name }}
                   </el-tag>
                 </div>
                 <div class="task-footer">
                   <span class="time">{{ formatDate(task.paid_at) }}</span>
                   <el-button type="primary" size="small" @click="handleProcess(task)">处理/反馈</el-button>
                 </div>
               </el-card>
             </div>
             <el-empty v-else description="暂无个性化服务任务" :image-size="60"></el-empty>
           </el-card>
        </div>

        <!-- Daily Care Tasks Component -->
        <DailyCareTasks />
      </div>

      <!-- 右侧侧边栏 -->
      <div class="side-column">
        <!-- 快捷概览 -->
        <el-card class="dashboard-card stats-card" shadow="hover">
          <template #header>
            <div class="card-header-wrapper">
              <el-icon class="header-icon"><DataBoard /></el-icon>
              <span>工作概览</span>
            </div>
          </template>
          <div class="stats-grid">
            <div class="stat-item pending">
              <div class="stat-icon">
                <el-icon><Timer /></el-icon>
              </div>
              <div class="stat-info">
                <span class="stat-value">{{ stats.pending }}</span>
                <span class="stat-label">待处理</span>
              </div>
            </div>
            <div class="stat-item progress">
              <div class="stat-icon">
                <el-icon><VideoPlay /></el-icon>
              </div>
              <div class="stat-info">
                <span class="stat-value">{{ stats.inProgress }}</span>
                <span class="stat-label">进行中</span>
              </div>
            </div>
            <div class="stat-item completed">
              <div class="stat-icon">
                <el-icon><CircleCheckFilled /></el-icon>
              </div>
              <div class="stat-info">
                <span class="stat-value">{{ stats.completed }}</span>
                <span class="stat-label">已完成</span>
              </div>
            </div>
          </div>
        </el-card>

        <!-- 生日提醒 -->
        <el-card class="dashboard-card birthday-card" shadow="hover">
          <template #header>
            <div class="card-header-wrapper primary">
              <el-icon class="header-icon"><Present /></el-icon>
              <span>院民生日</span>
            </div>
          </template>
          
          <div v-if="birthdays.length > 0" class="birthday-list">
            <div v-for="p in birthdays" :key="p.id" class="birthday-item">
              <div class="cake-icon">
                <el-icon><Present /></el-icon>
              </div>
              <div class="birthday-info">
                <div class="patient-name">{{ p.name }}</div>
                <div class="patient-detail">{{ p.age }}岁 ・ {{ p.room || '未分配房间' }}</div>
              </div>
              <el-tag type="warning" effect="plain" size="small" round>Today</el-tag>
            </div>
          </div>
          <el-empty v-else description="今天没有寿星哦" :image-size="80">
            <template #image>
              <el-icon :size="60" color="#e0e0e0"><Calendar /></el-icon>
            </template>
          </el-empty>
        </el-card>
      </div>
    </div>

    <!-- Feedback Dialog -->
    <el-dialog v-model="showFeedbackDialog" title="服务反馈" width="500px">
      <el-form label-width="80px">
        <el-form-item label="执行情况">
          <el-input v-model="feedbackContent" type="textarea" rows="4" placeholder="请输入服务完成情况..." />
        </el-form-item>
        <el-form-item label="现场照片">
          <el-upload
            action="#"
            list-type="picture-card"
            :auto-upload="false"
            :on-change="handleFileChange"
            :on-remove="handleFileRemove"
            :file-list="fileList"
            multiple
          >
            <el-icon><Plus /></el-icon>
          </el-upload>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showFeedbackDialog = false">取消</el-button>
          <el-button type="primary" :loading="submittingFeedback" @click="submitFeedback">提交反馈</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
 import { onMounted, ref, computed } from 'vue'
import DailyCareTasks from '@/components/business/DailyCareTasks.vue'
import { getDashboardData } from '@/services/tasks'
import { getServiceOrders, processServiceOrder, submitServiceFeedback, type ServiceOrder } from '@/services/services'
import { 
  BellFilled, Warning, DataBoard, Timer, VideoPlay, 
  CircleCheckFilled, Present, Calendar, Refresh, Service, Plus
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const dashboardLoading = ref(false)
const loading = computed(() => dashboardLoading.value)

const alerts = ref<any[]>([])
const birthdays = ref<any[]>([])
const serviceTasks = ref<ServiceOrder[]>([])

const showFeedbackDialog = ref(false)
const submittingFeedback = ref(false)
const currentOrder = ref<ServiceOrder | null>(null)
const feedbackContent = ref('')
const fileList = ref<any[]>([])

const stats = computed(() => {
  // const all = tasks.value // Legacy tasks removed
  // TODO: Add DailyCareTask stats if needed, or just use serviceTasks for now + pending from API
  return {
    pending: serviceTasks.value.filter((t: any) => t.status === 'pending').length,
    inProgress: serviceTasks.value.filter((t: any) => t.status === 'processing').length,
    completed: serviceTasks.value.filter((t: any) => t.status === 'completed').length
  }
})

onMounted(() => {
  fetch()
})

async function fetch() {
  dashboardLoading.value = true
  try {
    const data = await getDashboardData()
    if (data.tasks) {
      // Legacy tasks logic removed
      // tasksStore.list = data.tasks
    } else {
      // tasksStore.fetchTasks()
    }
    
    alerts.value = data.alerts || []
    birthdays.value = data.birthdays || []

    // Fetch Service Tasks
    try {
      const ordersRes = await getServiceOrders()
      console.log('Orders response:', ordersRes)
      const orders = Array.isArray(ordersRes) ? ordersRes : (ordersRes as any).results || []
      // Filter for staff: pending or processing
      serviceTasks.value = orders.filter((o: ServiceOrder) => ['pending', 'processing'].includes(o.status))
      console.log('Filtered Service Tasks:', serviceTasks.value)
    } catch (e) {
      console.error('Fetch service orders failed:', e)
    }

  } catch (error: any) {
    console.error('Fetch dashboard data failed:', error)
    if (error.message && error.message.includes('Not a staff user')) {
       alerts.value = []
       birthdays.value = []
    }
  } finally {
    dashboardLoading.value = false
  }
}

// Service Task Actions
const handleProcess = async (order: ServiceOrder) => {
  currentOrder.value = order
  // If pending, mark as processing first (optional, or just go straight to feedback)
  if (order.status === 'pending') {
    try {
      await processServiceOrder(order.id)
      order.status = 'processing' // Optimistic update
    } catch (e) {
      console.error(e)
    }
  }
  feedbackContent.value = ''
  fileList.value = []
  showFeedbackDialog.value = true
}

const handleFileChange = (file: any) => {
  fileList.value.push(file)
}
const handleFileRemove = (file: any) => {
  const index = fileList.value.indexOf(file)
  if (index !== -1) fileList.value.splice(index, 1)
}

const submitFeedback = async () => {
  if (!currentOrder.value) return
  if (!feedbackContent.value) {
    ElMessage.warning('请输入反馈内容')
    return
  }

  submittingFeedback.value = true
  try {
    const formData = new FormData()
    formData.append('content', feedbackContent.value)
    fileList.value.forEach(f => {
      formData.append('images', f.raw) // f.raw is the File object
    })

    await submitServiceFeedback(currentOrder.value.id, formData)
    ElMessage.success('反馈提交成功')
    showFeedbackDialog.value = false
    fetch() // Refresh list
  } catch (error) {
    console.error(error)
    ElMessage.error('提交失败')
  } finally {
    submittingFeedback.value = false
  }
}

const formatDate = (dateStr: string) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleString()
}
</script>

<style scoped>
.staff-dashboard {
  padding: 24px;
  max-width: 1600px;
  margin: 0 auto;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.dashboard-header h2 {
  margin: 0;
  font-size: 24px;
  color: #303133;
  font-weight: 600;
}

.subtitle {
  margin: 8px 0 0;
  color: #909399;
  font-size: 14px;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
}

/* Card Common Styles */
.dashboard-card {
  border: none;
  border-radius: 12px;
  transition: all 0.3s ease;
  overflow: hidden;
}

.dashboard-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

.card-header-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
}

.card-header-wrapper.danger { color: #f56c6c; }
.card-header-wrapper.primary { color: #409eff; }

.header-icon {
  font-size: 18px;
}

/* Alert Card */
.alert-card {
  margin-bottom: 24px;
  border-left: 4px solid #f56c6c;
}

.alert-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.alert-item {
  display: flex;
  align-items: flex-start;
  padding: 12px;
  background-color: #fef0f0;
  border-radius: 8px;
  gap: 12px;
}

.alert-icon-wrapper {
  color: #f56c6c;
  font-size: 20px;
  margin-top: 2px;
}

.alert-type {
  font-size: 12px;
  font-weight: bold;
  color: #f56c6c;
  margin-bottom: 4px;
}

.alert-text {
  font-size: 14px;
  color: #606266;
  line-height: 1.4;
}

/* Stats Card */
.stats-card {
  margin-bottom: 24px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16px 8px;
  border-radius: 8px;
  background-color: #f5f7fa;
  transition: background-color 0.2s;
}

.stat-item:hover {
  background-color: #ecf5ff;
}

.stat-icon {
  font-size: 24px;
  margin-bottom: 8px;
}

.stat-item.pending .stat-icon { color: #e6a23c; }
.stat-item.progress .stat-icon { color: #409eff; }
.stat-item.completed .stat-icon { color: #67c23a; }

.stat-value {
  font-size: 20px;
  font-weight: bold;
  color: #303133;
  line-height: 1.2;
}

.stat-label {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

/* Birthday Card */
.birthday-card {
  border-top: 4px solid #e6a23c;
}

.birthday-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.birthday-item {
  display: flex;
  align-items: center;
  padding: 12px;
  background: linear-gradient(to right, #fffbf0, #fff);
  border-radius: 8px;
  border: 1px solid #faecd8;
}

.cake-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #fdf6ec;
  color: #e6a23c;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  margin-right: 12px;
}

.birthday-info {
  flex: 1;
}

.patient-name {
  font-weight: 600;
  color: #303133;
  font-size: 15px;
}

.patient-detail {
  font-size: 12px;
  color: #909399;
  margin-top: 2px;
}

/* Service Tasks */
.service-task-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

.service-task-item {
  border: 1px solid #ebeef5;
}

.task-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.task-content {
  margin-bottom: 10px;
  height: 40px;
  overflow: hidden;
}

.service-tag {
  margin-right: 4px;
  margin-bottom: 4px;
}

.task-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: #909399;
}

@media (max-width: 1200px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
</style>
