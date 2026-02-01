<template>
  <div class="care-records-view">
    <el-page-header content="护理记录" />

    <el-row :gutter="16" style="margin-top: 16px">
      <el-col :span="8">
        <el-card>
          <template #header>
            <span>选择院民</span>
          </template>
          <el-skeleton v-if="patientsLoading" :rows="4" animated />
          <el-table
            v-else
            :data="patients"
            size="small"
            height="400"
            @row-click="handleSelectPatient"
            highlight-current-row
          >
            <el-table-column prop="name" label="姓名" />
            <el-table-column prop="age" label="年龄" width="80" />
            <el-table-column prop="careLevel" label="护理等级" width="120" />
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="16">
        <CareRecordForm
          v-if="currentPatientId"
          :patient-id="currentPatientId"
          :staff-id="staffId"
          @saved="onSaved"
          @submitted="onSubmitted"
        />
        <el-empty v-else description="请先在左侧选择一位院民" />
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { usePatientsStore } from '@/stores/patients'
import { useUserStore } from '@/stores/user'
import CareRecordForm from '@/components/business/CareRecordForm.vue'
import type { Patient } from '@/types/patient'

const patientsStore = usePatientsStore()
const userStore = useUserStore()

const patients = computed(() => patientsStore.list)
const patientsLoading = computed(() => patientsStore.loading)
const currentPatientId = ref<string | null>(null)

const staffId = computed(() => String(userStore.user?.id || 'staff-demo'))

onMounted(() => {
  patientsStore.fetchPatients()
})

function handleSelectPatient(row: Patient) {
  currentPatientId.value = row.id
}

function onSaved() {
  ElMessage.success('护理记录草稿已保存')
}

function onSubmitted() {
  ElMessage.success('护理记录已提交')
}
</script>

<style scoped>
.care-records-view {
  padding: 16px;
}
</style>
