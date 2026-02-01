<template>
  <el-card class="patient-card" shadow="hover">
    <div class="header">
      <el-avatar v-if="avatar" :src="avatar" size="large" />
      <div class="info">
        <div class="name">{{ name }}</div>
        <div class="meta">{{ genderText }} ? {{ age }}岁 ? 床位 {{ bedNumber }}</div>
      </div>
      <el-tag type="success">{{ careLevel }}</el-tag>
    </div>
    <div class="condition">{{ condition }}</div>
    <div class="actions">
      <el-button size="small" @click="$emit('onViewDetails', patientId)">ĎęÇé</el-button>
      <el-button size="small" type="primary" @click="$emit('onScheduleVisit', patientId)">Ô¤ÔźĚ˝ĘÓ</el-button>
      <el-button size="small" @click="$emit('onEdit', patientId)">ąŕź­</el-button>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps({
  patientId: { type: String, required: true },
  name: { type: String, required: true },
  age: { type: Number, required: true },
  gender: { type: String, required: true },
  avatar: { type: String, default: '' },
  condition: { type: String, default: '' },
  careLevel: { type: String, required: true },
  bedNumber: { type: String, required: true }
})

const genderText = computed(() => props.gender === 'male' ? 'ÄĐ' : 'ĹŽ')
</script>

<style scoped>
.patient-card { margin-bottom: 12px }
.header { display: flex; align-items: center; gap: 12px }
.info { flex: 1 }
.name { font-weight: 600 }
.meta { color: #888; font-size: 12px }
.condition { margin-top: 8px }
.actions { margin-top: 12px; display: flex; gap: 8px }
</style>
