<template>
  <el-card class="bed-scheduling-panel">
    <template #header>
      <div class="header">
        <span>床位调度管理面板</span>
        <div class="header-actions">
          <el-button size="small" type="primary" @click="openMatchDialog">
            智能匹配
          </el-button>
        </div>
      </div>
    </template>

    <el-form :inline="true" :model="filters" class="filter-bar" @submit.prevent="handleSearch">
      <el-form-item label="房间号">
        <el-input 
          v-model="filters.roomNumber" 
          placeholder="例如 101"
          @input="handleRoomNumberInput"
        />
      </el-form-item>
      <el-form-item label="床位ID">
        <el-input 
          v-model="filters.bedId" 
          placeholder="例如 bed-001"
          @input="handleBedIdInput"
        />
      </el-form-item>
      <el-form-item label="状态">
        <el-select v-model="filters.status" placeholder="所有状态" clearable style="width: 120px">
          <el-option label="空闲" value="available" />
          <el-option label="已占用" value="occupied" />
          <el-option label="清洁中" value="cleaning" />
          <el-option label="维修中" value="maintenance" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" :loading="loading" @click="handleSearch">
          查询
        </el-button>
        <el-button @click="handleReset">重置</el-button>
      </el-form-item>
    </el-form>

    <el-descriptions :column="5" size="small" border class="summary">
      <el-descriptions-item label="床位总数">{{ status?.totalBeds ?? '-' }}</el-descriptions-item>
      <el-descriptions-item label="空闲" class="status-available">
        {{ status?.available ?? '-' }}
      </el-descriptions-item>
      <el-descriptions-item label="已占用" class="status-occupied">
        {{ status?.occupied ?? '-' }}
      </el-descriptions-item>
      <el-descriptions-item label="清洁中" class="status-cleaning">
        {{ status?.cleaning ?? '-' }}
      </el-descriptions-item>
      <el-descriptions-item label="维修中" class="status-maintenance">
        {{ status?.maintenance ?? '-' }}
      </el-descriptions-item>
    </el-descriptions>

    <div class="visual-bed-grid">
      <div
        v-for="bed in filteredBeds"
        :key="bed.id"
        :class="['bed-card', `bed-${bed.status}`]"
        @click="handleBedClick(bed)"
      >
        <div class="bed-header">
          <span class="bed-location">{{ bed.roomNumber }}-{{ bed.bedNumber }}</span>
          <el-tag :type="statusType(bed.status)" size="small">
            {{ statusText(bed.status) }}
          </el-tag>
        </div>
        <div class="bed-content">
          <div v-if="bed.elderlyName" class="elderly-info">
            <el-icon><User /></el-icon>
            <span>{{ bed.elderlyName }}</span>
          </div>
          <div v-else class="bed-empty">
            <el-icon><Plus /></el-icon>
            <span>空闲</span>
          </div>
        </div>
        <div class="bed-actions">
          <el-button
            v-if="bed.status === 'available'"
            size="small"
            type="primary"
            @click.stop="$emit('assign', bed.id)"
          >
            分配床位
          </el-button>
          <el-button
            v-if="bed.status === 'occupied'"
            size="small"
            type="warning"
            @click.stop="handleRelease(bed)"
          >
            释放床位
          </el-button>
          <el-button
            v-if="bed.status === 'cleaning'"
            size="small"
            type="success"
            @click.stop="handleCompleteCleaning(bed)"
          >
            完成清洁
          </el-button>
        </div>
      </div>
    </div>

    <el-table
      :data="filteredBeds"
      size="small"
      style="margin-top: 12px"
      empty-text="暂无床位数据"
      @row-click="handleRowClick"
    >
      <el-table-column prop="roomNumber" label="房间号" width="100" />
      <el-table-column prop="bedNumber" label="床位号" width="80" />
      <el-table-column prop="status" label="状态" width="120">
        <template #default="scope">
          <el-tag :type="statusType(scope.row.status)" size="small">
            {{ statusText(scope.row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="elderlyName" label="院民姓名" min-width="120" />
      <el-table-column prop="lastUpdated" label="更新时间" width="160">
        <template #default="scope">
          {{ formatDateTime(scope.row.lastUpdated) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="scope">
          <el-button
            v-if="scope.row.status === 'available'"
            size="small"
            type="primary"
            @click="$emit('assign', scope.row.id)"
          >
            分配床位
          </el-button>
          <el-button
            v-if="scope.row.status === 'occupied'"
            size="small"
            type="warning"
            @click="handleRelease(scope.row)"
          >
            释放床位
          </el-button>
          <el-button
            v-if="scope.row.status === 'cleaning'"
            size="small"
            type="success"
            @click="handleCompleteCleaning(scope.row)"
          >
            完成清洁
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="matchDialogVisible" title="智能床位匹配" width="600px">
      <el-form :model="matchForm" label-width="100px" :rules="matchRules" ref="matchFormRef">
        <el-form-item label="院民ID" prop="elderlyId">
          <el-input v-model="matchForm.elderlyId" placeholder="请输入院民ID" />
        </el-form-item>
        <el-form-item label="护理等级" prop="nursingLevel">
          <el-select v-model="matchForm.nursingLevel" placeholder="请选择护理等级">
            <el-option label="一级护理" value="level1" />
            <el-option label="二级护理" value="level2" />
            <el-option label="三级护理" value="level3" />
            <el-option label="特护" value="special" />
          </el-select>
        </el-form-item>
      </el-form>
      <div v-if="matchResult" class="match-result">
        <h4>匹配结果</h4>
        <el-alert :title="`推荐床位: ${matchResult.recommendedBed.roomNumber}-${matchResult.recommendedBed.bedNumber}`" type="success" :closable="false">
          <template #default>
            <p>匹配度: {{ matchResult.recommendedBed.matchScore }}/100</p>
            <p>推荐理由: {{ matchResult.recommendedBed.reason }}</p>
          </template>
        </el-alert>
        <el-table :data="matchResult.matchedBeds" size="small" style="margin-top: 12px">
          <el-table-column prop="roomNumber" label="房间" width="80" />
          <el-table-column prop="bedNumber" label="床位" width="80" />
          <el-table-column prop="matchScore" label="匹配度" width="100">
            <template #default="scope">
              <el-progress :percentage="scope.row.matchScore" :stroke-width="8" />
            </template>
          </el-table-column>
          <el-table-column prop="reason" label="匹配理由" min-width="150" />
        </el-table>
      </div>
      <template #footer>
        <el-button @click="matchDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="matching" @click="handleMatch">
          开始匹配
        </el-button>
        <el-button
          v-if="matchResult"
          type="success"
          @click="handleAssignRecommended"
        >
          分配推荐
        </el-button>
      </template>
    </el-dialog>
  </el-card>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { User, Plus } from '@element-plus/icons-vue'
import type { BedStatus, MatchBedData, BedMatchResult } from '@/services/bed-scheduling'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'

const props = defineProps<{
  status: BedStatus | null
  loading?: boolean
}>()

const emit = defineEmits<{
  (e: 'refresh', filters: any): void
  (e: 'assign', bedId: string): void
  (e: 'match', data: MatchBedData): void
  (e: 'release', bed: any): void
  (e: 'complete-cleaning', bed: any): void
}>()

const filters = reactive<{
  roomNumber?: string
  bedId?: string
  status?: string
}>({
  roomNumber: undefined,
  bedId: undefined,
  status: undefined
})

const matchDialogVisible = ref(false)
const matching = ref(false)
const matchResult = ref<BedMatchResult | null>(null)
const matchFormRef = ref<FormInstance>()

const matchForm = reactive<MatchBedData>({
  elderlyId: '',
  nursingLevel: ''
})

const matchRules: FormRules = {
  elderlyId: [
    { required: true, message: '请输入院民ID', trigger: 'blur' },
    { pattern: /^[a-zA-Z0-9-]+$/, message: '院民ID格式不正确', trigger: 'blur' }
  ],
  nursingLevel: [
    { required: true, message: '请选择护理等级', trigger: 'change' }
  ]
}

const filteredBeds = computed(() => {
  const statusValue = props.status
  if (!statusValue?.beds) return []
  return statusValue.beds.filter((bed: any) => {
    if (filters.roomNumber && !bed.roomNumber.includes(filters.roomNumber)) return false
    if (filters.bedId) {
      const search = filters.bedId.toString().toLowerCase()
      const bedNum = bed.bedNumber ? bed.bedNumber.toString().toLowerCase() : ''
      const id = bed.id ? bed.id.toString().toLowerCase() : ''
      if (!bedNum.includes(search) && !id.includes(search)) return false
    }
    if (filters.status && bed.status !== filters.status) return false
    return true
  })
})

const statusText = (value: BedStatus['beds'][number]['status']) => {
  const map = {
    available: '空闲',
    occupied: '已占用',
    cleaning: '清洁中',
    maintenance: '维修中'
  } as const
  return map[value] || value
}

const statusType = (value: BedStatus['beds'][number]['status']) => {
  const map = {
    available: 'success',
    occupied: 'info',
    cleaning: 'warning',
    maintenance: 'danger'
  } as const
  return map[value] || 'info'
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('zh-CN')
}

const formatDateTime = (date?: string) => {
  if (!date) return '-'
  return new Date(date).toLocaleString('zh-CN')
}

const handleRoomNumberInput = async (value: string) => {
  if (value.length >= 3) {
    emit('refresh', { roomNumber: value })
  }
}

const handleBedIdInput = async (value: string) => {
  if (value.length >= 5) {
    emit('refresh', { bedId: value })
  }
}

const handleSearch = () => {
  emit('refresh', filters)
}

const handleReset = () => {
  filters.roomNumber = undefined
  filters.bedId = undefined
  filters.status = undefined
  emit('refresh', {})
}

const handleBedClick = (bed: any) => {
  console.log('Bed clicked:', bed)
}

const handleRowClick = (row: any) => {
  console.log('Row clicked:', row)
}

const openMatchDialog = () => {
  matchDialogVisible.value = true
  matchResult.value = null
  matchForm.elderlyId = ''
  matchForm.nursingLevel = ''
  matchForm.preferredBuilding = undefined
  matchForm.preferredFloor = undefined
}

const handleMatch = async () => {
  if (!matchFormRef.value) return
  
  try {
    await matchFormRef.value.validate()
    matching.value = true
    emit('match', matchForm)
  } catch (error) {
    console.error('表单验证失败:', error)
  } finally {
    matching.value = false
  }
}

const handleAssignRecommended = () => {
  if (matchResult.value) {
    emit('assign', matchResult.value.recommendedBed.id)
    matchDialogVisible.value = false
  }
}

const handleRelease = async (bed: any) => {
  try {
    await ElMessageBox.confirm(
      `确定要释放 ${bed.roomNumber}-${bed.bedNumber} 床位吗？`,
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    emit('release', bed)
  } catch {
    ElMessage.info('已取消操作')
  }
}

const handleCompleteCleaning = async (bed: any) => {
  try {
    await ElMessageBox.confirm(
      `确认 ${bed.roomNumber}-${bed.bedNumber} 清洁已完成吗？`,
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'success'
      }
    )
    emit('complete-cleaning', bed)
  } catch {
    ElMessage.info('已取消操作')
  }
}

const setMatchResult = (result: BedMatchResult) => {
  matchResult.value = result
}

defineExpose({
  setMatchResult
})
</script>

<style scoped>
.bed-scheduling-panel {
  width: 100%;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.filter-bar {
  margin-bottom: 12px;
}

.summary {
  margin-bottom: 16px;
}

.summary :deep(.el-descriptions__label) {
  font-weight: bold;
}

.summary.status-available :deep(.el-descriptions__body) {
  color: #67c23a;
}

.summary.status-occupied :deep(.el-descriptions__body) {
  color: #909399;
}

.summary.status-cleaning :deep(.el-descriptions__body) {
  color: #e6a23c;
}

.summary.status-maintenance :deep(.el-descriptions__body) {
  color: #f56c6c;
}

.visual-bed-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
  margin-bottom: 16px;
}

.bed-card {
  border: 2px solid #dcdfe6;
  border-radius: 8px;
  padding: 12px;
  cursor: pointer;
  transition: all 0.3s;
}

.bed-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.bed-available {
  border-color: #67c23a;
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
}

.bed-occupied {
  border-color: #909399;
  background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
}

.bed-cleaning {
  border-color: #e6a23c;
  background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
}

.bed-maintenance {
  border-color: #f56c6c;
  background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
}

.bed-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.bed-location {
  font-weight: bold;
  color: #303133;
}

.bed-content {
  min-height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
}

.elderly-info {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #606266;
}

.bed-empty {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #909399;
  font-size: 14px;
}

.bed-actions {
  display: flex;
  gap: 8px;
  justify-content: center;
}

.match-result {
  margin-top: 16px;
}

.match-result h4 {
  margin: 0 0 12px 0;
  color: #303133;
}

@media (max-width: 768px) {
  .visual-bed-grid {
    grid-template-columns: 1fr;
  }
  
  .filter-bar {
    flex-direction: column;
  }
  
  .header-actions {
    flex-direction: column;
  }
}
</style>