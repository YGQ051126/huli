<template>
  <div class="care-records-view">
    <el-page-header content="护理记录" />

    <el-row :gutter="16" style="margin-top: 16px">
      <el-col :span="8">
        <el-card shadow="hover">
          <template #header>
            <span>选择院民</span>
          </template>
          <el-skeleton v-if="patientsLoading" :rows="4" animated />
          <el-table
            v-else
            :data="patients"
            size="small"
            height="500"
            @row-click="handleSelectPatient"
            highlight-current-row
            stripe
          >
            <el-table-column prop="name" label="姓名" width="100" />
            <el-table-column prop="age" label="年龄" width="60" />
            <el-table-column prop="care_level" label="护理等级" />
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="16">
        <div v-if="currentPatientId">
          <el-card shadow="hover" class="record-list-card">
            <template #header>
              <div class="card-header">
                <span>历史护理记录</span>
              </div>
            </template>
            <el-table :data="careRecords" v-loading="recordsLoading" stripe height="500">
              <el-table-column prop="record_date" label="记录时间" width="160">
                <template #default="{ row }">
                    {{ formatDate(row.record_date) }}
                </template>
              </el-table-column>
              <el-table-column prop="staff.real_name" label="记录人" width="100">
                  <template #default="{ row }">
                    <span v-if="row._type === 'task'">-</span>
                    <span v-else>{{ row.staff?.real_name || row.staff?.username || '-' }}</span>
                  </template>
              </el-table-column>
              <el-table-column prop="status" label="状态" width="80">
                  <template #default="{ row }">
                    <el-tag v-if="row._type === 'task'" size="small" :type="row.is_completed ? 'success' : 'warning'">
                      {{ row.is_completed ? '已完成' : '未完成' }}
                    </el-tag>
                    <el-tag v-else size="small" :type="row.status === 'submitted' ? 'success' : 'info'">
                      {{ row.status === 'submitted' ? '已提交' : '草稿' }}
                    </el-tag>
                  </template>
              </el-table-column>
              <el-table-column label="摘要" min-width="150" show-overflow-tooltip>
                  <template #default="{ row }">
                    {{ getRecordSummary(row) }}
                  </template>
              </el-table-column>
              <el-table-column label="操作" width="80" fixed="right">
                <template #default="{ row }">
                  <el-button link type="primary" size="small" @click="viewRecord(row)">详情</el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </div>
        <el-empty v-else description="请先在左侧选择一位院民" />
      </el-col>
    </el-row>

    <!-- Detail Dialog -->
    <el-dialog v-model="detailVisible" title="护理记录详情" width="700px">
        <div v-if="currentRecord" class="record-detail">
            <div v-if="currentRecord._type === 'task'" class="task-detail">
                <el-descriptions title="打卡详情" :column="1" border>
                    <el-descriptions-item label="打卡日期">{{ currentRecord.task_date }}</el-descriptions-item>
                    <el-descriptions-item label="生命体征">{{ currentRecord.vital_signs_normal ? '正常' : '异常' }}</el-descriptions-item>
                    <el-descriptions-item label="饮食情况">{{ currentRecord.diet_normal ? '正常' : '异常' }}</el-descriptions-item>
                    <el-descriptions-item label="精神状态">{{ currentRecord.mental_normal ? '正常' : '异常' }}</el-descriptions-item>
                    <el-descriptions-item label="完成状态">{{ currentRecord.is_completed ? '已完成' : '未完成' }}</el-descriptions-item>
                    <el-descriptions-item label="更新时间">{{ formatDate(currentRecord.updated_at) }}</el-descriptions-item>
                </el-descriptions>
            </div>
            <div v-else>
                <el-descriptions title="基础信息" :column="2" border>
                    <el-descriptions-item label="记录时间">{{ formatDate(currentRecord.record_date) }}</el-descriptions-item>
                    <el-descriptions-item label="记录人">{{ currentRecord.staff?.real_name || '-' }}</el-descriptions-item>
                    <el-descriptions-item label="状态">
                        <el-tag size="small" :type="currentRecord.status === 'submitted' ? 'success' : 'info'">
                        {{ currentRecord.status === 'submitted' ? '已提交' : '草稿' }}
                        </el-tag>
                    </el-descriptions-item>
                </el-descriptions>

                <div class="mt-4" v-if="currentRecord.vital_signs">
                    <h4>生命体征</h4>
                    <el-descriptions :column="3" border size="small">
                        <el-descriptions-item label="体温">{{ currentRecord.vital_signs.temperature }} ℃</el-descriptions-item>
                        <el-descriptions-item label="心率">{{ currentRecord.vital_signs.heartRate }} 次/分</el-descriptions-item>
                        <el-descriptions-item label="呼吸">{{ currentRecord.vital_signs.respiratoryRate }} 次/分</el-descriptions-item>
                        <el-descriptions-item label="血压">
                            {{ currentRecord.vital_signs.bloodPressure?.systolic }}/{{ currentRecord.vital_signs.bloodPressure?.diastolic }} mmHg
                        </el-descriptions-item>
                        <el-descriptions-item label="血氧">{{ currentRecord.vital_signs.oxygenSaturation }} %</el-descriptions-item>
                    </el-descriptions>
                </div>

                <div class="mt-4" v-if="currentRecord.care_activities">
                    <h4>日常护理</h4>
                    <div v-for="(val, key) in currentRecord.care_activities" :key="key" class="activity-item">
                        <span class="label">{{ key }}: </span>
                        <span class="value">{{ val }}</span>
                    </div>
                </div>
                <div class="mt-4" v-if="currentRecord.fields">
                    <h4>其他记录</h4>
                    <div v-for="(val, key) in currentRecord.fields" :key="key" class="activity-item">
                        <span class="label">{{ key }}: </span>
                        <span class="value">{{ val }}</span>
                    </div>
                </div>
            </div>
        </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { usePatientsStore } from '@/stores/patients'
