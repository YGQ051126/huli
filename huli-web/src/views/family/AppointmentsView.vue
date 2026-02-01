<template>
  <div class="appointments-view">
    <el-page-header content="探视预约" />
    
    <div class="actions">
      <el-button type="primary" @click="showCreateDialog">申请探视</el-button>
      <el-button @click="refresh">刷新</el-button>
    </div>

    <el-table :data="appointments" style="width: 100%" v-loading="loading">
      <el-table-column prop="date" label="预约日期" width="120" sortable />
      <el-table-column prop="time_slot" label="时间段" width="140" />
      <el-table-column prop="type" label="类型" width="100">
        <template #default="scope">
          {{ getTypeName(scope.row.type) }}
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="100">
        <template #default="scope">
          <el-tag :type="getStatusType(scope.row.status)">{{ getStatusName(scope.row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="notes" label="备注" min-width="150" show-overflow-tooltip />
      <el-table-column label="操作" width="120" fixed="right">
        <template #default="scope">
          <el-button 
            v-if="scope.row.status === 'pending'" 
            size="small" 
            type="danger" 
            plain 
            @click="cancel(scope.row.id)"
          >
            取消
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- Create Dialog -->
    <el-dialog
      v-model="dialogVisible"
      title="申请探视预约"
      width="500px"
    >
      <el-form :model="form" label-width="80px" ref="formRef" :rules="rules">
        <el-form-item label="日期" prop="date">
          <el-date-picker
            v-model="form.date"
            type="date"
            placeholder="选择日期"
            value-format="YYYY-MM-DD"
            :disabled-date="disabledDate"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="时间段" prop="time_slot">
          <el-select v-model="form.time_slot" placeholder="选择时间段" style="width: 100%">
            <el-option label="上午 (09:00-11:00)" value="09:00-11:00" />
            <el-option label="下午 (14:00-16:00)" value="14:00-16:00" />
            <el-option label="晚上 (18:00-20:00)" value="18:00-20:00" />
          </el-select>
        </el-form-item>
        <el-form-item label="备注" prop="notes">
          <el-input v-model="form.notes" type="textarea" placeholder="请输入探视人数或其他说明" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitCreate" :loading="submitting">
            提交申请
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, reactive } from 'vue'
import { useAppointmentStore } from '@/stores/appointments'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance } from 'element-plus'

const appointmentStore = useAppointmentStore()
const appointments = computed(() => appointmentStore.appointments)
const loading = computed(() => appointmentStore.loading)

const dialogVisible = ref(false)
const submitting = ref(false)
const formRef = ref<FormInstance>()

const form = reactive({
  date: '',
  time_slot: '',
  notes: '',
  type: 'visit'
})

const rules = {
  date: [{ required: true, message: '请选择日期', trigger: 'change' }],
  time_slot: [{ required: true, message: '请选择时间段', trigger: 'change' }]
}

onMounted(() => {
  appointmentStore.fetchAppointments()
})

function refresh() {
  appointmentStore.fetchAppointments()
}

function showCreateDialog() {
  form.date = ''
  form.time_slot = ''
  form.notes = ''
  dialogVisible.value = true
}

function disabledDate(time: Date) {
  return time.getTime() < Date.now() - 8.64e7 // Disable past dates
}

function getTypeName(type: string) {
  const map: Record<string, string> = {
    visit: '探视',
    service: '服务',
    consultation: '咨询'
  }
  return map[type] || type
}

function getStatusName(status: string) {
  const map: Record<string, string> = {
    pending: '待审批',
    approved: '已通过',
    rejected: '已拒绝',
    cancelled: '已取消',
    completed: '已完成'
  }
  return map[status] || status
}

function getStatusType(status: string) {
  const map: Record<string, string> = {
    pending: 'warning',
    approved: 'success',
    rejected: 'danger',
    cancelled: 'info',
    completed: 'success'
  }
  return map[status] || 'info'
}

async function submitCreate() {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        await appointmentStore.createApt({
          ...form,
          patient: 0 // Backend handles this
        } as any)
        ElMessage.success('申请提交成功')
        dialogVisible.value = false
        refresh()
      } catch (error: any) {
        ElMessage.error(error.message || '提交失败')
      } finally {
        submitting.value = false
      }
    }
  })
}

function cancel(id: number) {
  ElMessageBox.confirm('确定要取消这个预约吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await appointmentStore.cancelApt(String(id))
      ElMessage.success('取消成功')
      refresh()
    } catch (error: any) {
      ElMessage.error(error.message || '取消失败')
    }
  })
}
</script>

<style scoped>
.appointments-view {
  padding: 20px;
}
.actions {
  margin: 20px 0;
  display: flex;
  gap: 10px;
}
</style>
