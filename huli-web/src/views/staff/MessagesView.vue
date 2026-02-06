<template>
  <div class="staff-messages-view">
    <div class="page-header-wrapper">
      <el-page-header content="在线沟通" icon="" title="工作台" />
    </div>

    <div class="layout-container">
      <!-- Left Sidebar: Family Selector -->
      <aside class="sidebar">
        <el-card class="sidebar-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>选择家属</span>
            </div>
          </template>
          
          <div class="family-selector">
            <el-select
              v-model="receiverId"
              placeholder="搜索或选择家属..."
              class="custom-select"
              clearable
              filterable
              :loading="loadingFamilies"
              @change="handleFamilyChange"
            >
              <el-option
                v-for="user in familyUsers"
                :key="user.id"
                :label="`${user.real_name} (${user.username})`"
                :value="String(user.id)"
              >
                <div class="user-option">
                  <span class="user-name">{{ user.real_name }}</span>
                  <span class="user-username">{{ user.username }}</span>
                </div>
              </el-option>
            </el-select>
            
            <el-button 
              type="primary" 
              class="load-btn"
              @click="fetch" 
              :disabled="!receiverId"
              round
            >
              加载消息
            </el-button>
          </div>
        </el-card>
      </aside>
      
      <!-- Main Content: Chat Panel -->
      <main class="main-content">
        <CommunicationPanel
          :messages="messages"
          :loading="loading"
          :receiver-id="receiverId"
          @send="handleSend"
        />
      </main>

      <!-- Right Aux Panel: Info (Only visible on large screens) -->
      <aside class="aux-panel" v-if="receiverId">
        <el-card class="info-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>当前会话</span>
            </div>
          </template>
          <div class="user-info-detail">
            <el-avatar :size="64" class="info-avatar">{{ (receiverName || 'U').charAt(0).toUpperCase() }}</el-avatar>
            <h3 class="info-name">{{ receiverName }}</h3>
            <p class="info-id">ID: {{ receiverId }}</p>
            <el-divider />
            <div class="info-meta">
              <p>状态: <span class="status-online">在线</span></p>
              <p>角色: 家属</p>
            </div>
          </div>
        </el-card>
      </aside>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import CommunicationPanel from '@/components/business/CommunicationPanel.vue'
import { getStaffMessages, sendStaffMessage, type Message, type CreateMessageData } from '@/services/messages'
import { getFamilyUsers, getAllUsersAndFilterFamily } from '@/services/users'
import type { User } from '@/types/user'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const receiverId = ref('')
const receiverName = ref('')
const messages = ref<Message[]>([])
const loading = ref(false)
const familyUsers = ref<User[]>([])
const loadingFamilies = ref(false)

// 加载家属用户列表
async function loadFamilyUsers() {
  loadingFamilies.value = true
  try {
    let users = await getFamilyUsers()
    if (!users || users.length === 0) {
      users = await getAllUsersAndFilterFamily()
    }
    familyUsers.value = users
  } catch (error: any) {
    console.error('加载家属用户失败:', error)
    ElMessage.error('加载家属用户失败')
  } finally {
    loadingFamilies.value = false
  }
}

// 处理家属选择变化
function handleFamilyChange(value: string) {
  messages.value = []
  if (value) {
    const selectedUser = familyUsers.value.find(user => String(user.id) === value)
    if (selectedUser) {
      receiverName.value = selectedUser.real_name || selectedUser.username
      fetch()
    }
  } else {
    receiverName.value = ''
  }
}

async function fetch() {
  if (!receiverId.value) {
    ElMessage.warning('请先选择家属用户')
    return
  }
  loading.value = true
  try {
    messages.value = await getStaffMessages(receiverId.value)
    if (messages.value.length === 0) {
      ElMessage.info('暂无消息记录，开始新的对话吧！')
    }
  } catch (error) {
    ElMessage.error('加载消息失败')
  } finally {
    loading.value = false
  }
}

async function handleSend(data: CreateMessageData) {
  if (!receiverId.value) {
    ElMessage.warning('请先选择家属用户')
    return
  }
  
  try {
    const msg = await sendStaffMessage(data)
    messages.value.push(msg)
    ElMessage.success('消息已发送')
  } catch (error) {
    ElMessage.error('发送消息失败')
  }
}

// 初次加载家属用户列表
onMounted(() => {
  if (!authStore.isAuthenticated) {
    return
  }
  loadFamilyUsers()
})
</script>

<style scoped>
.staff-messages-view {
  padding: 24px;
  max-width: 1600px;
  margin: 0 auto;
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  color: #303133;
}

.page-header-wrapper {
  margin-bottom: 24px;
}

/* Layout Grid */
.layout-container {
  display: grid;
  gap: 24px;
  align-items: start;
}

/* Large Screens: 3 Columns */
@media (min-width: 1200px) {
  .layout-container {
    grid-template-columns: 240px 1fr 280px;
  }
}

/* Medium Screens: 2 Columns (Hide Aux) */
@media (min-width: 992px) and (max-width: 1199px) {
  .layout-container {
    grid-template-columns: 240px 1fr;
  }
  .aux-panel {
    display: none;
  }
}

/* Small Screens: 1 Column (Sidebar stacked) */
@media (max-width: 991px) {
  .layout-container {
    grid-template-columns: 1fr;
  }
  .sidebar {
    margin-bottom: 16px;
  }
  .aux-panel {
    display: none;
  }
}

/* Card Styles */
.sidebar-card, .info-card {
  border-radius: 8px;
  border: none;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
}

.card-header {
  font-weight: 600;
  font-size: 16px;
}

/* Sidebar Components */
.family-selector {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.custom-select {
  width: 100%;
}

.load-btn {
  width: 100%;
  transition: all 0.2s ease-out;
}

.load-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}

/* User Option */
.user-option {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-name {
  font-weight: 500;
  color: #303133;
}

.user-username {
  color: #909399;
  font-size: 12px;
}

/* Aux Panel Info */
.user-info-detail {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16px 0;
}

.info-avatar {
  background-color: #E6A23C;
  font-size: 24px;
  margin-bottom: 16px;
  box-shadow: 0 4px 12px rgba(230, 162, 60, 0.3);
}

.info-name {
  margin: 0 0 8px;
  font-size: 18px;
  font-weight: 600;
}

.info-id {
  margin: 0;
  font-family: 'Roboto', sans-serif;
  color: #909399;
  font-size: 14px;
}

.info-meta {
  width: 100%;
  text-align: left;
  font-size: 14px;
  color: #606266;
}

.info-meta p {
  margin: 8px 0;
  display: flex;
  justify-content: space-between;
}

.status-online {
  color: #67C23A;
  font-weight: 500;
}
</style>