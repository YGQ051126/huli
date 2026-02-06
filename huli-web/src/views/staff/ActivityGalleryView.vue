<template>
  <div class="activity-gallery-view">
    <el-page-header content="活动相册" />
    <el-card style="margin-top: 16px">
      <ActivityGalleryManager
        :activities="activities"
        :loading="loading"
        @refresh="fetch"
        @create="handleCreate"
        @view="handleView"
      />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRoute, useRouter } from 'vue-router'
import ActivityGalleryManager from '@/components/business/ActivityGalleryManager.vue'
import { getActivityGallery, createActivity, type ActivityGallery, type CreateActivityData } from '@/services/activity-gallery'
import { ElMessage } from 'element-plus'

const authStore = useAuthStore()
const route = useRoute()
const router = useRouter()
const activities = ref<ActivityGallery[]>([])
const loading = ref(false)

async function fetch() {
  loading.value = true
  try {
    console.log('获取活动列表...')
    activities.value = await getActivityGallery()
    console.log('活动列表数据:', activities.value)
  } catch (error) {
    console.error('获取活动列表失败:', error)
    ElMessage.error('获取活动列表失败')
  } finally {
    loading.value = false
  }
}

async function handleCreate(data: CreateActivityData) {
  try {
    console.log('创建活动:', data)
    await createActivity(data)
    ElMessage.success('活动相册已创建')
    fetch()
  } catch (error) {
    console.error('创建活动失败:', error)
    ElMessage.error('创建活动失败，请重试')
  }
}

function handleView(id: string) {
  console.log('跳转到活动详情页, ID:', id)
  router.push(`/staff/activity-gallery/${id}`)
}

onMounted(() => {
  console.log('活动相册页面挂载')
  console.log('用户状态:', {
    user: authStore.user,
    isAuthenticated: authStore.isAuthenticated,
    route: route.path
  })
  fetch()
})
</script>

<style scoped>
.activity-gallery-view {
  padding: 16px;
}
</style>


