<template>
  <div class="bed-scheduling-view">
    <el-page-header content="床位调度" />
    <div style="margin-top: 16px">
      <BedSchedulingPanel
        ref="bedPanelRef"
        :status="status"
        :loading="loading"
        @refresh="handleRefresh"
        @assign="openAssign"
        @match="handleMatch"
        @release="handleRelease"
        @complete-cleaning="handleCompleteCleaning"
      />
    </div>

    <el-dialog v-model="assignDialogVisible" title="分配床位" width="500px" @close="resetAssignForm">
      <el-form :model="assignForm" label-width="100px" :rules="assignRules" ref="assignFormRef">
        <el-form-item label="院民ID" prop="elderlyId">
          <el-input v-model="assignForm.elderlyId" placeholder="输入院民ID" />
        </el-form-item>
        <el-form-item label="院民姓名" prop="elderlyName">
          <el-input v-model="assignForm.elderlyName" placeholder="输入院民姓名" />
        </el-form-item>
        <el-form-item label="护理等级" prop="nursingLevel">
          <el-select v-model="assignForm.nursingLevel" placeholder="选择护理等级">
            <el-option label="一级护理" value="level1" />
            <el-option label="二级护理" value="level2" />
            <el-option label="三级护理" value="level3" />
            <el-option label="特护" value="special" />
          </el-select>
        </el-form-item>
        <el-form-item label="入住日期" prop="assignDate">
          <el-date-picker
            v-model="assignForm.assignDate"
            type="date"
            placeholder="选择入住日期"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="备注">
          <el-input
            v-model="assignForm.notes"
            type="textarea"
            :rows="3"
            placeholder="填写备注信息（可选）"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="assignDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="assigning" @click="handleAssignConfirm">
          确认分配
        </el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="allocationFormDialogVisible" title="床位分配单" width="600px">
      <div v-if="currentAllocation" class="allocation-form">
        <h3>床位分配确认单</h3>
        <el-descriptions :column="2" border>
          <el-descriptions-item label="分配单号">{{ currentAllocation.id }}</el-descriptions-item>
          <el-descriptions-item label="分配时间">{{ formatDate(currentAllocation.createdAt) }}</el-descriptions-item>
          <el-descriptions-item label="院民ID">{{ currentAllocation.elderlyId }}</el-descriptions-item>
          <el-descriptions-item label="院民姓名">{{ currentAllocation.elderlyName }}</el-descriptions-item>
          <el-descriptions-item label="床位号">{{ currentAllocation.roomNumber }}-{{ currentAllocation.bedNumber }}</el-descriptions-item>
          <el-descriptions-item label="入住日期">{{ formatDate(currentAllocation.assignDate) }}</el-descriptions-item>
          <el-descriptions-item label="保洁通知" :span="2">
            <el-tag :type="currentAllocation.cleaningNotified ? 'success' : 'warning'">
              {{ currentAllocation.cleaningNotified ? '已发送' : '未发送' }}
            </el-tag>
          </el-descriptions-item>
        </el-descriptions>
        <div class="form-actions">
          <el-button @click="downloadAllocationForm">下载分配单</el-button>
          <el-button type="primary" @click="allocationFormDialogVisible = false">
            关闭
          </el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import BedSchedulingPanel from '@/components/business/BedSchedulingPanel.vue'
import {
  getBedStatus,
  assignBed,
  matchBed,
  updateBedStatus,
  getAllocationHistory,
  generateAllocationForm,
  type BedStatus,
  type MatchBedData,
  type BedAssignment
} from '@/services/bed-scheduling'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'

const bedPanelRef = ref<InstanceType<typeof BedSchedulingPanel>>()
const status = ref<BedStatus | null>(null)
const loading = ref(false)

const assignDialogVisible = ref(false)
const assigning = ref(false)
const currentBedId = ref<string | null>(null)
const currentAllocation = ref<BedAssignment | null>(null)
const allocationFormDialogVisible = ref(false)

const assignFormRef = ref<FormInstance>()

const assignForm = reactive<{
  elderlyId: string
  elderlyName: string
  nursingLevel: string
  assignDate: Date | null
  notes?: string
}>({
  elderlyId: '',
  elderlyName: '',
  nursingLevel: '',
  assignDate: new Date(),
  notes: ''
})

const assignRules: FormRules = {
  elderlyId: [
    { required: true, message: '请输入院民ID', trigger: 'blur' },
    { pattern: /^[a-zA-Z0-9-]+$/, message: '院民ID格式不正确', trigger: 'blur' }
  ],
  elderlyName: [
    { required: true, message: '请输入院民姓名', trigger: 'blur' },
    { min: 2, max: 20, message: '姓名长度在2-20个字符', trigger: 'blur' }
  ],
  nursingLevel: [
    { required: true, message: '请选择护理等级', trigger: 'change' }
  ],
  assignDate: [
    { required: true, message: '请选择入住日期', trigger: 'change' }
  ]
}

