<template>
  <div class="alerts-view">
    <el-page-header content="告警与系统通知" />
    <div style="margin-top: 16px">
      <NotificationList
        :notifications="notifications"
        :loading="loading"
        :unread-count="unreadCount"
        @refresh="fetch"
        @clear="clearAll"
        @read="markRead"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, computed } from 'vue'
import NotificationList from '@/components/business/NotificationList.vue'
import { useNotificationsStore } from '@/stores/notifications'

const store = useNotificationsStore()

const notifications = computed(() => store.items)
const loading = computed(() => store.loading)
const unreadCount = computed(() => store.unreadCount)

const fetch = () => store.fetchNotifications()
const clearAll = () => store.clearAll()
const markRead = (id: string) => store.markRead(id)

onMounted(fetch)
</script>

<style scoped>
.alerts-view {
  padding: 16px;
}
</style>


