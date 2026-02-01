<template>
  <div>
    <el-page-header content="患者管理" />
    <el-table :data="patients">
      <el-table-column prop="name" label="姓名" />
      <el-table-column prop="age" label="年龄" width="100" />
      <el-table-column prop="careLevel" label="护理等级" width="120" />
      <el-table-column prop="bedNumber" label="床位" width="120" />
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { usePatientsStore } from '@/stores/patients'

const patientsStore = usePatientsStore()
const patients = computed(() => patientsStore.list)

onMounted(() => {
  patientsStore.fetchPatients()
})
</script>