async function handleRefresh(filters: any) {
  loading.value = true
  try {
    console.log('Fetching bed status with filters:', filters)
    status.value = await getBedStatus(undefined, undefined, filters.status)
    console.log('Bed status loaded:', status.value)
    
    if (bedPanelRef.value) {
      try {
        const history = await getAllocationHistory()
        bedPanelRef.value.setHistory(history)
      } catch (historyError) {
        console.error('获取床位分配历史失败(不影响床位状态展示):', historyError)
      }
    }
  } catch (error) {
    console.error('获取床位状态失败:', error)
    const errMsg = String((error as any)?.message || error || '')
    if (errMsg.includes('请求的资源不存在')) {
      console.error('错误类型: 资源不存在(404)，请检查后端接口是否已启动、URL是否为 /api/v1/bed_scheduling/beds/status/')
    } else if (errMsg.includes('网络错误')) {
      console.error('错误类型: 网络错误，请检查后端服务是否运行在 http://localhost:8000')
    } else if (errMsg.includes('数据格式错误')) {
      console.error('错误类型: 数据格式错误，请检查后端返回字段结构是否符合 BedStatus')
    }
    ElMessage.error('获取床位状态失败，请重试')
  } finally {
    loading.value = false
  }
}

function openAssign(bedId: string) {
  console.log('Opening assign dialog for bed:', bedId)
  currentBedId.value = bedId
  assignDialogVisible.value = true
}

async function handleAssignConfirm() {
  if (!currentBedId.value || !assignFormRef.value) {
    return
  }

  try {
    await assignFormRef.value.validate()
    
    assigning.value = true
    console.log('Assigning bed:', {
      elderlyId: assignForm.elderlyId,
      bedId: currentBedId.value,
      assignDate: assignForm.assignDate?.toISOString()
    })

    const assignment = await assignBed({
      elderlyId: assignForm.elderlyId,
      bedId: currentBedId.value,
      assignDate: assignForm.assignDate?.toISOString() || new Date().toISOString()
    })

    console.log('Bed assigned successfully:', assignment)
    currentAllocation.value = assignment
    
    ElMessage.success('床位分配成功，并已通知保洁')
    assignDialogVisible.value = false
    allocationFormDialogVisible.value = true
    
    await handleRefresh({})
  } catch (error) {
    console.error('床位分配失败:', error)
    ElMessage.error('床位分配失败，请重试')
  } finally {
    assigning.value = false
  }
}

async function handleMatch(data: MatchBedData) {
  try {
    console.log('Matching bed with criteria:', data)
    const matchResult = await matchBed(data)
    console.log('Match result:', matchResult)
    
    if (bedPanelRef.value) {
      bedPanelRef.value.setMatchResult(matchResult)
    }
    
    ElMessage.success('智能匹配完成')
  } catch (error) {
    console.error('智能匹配失败:', error)
    ElMessage.error('智能匹配失败，请重试')
  }
}

async function handleRelease(bed: any) {
  try {
    console.log('Releasing bed:', bed)
    await updateBedStatus(bed.id, 'available')
    ElMessage.success('床位已释放')
    await handleRefresh({})
  } catch (error) {
    console.error('释放床位失败:', error)
    ElMessage.error('释放床位失败，请重试')
  }
}

async function handleCompleteCleaning(bed: any) {
  try {
    console.log('Completing cleaning for bed:', bed)
    await updateBedStatus(bed.id, 'available')
    ElMessage.success('清理完成，床位已标记为空闲')
    await handleRefresh({})
  } catch (error) {
    console.error('更新床位状态失败:', error)
    ElMessage.error('更新床位状态失败，请重试')
  }
}

function resetAssignForm() {
  assignForm.elderlyId = ''
  assignForm.elderlyName = ''
  assignForm.nursingLevel = ''
  assignForm.assignDate = new Date()
  assignForm.notes = ''
  if (assignFormRef.value) {
    assignFormRef.value.clearValidate()
  }
}

async function downloadAllocationForm() {
  if (!currentAllocation.value) return
  
  try {
    console.log('Generating allocation form for:', currentAllocation.value.id)
    const blob = await generateAllocationForm(currentAllocation.value.id)
    
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `床位分配单_${currentAllocation.value.id}_${new Date().getTime()}.pdf`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(url)
    
    ElMessage.success('分配单下载成功')
  } catch (error) {
    console.error('下载分配单失败:', error)
    ElMessage.error('下载分配单失败，请重试')
  }
}

function formatDate(date: string) {
  return new Date(date).toLocaleDateString('zh-CN')
}

onMounted(() => {
  console.log('Bed scheduling view mounted')
  handleRefresh({})
})
</script>

<style scoped>
.bed-scheduling-view {
  padding: 16px;
}

.allocation-form {
  padding: 16px;
}

.allocation-form h3 {
  margin: 0 0 16px 0;
  color: #303133;
  text-align: center;
}

.form-actions {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-top: 24px;
}

@media (max-width: 768px) {
  .bed-scheduling-view {
    padding: 8px;
  }
  
  .form-actions {
    flex-direction: column;
  }
}
</style>
