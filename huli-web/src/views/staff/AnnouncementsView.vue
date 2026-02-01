<template>
  <div class="announcements-view">
    <el-page-header content="公告中心" />
    <div style="margin-top: 16px">
      <AnnouncementList
        :announcements="announcements"
        :loading="loading"
        @refresh="fetch"
        @read="showDetail"
      />
    </div>
    
    <!-- 公告详情对话框 -->
    <AnnouncementDetail
      v-model="showDetailDialog"
      :announcement-id="selectedAnnouncementId"
      @read="handleRead"
    />
  </div>
</template>

<script setup lang="ts">
import { onMounted, computed, ref } from 'vue'
import AnnouncementList from '@/components/business/AnnouncementList.vue'
import AnnouncementDetail from '@/components/business/AnnouncementDetail.vue'
import { useAnnouncementsStore } from '@/stores/announcements'

const store = useAnnouncementsStore()

// 状态管理
const showDetailDialog = ref(false)
const selectedAnnouncementId = ref<string | number | null>(null)

// 从store中获取数据
const announcements = computed(() => store.items)
const loading = computed(() => store.loading)

// 获取公告列表
const fetch = () => store.fetchAnnouncements()

// 显示公告详情
const showDetail = (id: string | number) => {
  selectedAnnouncementId.value = id
  showDetailDialog.value = true
}

// 处理公告已读（简化版本，仅显示详情）
const handleRead = (id: string | number) => {
  console.log('查看公告详情:', id)
  // 不再处理已读状态，仅显示详情
}

// 初始加载
onMounted(() => {
  console.log('公告视图组件挂载，开始获取公告...')
  fetch()
})
</script>

<style scoped>
.announcements-view {
  padding: 16px;
}
</style>