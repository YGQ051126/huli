<template>
  <div class="staff-messages-view">
    <el-page-header content="在线沟通" />

    <el-row :gutter="16" style="margin-top: 16px">
      <el-col :span="8">
        <el-card>
          <template #header>
            <span>选择家属</span>
          </template>
          
          <!-- 家属用户选择器 -->
          <div class="family-selector">
            <el-select
              v-model="receiverId"
              placeholder="请选择家属用户"
              style="width: 100%; margin-bottom: 8px"
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
              size="small" 
              @click="fetch" 
              :disabled="!receiverId"
              style="width: 100%"
            >
              加载消息
            </el-button>
          </div>
          
          <!-- 当前选择的家属信息 -->
          <div v-if="receiverName" class="selected-family-info">
            <el-divider />
            <p>当前沟通对象：<strong>{{ receiverName }}</strong></p>
            <p>用户ID：<code>{{ receiverId }}</code></p>
          </div>
          
        </el-card>
      </el-col>
      
      <el-col :span="16">
        <CommunicationPanel
          :messages="messages"
          :loading="loading"
          :receiver-id="receiverId"
          @send="handleSend"
        />
      </el-col>
    </el-row>
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
    console.log('=== 开始加载家属用户列表 ===')
    console.log('当前用户token:', localStorage.getItem('access_token'))
    console.log('当前用户认证状态:', authStore.isAuthenticated)
    console.log('当前用户信息:', authStore.user)
    
    // 先尝试通过family-users API获取
    console.log('尝试调用getFamilyUsers...')
    let users = await getFamilyUsers()
    console.log('getFamilyUsers返回结果:', users)
    console.log('getFamilyUsers返回用户数:', users.length)
    
    // 如果获取失败或返回为空，尝试备用方案
    if (!users || users.length === 0) {
      console.log('主要方法返回空，尝试备用方案getAllUsersAndFilterFamily...')
      users = await getAllUsersAndFilterFamily()
      console.log('备用方案返回结果:', users)
      console.log('备用方案返回用户数:', users.length)
    }
    
    familyUsers.value = users
    console.log('最终设置的用户列表:', familyUsers.value)
    console.log('最终设置的用户数:', familyUsers.value.length)
    
    if (users.length === 0) {
      console.warn('没有获取到任何家属用户数据')
      ElMessage.warning('暂无家属用户数据，请检查网络连接或联系管理员')
    } else {
      console.log('? 成功加载家属用户数据')
      ElMessage.success(`成功加载 ${users.length} 个家属用户`)
    }
  } catch (error: any) {
    console.error('? 加载家属用户失败:', error)
    console.error('错误详情:', error)
    ElMessage.error('加载家属用户失败: ' + (error.message || '未知错误'))
    
    // 显示更详细的错误信息
    if (error.response) {
      console.error('响应错误:', error.response.data)
      console.error('状态码:', error.response.status)
      console.error('响应头:', error.response.headers)
    } else if (error.request) {
      console.error('请求错误:', error.request)
    } else {
      console.error('配置错误:', error.message)
    }
    console.error('错误配置:', error.config)
  } finally {
    loadingFamilies.value = false
    console.log('=== 家属用户加载完成 ===')
  }
}

// 处理家属选择变化
function handleFamilyChange(value: string) {
  // 切换用户时立即清空消息列表，避免显示上一位用户的消息
  messages.value = []
  
  if (value) {
    const selectedUser = familyUsers.value.find(user => String(user.id) === value)
    if (selectedUser) {
      receiverName.value = selectedUser.real_name || selectedUser.username
      // 自动加载消息
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
    console.error('Failed to load messages:', error)
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
    console.error('Failed to send message:', error)
  }
}

// 初次加载家属用户列表
onMounted(() => {
  console.log('MessagesView组件挂载完成')
  console.log('当前路由:', window.location.href)
  console.log('localStorage中的token:', localStorage.getItem('access_token'))
  console.log('当前用户认证状态:', authStore.isAuthenticated)
  console.log('当前用户信息:', authStore.user)
  
  // 检查是否有token和用户认证
  if (!authStore.isAuthenticated) {
    console.warn('用户未认证，请先登录')
    ElMessage.warning('请先登录系统')
    return
  }
  
  console.log('开始加载家属用户列表...')
  loadFamilyUsers()
})
</script>

<style scoped>
.staff-messages-view {
  padding: 16px;
}

.family-selector {
  margin-bottom: 16px;
}

.user-option {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-name {
  font-weight: 500;
}

.user-username {
  color: #909399;
  font-size: 12px;
}

.selected-family-info {
  margin-top: 16px;
  font-size: 14px;
  color: #606266;
}

.selected-family-info strong {
  color: #303133;
}

.selected-family-info code {
  background-color: #f4f4f5;
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 12px;
}
</style>