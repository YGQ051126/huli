<template>
  <div class="activity-gallery">
    <div class="toolbar">
      <el-button type="primary" @click="dialogVisible = true">发布新活动</el-button>
      <el-button @click="$emit('refresh')">刷新</el-button>
    </div>

    <el-row :gutter="16">
      <el-col v-for="item in activities" :key="item.id" :span="8">
        <el-card :body-style="{ padding: '12px' }" class="activity-card">
          <div class="title">{{ item.title }}</div>
          <div class="meta">
            <span>{{ item.activityDate }}</span>
            <span>照片数量: {{ item.mediaCount }}</span>
          </div>
          <div class="footer">
            <el-button size="small" @click="handleViewDetail(item.id)">查看</el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-empty v-if="!activities.length && !loading" description="暂无活动记录" />

    <el-dialog v-model="dialogVisible" title="发布新活动" width="480px">
      <el-form :model="form" label-width="90px">
        <el-form-item label="活动标题">
          <el-input v-model="form.title" placeholder="请输入活动标题" />
        </el-form-item>
        <el-form-item label="活动日期">
          <el-date-picker v-model="form.activityDate" type="date" value-format="YYYY-MM-DD" />
        </el-form-item>
        <el-form-item label="活动描述">
          <el-input v-model="form.description" type="textarea" rows="3" />
        </el-form-item>
        <el-form-item label="活动媒体">
          <el-upload
            v-model:file-list="fileList"
            :auto-upload="false"
            list-type="picture-card"
            accept="image/png,image/jpeg,image/gif,image/webp,video/mp4,video/webm,video/ogg"
            :on-preview="handlePictureCardPreview"
          >
            <el-icon><Plus /></el-icon>
          </el-upload>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleCreate">发布</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="previewVisible" title="预览" width="60%">
      <video v-if="previewType === 'video'" :src="previewUrl" controls style="width: 100%"></video>
      <img v-else :src="previewUrl" alt="Preview Image" style="width: 100%" />
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import type { UploadProps, UploadUserFile } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import type { ActivityGallery, CreateActivityData } from '@/services/activity-gallery'

defineProps<{
  activities: ActivityGallery[]
  loading?: boolean
}>()

const emit = defineEmits<{
  (e: 'refresh'): void
  (e: 'create', data: CreateActivityData): void
  (e: 'view', id: string): void
}>()

const dialogVisible = ref(false)
const previewVisible = ref(false)
const previewUrl = ref('')
const previewType = ref<'image' | 'video'>('image')
const submitting = ref(false)
const fileList = ref<UploadUserFile[]>([])

const handlePictureCardPreview: UploadProps['onPreview'] = (uploadFile) => {
  previewUrl.value = uploadFile.url!
  
  // Determine type based on raw file type or name
  const rawFile = uploadFile.raw
  if (rawFile) {
    if (rawFile.type.startsWith('video/')) {
      previewType.value = 'video'
    } else {
      previewType.value = 'image'
    }
  } else {
    // Fallback if no raw file (e.g. existing files, though here we are creating new)
    // Simple extension check
    const url = uploadFile.url || ''
    if (url.match(/\.(mp4|webm|ogg)$/i)) {
      previewType.value = 'video'
    } else {
      previewType.value = 'image'
    }
  }
  
  previewVisible.value = true
}

const form = reactive<{
  title: string
  activityDate: string
  description?: string
}>({
  title: '',
  activityDate: '',
  description: ''
})

function handleViewDetail(id: string) {
  console.log('点击查看活动详情, ID:', id)
  emit('view', id)
}

async function handleCreate() {
  if (!form.title || !form.activityDate) return
  submitting.value = true
  try {
    const files = (fileList.value || []).map(f => f.raw!).filter(Boolean)
    console.log('准备上传的文件:', files)
    
    if (files.length === 0 && fileList.value.length > 0) {
      console.warn('警告: fileList 有数据但无法提取 raw File', fileList.value)
    }

    const payload: CreateActivityData = {
      title: form.title,
      description: form.description,
      activityDate: form.activityDate,
      mediaFiles: files
    }
    emit('create', payload)
    dialogVisible.value = false
    fileList.value = []
    form.title = ''
    form.activityDate = ''
    form.description = ''
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.toolbar {
  margin-bottom: 16px;
  display: flex;
  gap: 8px;
}

.activity-card .title {
  font-weight: 600;
}

.activity-card .meta {
  margin-top: 4px;
  font-size: 12px;
  color: #999;
  display: flex;
  justify-content: space-between;
}

.activity-card .footer {
  margin-top: 8px;
  text-align: right;
}
</style>
