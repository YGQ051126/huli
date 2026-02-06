<template>
  <div class="patients-view">
    <el-page-header content="患者管理" class="page-header" icon="" title="患者列表" />
    
    <el-card shadow="never">
      <el-table :data="patients" v-loading="loading" stripe style="width: 100%">
        <el-table-column prop="name" label="姓名" width="100" />
        <el-table-column prop="gender" label="性别" width="80">
          <template #default="{ row }">
            {{ formatGender(row.gender) }}
          </template>
        </el-table-column>
        <el-table-column prop="age" label="年龄" width="80" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)" size="small">{{ formatStatus(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="care_level" label="护理等级" width="120" />
        <el-table-column prop="health_level" label="健康等级" width="120" />
        <el-table-column label="房间/床位" width="140">
          <template #default="{ row }">
            <span v-if="row.room">{{ row.room }}房 / {{ row.bed_id }}床</span>
            <span v-else class="text-gray">-</span>
          </template>
        </el-table-column>
        <el-table-column prop="phone" label="联系电话" width="130" />
        <el-table-column prop="admission_date" label="入院日期" min-width="120" />
        
        <el-table-column label="操作" fixed="right" width="100">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleView(row)">查看详情</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 详情弹窗 -->
    <el-dialog
      v-model="dialogVisible"
      title="患者详情"
      width="700px"
      destroy-on-close
    >
      <div v-if="currentPatient" class="patient-detail">
        <div class="detail-section">
          <h3 class="section-title">基本信息</h3>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="姓名">{{ currentPatient.name }}</el-descriptions-item>
            <el-descriptions-item label="性别">{{ formatGender(currentPatient.gender) }}</el-descriptions-item>
            <el-descriptions-item label="年龄">{{ currentPatient.age }}岁</el-descriptions-item>
            <el-descriptions-item label="身份证号">{{ currentPatient.id_card }}</el-descriptions-item>
            <el-descriptions-item label="联系电话">{{ currentPatient.phone }}</el-descriptions-item>
            <el-descriptions-item label="家庭住址">{{ currentPatient.address || '-' }}</el-descriptions-item>
          </el-descriptions>
        </div>

        <div class="detail-section">
          <h3 class="section-title">入住信息</h3>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="状态">
              <el-tag :type="getStatusType(currentPatient.status)" size="small">{{ formatStatus(currentPatient.status) }}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="入院日期">{{ currentPatient.admission_date }}</el-descriptions-item>
            <el-descriptions-item label="房间号">{{ currentPatient.room || '未分配' }}</el-descriptions-item>
            <el-descriptions-item label="床位号">{{ currentPatient.bed_id || '未分配' }}</el-descriptions-item>
            <el-descriptions-item label="护理等级">{{ currentPatient.care_level || '-' }}</el-descriptions-item>
            <el-descriptions-item label="健康等级">{{ currentPatient.health_level || '-' }}</el-descriptions-item>
          </el-descriptions>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { onMounted, computed, ref } from 'vue'
import { usePatientsStore } from '@/stores/patients'
import type { Patient } from '@/types/patient'

const patientsStore = usePatientsStore()
const patients = computed(() => patientsStore.list)
const loading = computed(() => patientsStore.loading)

const dialogVisible = ref(false)
const currentPatient = ref<Patient | null>(null)

const handleView = (row: Patient) => {
  currentPatient.value = row
  dialogVisible.value = true
}

const formatGender = (val: string) => {
  const map: Record<string, string> = { male: '男', female: '女' }
  return map[val] || val
}

const formatStatus = (val: string) => {
  const map: Record<string, string> = { 
    active: '在院', 
    discharged: '已出院', 
    transferred: '已转院',
    pending: '待入院' 
  }
  return map[val] || val
}

const getStatusType = (val: string) => {
  const map: Record<string, string> = { 
    active: 'success', 
    discharged: 'info', 
    transferred: 'warning',
    pending: 'primary' 
  }
  return map[val] || ''
}

onMounted(() => {
  patientsStore.fetchPatients()
})
</script>

<style scoped>
.patients-view {
  padding: 24px;
}
.page-header {
  margin-bottom: 24px;
}
.detail-section {
  margin-bottom: 24px;
}
.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 16px;
  padding-left: 12px;
  border-left: 4px solid #409eff;
}
.text-gray {
  color: #909399;
}
</style>
