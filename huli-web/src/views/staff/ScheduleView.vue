<template>
  <div class="schedule-view">
    <el-tabs v-model="activeTab" class="schedule-tabs">
      <el-tab-pane label="工作日程" name="schedule">
        <el-empty description="暂未集成排班接口" />
      </el-tab-pane>
      
      <el-tab-pane label="请假管理" name="leave">
        <div class="leave-content">
          <div class="page-header">
            <div class="header-left">
              <h2 class="section-title">我的请假申请</h2>
            </div>
            <div class="header-right">
              <el-button type="primary" :icon="Plus" @click="showApplyDialog">申请请假</el-button>
            </div>
          </div>
          
          <el-table :data="leaveRequests" v-loading="loading" stripe border style="width: 100%">
            <el-table-column prop="type" label="请假类型" width="120">
              <template #default="scope">
                <el-tag :type="getLeaveTypeTag(scope.row.type)">
                  {{ getLeaveTypeLabel(scope.row.type) }}
                </el-tag>
              </template>
            </el-table-column>
            
            <el-table-column prop="start_date" label="开始日期" width="120" sortable />
            <el-table-column prop="end_date" label="结束日期" width="120" sortable />
            
            <el-table-column label="天数" width="80">
              <template #default="scope">
                {{ calculateDays(scope.row.start_date, scope.row.end_date) }}天
              </template>
            </el-table-column>
            
            <el-table-column prop="reason" label="请假原因" min-width="200" show-overflow-tooltip />
            
            <el-table-column prop="status" label="状态" width="100">
              <template #default="scope">
                <el-tag :type="getStatusType(scope.row.status)">
                  {{ getStatusLabel(scope.row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            
            <el-table-column label="审批意见" min-width="150" show-overflow-tooltip>
              <template #default="scope">
                <span v-if="scope.row.rejection_reason" class="text-danger">{{ scope.row.rejection_reason }}</span>
                <span v-else-if="scope.row.status === 'approved'" class="text-success">已批准</span>
                <span v-else>-</span>
              </template>
            </el-table-column>
            
            <el-table-column prop="created_at" label="申请时间" width="160" sortable>
              <template #default="scope">
                {{ formatDate(scope.row.created_at) }}
              </template>
            </el-table-column>
            
             <el-table-column label="操作" width="100" fixed="right">
              <template #default="scope">
                <el-button 
                  v-if="scope.row.status === 'pending'"
                  type="danger" 
                  link
                  size="small"
                  @click="handleCancel(scope.row)"
                >
                  撤销
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-tab-pane>
    </el-tabs>

    <!-- 申请请假对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="申请请假"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="请假类型" prop="type">
          <el-select v-model="form.type" placeholder="请选择请假类型" style="width: 100%">
            <el-option label="病假" value="sick" />
            <el-option label="事假" value="casual" /> <!-- Backend uses 'casual' but frontend label '事假' -->
            <el-option label="年假" value="annual" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="起止日期" prop="dateRange">
          <el-date-picker
            v-model="form.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="YYYY-MM-DD"
            style="width: 100%"
            :disabled-date="disabledDate"
          />
        </el-form-item>
        
        <el-form-item label="请假原因" prop="reason">
          <el-input
            v-model="form.reason"
            type="textarea"
            :rows="3"
            placeholder="请输入请假原因"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm" :loading="submitting">
            提交
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox, type FormInstance } from 'element-plus'
import { getLeaveRequests, createLeaveRequest, cancelLeaveRequest, type LeaveRequest } from '@/services/staff/leave'
import dayjs from 'dayjs'

const activeTab = ref('leave') // Default to leave tab for this task
const loading = ref(false)
const leaveRequests = ref<LeaveRequest[]>([])
const dialogVisible = ref(false)
const submitting = ref(false)
const formRef = ref<FormInstance>()

const form = reactive({
  type: '',
  dateRange: [] as string[],
  reason: ''
})

const rules = {
  type: [{ required: true, message: '请选择请假类型', trigger: 'change' }],
  dateRange: [{ required: true, message: '请选择起止日期', trigger: 'change' }],
  reason: [{ required: true, message: '请输入请假原因', trigger: 'blur' }]
}

const fetchRequests = async () => {
  loading.value = true
  try {
    const res = await getLeaveRequests()
    // Ensure array
    const data = Array.isArray(res) ? res : (res as any).results || []
    leaveRequests.value = data
  } catch (error) {
    ElMessage.error('获取请假记录失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchRequests()
})

const showApplyDialog = () => {
  form.type = ''
  form.dateRange = []
  form.reason = ''
  dialogVisible.value = true
}

const submitForm = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        await createLeaveRequest({
          type: form.type,
          start_date: form.dateRange?.[0] || '',
          end_date: form.dateRange?.[1] || '',
          reason: form.reason
        })
        ElMessage.success('申请提交成功')
        dialogVisible.value = false
        fetchRequests()
      } catch (error) {
        ElMessage.error('提交失败')
      } finally {
        submitting.value = false
      }
    }
  })
}

const handleCancel = (row: LeaveRequest) => {
  ElMessageBox.confirm('确定撤销该请假申请吗？', '提示', {
    type: 'warning'
  }).then(async () => {
    try {
      await cancelLeaveRequest(row.id)
      ElMessage.success('撤销成功')
      fetchRequests()
    } catch (error) {
      ElMessage.error('撤销失败')
    }
  })
}

const calculateDays = (start: string, end: string) => {
  if (!start || !end) return 0
  return dayjs(end).diff(dayjs(start), 'day') + 1
}

const formatDate = (date: string) => {
  return dayjs(date).format('YYYY-MM-DD HH:mm')
}

const disabledDate = (time: Date) => {
  return time.getTime() < Date.now() - 8.64e7 // Disable past dates
}

// Helpers
const getLeaveTypeLabel = (type: string) => {
  const map: Record<string, string> = {
    sick: '病假',
    casual: '事假',
    annual: '年假',
    other: '其他'
  }
  return map[type] || type
}

const getLeaveTypeTag = (type: string) => {
  const map: Record<string, string> = {
    sick: 'danger',
    casual: 'warning',
    annual: 'success',
    other: 'info'
  }
  return map[type] || 'info'
}

const getStatusLabel = (status: string) => {
  const map: Record<string, string> = {
    pending: '待审批',
    approved: '已批准',
    rejected: '已拒绝',
    cancelled: '已撤销'
  }
  return map[status] || status
}

const getStatusType = (status: string) => {
  const map: Record<string, string> = {
    pending: 'warning',
    approved: 'success',
    rejected: 'danger',
    cancelled: 'info'
  }
  return map[status] || 'info'
}
</script>

<style scoped>
.schedule-view {
  padding: 24px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.section-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.text-danger {
  color: #F56C6C;
}

.text-success {
  color: #67C23A;
}
</style>