import type { Patient } from '@/types/patient'
import { getCareRecords, getDailyCareTasks } from '@/services/care-records'

const patientsStore = usePatientsStore()

const patients = computed(() => patientsStore.list)
const patientsLoading = computed(() => patientsStore.loading)
const currentPatientId = ref<string | null>(null)
const careRecords = ref<any[]>([])
const recordsLoading = ref(false)
const detailVisible = ref(false)
const currentRecord = ref<any>(null)

onMounted(() => {
  patientsStore.fetchPatients()
})

async function handleSelectPatient(row: Patient) {
  // Fix type mismatch: row.id might be number
  const pid = String(row.id)
  currentPatientId.value = pid
  
  // Fetch history records
  fetchHistory(pid)
}

async function fetchHistory(pid: string) {
    recordsLoading.value = true
    try {
        const [records, tasks] = await Promise.all([
            getCareRecords(pid),
            getDailyCareTasks(pid)
        ])
        
        // Merge and sort
        const combined = [
            ...records.map((r: any) => ({ ...r, _type: 'record' })),
            ...tasks.map((t: any) => ({ ...t, _type: 'task', record_date: t.updated_at || t.task_date }))
        ]
        
        combined.sort((a, b) => new Date(b.record_date).getTime() - new Date(a.record_date).getTime())
        
        careRecords.value = combined
    } catch (e) {
        console.error('Fetch records failed', e)
        careRecords.value = []
    } finally {
        recordsLoading.value = false
    }
}

function viewRecord(row: any) {
    currentRecord.value = row
    detailVisible.value = true
}

function formatDate(val: string) {
    if(!val) return ''
    return new Date(val).toLocaleString()
}

function getRecordSummary(row: any) {
    if (row._type === 'task') {
        const parts = []
        if (row.vital_signs_normal) parts.push('生命体征正常')
        else parts.push('生命体征异常')
        if (row.diet_normal) parts.push('饮食正常')
        else parts.push('饮食异常')
        if (row.mental_normal) parts.push('精神正常')
        else parts.push('精神异常')
        return `[日常打卡] ${parts.join(', ')}`
    }

    // 简略显示 vital signs 或者其他信息
    const vs = row.vital_signs
    if (vs) {
        return `T:${vs.temperature}℃ P:${vs.heartRate} BP:${vs.bloodPressure?.systolic}/${vs.bloodPressure?.diastolic}`
    }
    return '-'
}
</script>

<style scoped>
.care-records-view {
  padding: 16px;
}
.record-list-card {
  height: 600px;
  display: flex;
  flex-direction: column;
}
.record-list-card :deep(.el-card__body) {
  flex: 1;
  overflow: hidden;
  padding: 0;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.mt-4 {
    margin-top: 16px;
}
.activity-item {
    margin-bottom: 8px;
    border-bottom: 1px dashed #eee;
    padding-bottom: 4px;
}
.label {
    font-weight: bold;
    color: #606266;
    margin-right: 8px;
}
</style>
