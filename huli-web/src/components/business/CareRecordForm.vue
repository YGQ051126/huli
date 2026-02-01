<template>
  <el-card class="care-record-form">
    <template #header>
      <div class="header">
        <span>护理记录</span>
        <el-tag v-if="template" type="info" effect="plain">{{ template.name }}</el-tag>
      </div>
    </template>

    <el-skeleton v-if="loading" :rows="4" animated />
    <el-empty v-else-if="!template" description="暂无可用的护理记录模板" />
    <el-form
      v-else
      ref="formRef"
      :model="form"
      label-width="100px"
      :disabled="disabled"
    >
      <el-form-item label="记录时间">
        <el-date-picker
          v-model="form.recordDate"
          type="datetime"
          value-format="YYYY-MM-DD HH:mm:ss"
          style="width: 100%"
        />
      </el-form-item>

      <el-divider content-position="left">生命体征</el-divider>
      <el-row :gutter="12">
        <el-col :span="8">
          <el-form-item label="体温(℃)">
            <el-input-number v-model="form.vitalSigns.temperature" :min="30" :max="45" :step="0.1" />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="心率(次/分)">
            <el-input-number v-model="form.vitalSigns.heartRate" :min="30" :max="180" />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="呼吸(次/分)">
            <el-input-number v-model="form.vitalSigns.respiratoryRate" :min="5" :max="60" />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="12">
        <el-col :span="12">
          <el-form-item label="收缩压(mmHg)">
            <el-input-number v-model="form.vitalSigns.bloodPressure.systolic" :min="60" :max="240" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="舒张压(mmHg)">
            <el-input-number v-model="form.vitalSigns.bloodPressure.diastolic" :min="30" :max="160" />
          </el-form-item>
        </el-col>
      </el-row>

      <el-divider content-position="left">日常护理记录</el-divider>

      <el-form-item
        v-for="field in template.fields"
        :key="field.id"
        :label="field.label"
        :prop="field.id"
      >
        <component
          :is="resolveComponent(field.type)"
          v-model="form.fields[field.id]"
          v-bind="fieldProps(field)"
        >
          <template v-if="field.type === 'select'">
            <el-option
              v-for="opt in field.options || []"
              :key="String(opt.value)"
              :label="opt.label"
              :value="opt.value"
            />
          </template>
          <template v-if="field.type === 'checkbox_group'">
            <el-checkbox
              v-for="opt in field.options || []"
              :key="String(opt.value)"
              :label="opt.value"
            >
              {{ opt.label }}
            </el-checkbox>
          </template>
        </component>
      </el-form-item>

      <div class="actions">
        <el-button @click="$emit('cancel')">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSave('draft')">
          保存草稿
        </el-button>
        <el-button type="success" :loading="submitting" @click="handleSave('submitted')">
          提交记录
        </el-button>
      </div>
    </el-form>
  </el-card>
</template>

<script setup lang="ts">
import { onMounted, ref, reactive } from 'vue'
import type { FormInstance } from 'element-plus'
import type { CareRecordTemplate, CareRecordPayload } from '@/types/care'
import type { VitalSigns } from '@/types/patient'
import { getCareRecordTemplate, saveCareRecord, submitCareRecord } from '@/services/care-records'

const props = defineProps<{
  patientId: string
  staffId: string
  disabled?: boolean
}>()

const emit = defineEmits<{
  (e: 'saved'): void
  (e: 'submitted'): void
  (e: 'cancel'): void
}>()

const template = ref<CareRecordTemplate | null>(null)
const loading = ref(false)
const submitting = ref(false)
const formRef = ref<FormInstance>()

const defaultVital: VitalSigns = {
  temperature: 36.5,
  heartRate: 72,
  bloodPressure: { systolic: 120, diastolic: 80 },
  respiratoryRate: 18,
  oxygenSaturation: 98
}

const form = reactive<{
  recordDate: string
  vitalSigns: VitalSigns
  fields: Record<string, string | number | boolean>
}>({
  recordDate: '',
  vitalSigns: { ...defaultVital, bloodPressure: { ...defaultVital.bloodPressure } },
  fields: {}
})

onMounted(async () => {
  loading.value = true
  try {
    template.value = await getCareRecordTemplate(props.patientId)
  } finally {
    loading.value = false
  }
})

const resolveComponent = (type: string) => {
  if (type === 'textarea') return 'el-input'
  if (type === 'select') return 'el-select'
  if (type === 'number') return 'el-input-number'
  if (type === 'switch') return 'el-switch'
  if (type === 'checkbox_group') return 'el-checkbox-group'
  return 'el-input'
}

const fieldProps = (field: CareRecordTemplate['fields'][number]) => {
  const common = {
    placeholder: field.placeholder
  }
  if (field.type === 'textarea') {
    return { ...common, type: 'textarea', rows: 3 }
  }
  return common
}

async function handleSave(status: CareRecordPayload['status']) {
  if (!template.value) return
  
  // 表单验证
  try {
    await formRef.value?.validate()
  } catch (error) {
    return
  }
  
  submitting.value = true
  try {
    const payload: CareRecordPayload = {
      patientId: props.patientId,
      staffId: props.staffId,
      recordDate: form.recordDate || new Date().toISOString(),
      templateId: template.value.id,
      status,
      vitalSigns: form.vitalSigns,
      fields: form.fields
    }
    if (status === 'draft') {
      await saveCareRecord(payload)
      emit('saved')
    } else {
      await submitCareRecord(payload)
      emit('submitted')
    }
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.care-record-form :deep(.el-card__header) {
  padding: 12px 16px;
}

.header {
  display: flex;
  gap: 8px;
  align-items: center;
}

.actions {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}
</style>


