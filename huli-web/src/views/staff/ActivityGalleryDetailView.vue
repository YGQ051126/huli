<template>
  <div class="activity-gallery-detail">
    <el-page-header content="活动详情" @back="handleBack" />
    <el-card style="margin-top: 16px">
      <el-skeleton v-if="loading" :rows="6" animated />
      <div v-else>
        <div class="header">
          <div class="title">{{ activity?.title }}</div>
          <el-tag type="info" size="small">{{ activity?.activityDate }}</el-tag>
        </div>
        <div v-if="activity?.description" class="description">
          {{ activity.description }}
        </div>
        <el-empty v-else description="暂无描述" />
        <div class="section-title">活动相册</div>
        <el-skeleton v-if="mediaLoading" :rows="4" animated />
        <div v-else class="media-grid">
          <el-empty v-if="!mediaList.length" description="暂无媒体文件" />
          <div v-else class="media-list">
            <div
              v-for="(item, index) in mediaList"
              :key="item.id || index"
              class="media-item-wrapper"
            >
              <video
                v-if="item.fileType === 'video'"
                class="media-content"
                :src="item.fileUrl"
                controls
                preload="metadata"
              ></video>
              <el-image
                v-else
                class="media-content"
                :src="item.fileUrl"
                :preview-src-list="imageUrls"
                :initial-index="getImageIndex(item.fileUrl)"
                fit="cover"
                :lazy="true"
              >
                <template #error>
                  <div class="image-slot">
                    <el-icon><Picture /></el-icon>
                    <span>加载失败</span>
                  </div>
                </template>
                <template #placeholder>
                  <div class="image-slot loading">
                    <el-icon class="is-loading"><Loading /></el-icon>
                    <span>加载中...</span>
                  </div>
                </template>
              </el-image>
            </div>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Picture, Loading } from '@element-plus/icons-vue'
import { getActivityDetail, getActivityMedia, type ActivityGallery, type ActivityMedia } from '@/services/activity-gallery'

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const mediaLoading = ref(false)
const activity = ref<ActivityGallery | null>(null)
const mediaList = ref<ActivityMedia[]>([])

const activityId = computed(() => String(route.params.id || ''))
const imageUrls = computed(() =>
  mediaList.value
    .filter(item => item.fileType === 'image' && item.fileUrl)
    .map(item => item.fileUrl)
)

function getImageIndex(url: string) {
  return imageUrls.value.indexOf(url)
}

function handleBack() {
  router.push('/staff/activity-gallery')
}

async function fetchDetail() {
  if (!activityId.value) return
  loading.value = true
  try {
    activity.value = await getActivityDetail(activityId.value)
  } catch (error) {
    console.error('获取详情失败:', error)
    ElMessage.error('获取活动详情失败')
  } finally {
    loading.value = false
  }
}

async function fetchMedia() {
  if (!activityId.value) return
  mediaLoading.value = true
  try {
    mediaList.value = await getActivityMedia(activityId.value)
  } catch (error) {
    console.error('获取媒体失败:', error)
    ElMessage.error('获取媒体列表失败')
  } finally {
    mediaLoading.value = false
  }
}

async function fetchAll() {
  await Promise.all([fetchDetail(), fetchMedia()])
}

onMounted(fetchAll)

watch(activityId, () => {
  fetchAll()
})
</script>

<style scoped>
.activity-gallery-detail {
  padding: 16px;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.title {
  font-size: 18px;
  font-weight: 600;
}

.description {
  margin-bottom: 16px;
  color: #666;
  line-height: 1.6;
}

.section-title {
  font-weight: 600;
  margin: 16px 0 12px;
}

.media-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 12px;
}

.media-item-wrapper {
  width: 100%;
  height: 160px;
  border-radius: 6px;
  overflow: hidden;
  background: #000; /* Black background for videos */
}

.media-content {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.image-slot {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  background: #f5f7fa;
  color: #909399;
  font-size: 14px;
}

.image-slot .el-icon {
  font-size: 24px;
  margin-bottom: 8px;
}

.image-slot.loading {
  color: #409eff;
}
</style>
