<template>
  <el-form :model="form" label-width="80px">
    <el-form-item label="日期">
      <el-date-picker v-model="form.date" type="date" />
    </el-form-item>
    <el-form-item label="时间段">
      <el-select v-model="form.timeSlot" placeholder="选择时间段">
        <el-option v-for="slot in timeSlots" :key="slot" :label="slot" :value="slot" />
      </el-select>
    </el-form-item>
    <div class="actions">
      <el-button @click="$emit('onCancel')">取消</el-button>
      <el-button type="primary" @click="submit">提交</el-button>
    </div>
  </el-form>
</template>

<script setup lang="ts">
import { reactive } from 'vue'

const props = defineProps({
  patientId: { type: String, required: true },
  availableTimeSlots: { type: Array as () => string[], default: () => ['09:00-10:00', '10:00-11:00'] }
})

const emit = defineEmits<{
  (e: 'onSubmit', payload: { patientId: string; date: string; timeSlot: string; type: string }): void
  (e: 'onCancel'): void
}>()

const form = reactive({ date: '', timeSlot: '' })
const timeSlots = props.availableTimeSlots

function submit() {
  const payload = { patientId: props.patientId, date: form.date, timeSlot: form.timeSlot, type: 'visit' }
  emit('onSubmit', payload)
}
</script>

<style scoped>
.actions { display: flex; justify-content: flex-end; gap: 8px }
</style>
