<template>
  <div class="simple-announcements">
    <h3>简单公告列表测试</h3>
    <div v-if="loading">加载中...</div>
    <div v-else-if="error">错误: {{ error }}</div>
    <div v-else-if="!announcements.length">暂无公告数据</div>
    <div v-else>
      <div v-for="announcement in announcements" :key="announcement.id" class="announcement-item">
        <h4>{{ announcement.title }}</h4>
        <p>{{ announcement.content }}</p>
        <small>发布时间: {{ announcement.publish_time }}</small>

      </div>
    </div>
    
    <div style="margin-top: 20px;">
      <h4>调试信息:</h4>
      <pre>{{ debugInfo }}</pre>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useAnnouncementsStore } from '@/stores/announcements'

const store = useAnnouncementsStore()

const debugInfo = computed(() => ({
  itemsLength: store.items.length,
  loading: store.loading,
  error: store.error
}))

const announcements = computed(() => store.items)
const loading = computed(() => store.loading)
const error = computed(() => store.error)

onMounted(() => {
  console.log('简单公告列表组件挂载')
  store.fetchAnnouncements()
})
</script>

<style scoped>
.simple-announcements {
  padding: 20px;
  background: #f5f5f5;
  margin: 20px;
  border-radius: 8px;
}

.announcement-item {
  background: white;
  padding: 15px;
  margin: 10px 0;
  border-radius: 4px;
  border-left: 3px solid #409eff;
}
</style>