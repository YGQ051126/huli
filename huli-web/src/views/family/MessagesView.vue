<template>
  <div class="family-messages-view">
    <el-page-header content="消息中心" />

    <el-row :gutter="16" style="margin-top: 16px">
      <!-- 家属端主要与护理人员沟通，可能不需要选择列表，或者选择特定的负责员工 -->
      <!-- 暂时简化为直接显示沟通面板，默认与负责的护工或管理员沟通 -->
      <!-- 或者左侧显示工作人员列表 -->
      <el-col :span="8">
        <el-card>
          <template #header>
            <span>工作人员</span>
          </template>
          
          <div class="staff-list">
             <!-- 这里暂时模拟或者列出相关工作人员 -->
             <!-- 实际项目中应该调用API获取关联的护工/医生 -->
             <div 
               v-for="staff in staffList" 
               :key="staff.id"
               class="staff-item"
               :class="{ active: receiverId === String(staff.id) }"
               @click="handleStaffSelect(staff)"
             >
               <el-avatar :size="36" :src="staff.avatar || ''">{{ staff.real_name?.[0] }}</el-avatar>
               <div class="staff-info">
                 <div class="staff-name">{{ staff.real_name }}</div>
                 <div class="staff-role">{{ staff.role === 'staff' ? '护理人员' : '管理员' }}</div>
               </div>
             </div>
             <el-empty v-if="staffList.length === 0" description="暂无关联工作人员" />
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="16">
        <CommunicationPanel
          v-if="receiverId"
          :messages="messages"
          :loading="loading"
          :receiver-id="receiverId"
          @send="handleSend"
        />
        <el-empty v-else description="请选择工作人员开始沟通" />
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import CommunicationPanel from '@/components/business/CommunicationPanel.vue'
import { getStaffMessages, sendStaffMessage, type Message, type CreateMessageData } from '@/services/messages'
import { getRelatedStaff } from '@/services/users'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const receiverId = ref('')
const receiverName = ref('')
const messages = ref<Message[]>([])
const loading = ref(false)
const staffList = ref<any[]>([]) // 工作人员列表

// 获取关联工作人员
async function loadRelatedStaff() {
  try {
    const res = await getRelatedStaff()
    staffList.value = res
  } catch (error) {
    console.error('加载工作人员失败:', error)
    ElMessage.error('加载联系人失败')
  }
}

function handleStaffSelect(staff: any) {
  receiverId.value = String(staff.id)
  receiverName.value = staff.real_name
  messages.value = [] // 切换时清空
  fetch()
}

async function fetch() {
  if (!receiverId.value) return
  
  loading.value = true
  try {
    // 复用获取消息的API
    // 注意：getStaffMessages 实际上是获取"与某人的聊天记录"
    // 对于家属来说，调用同样的接口，传入对方ID即可
    messages.value = await getStaffMessages(receiverId.value)
  } catch (error) {
    ElMessage.error('加载消息失败')
    console.error('Failed to load messages:', error)
  } finally {
    loading.value = false
  }
}

async function handleSend(data: CreateMessageData) {
  if (!receiverId.value) {
    ElMessage.warning('请先选择工作人员')
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

onMounted(() => {
  if (!authStore.isAuthenticated) {
    ElMessage.warning('请先登录系统')
    return
  }
  loadRelatedStaff()
})
</script>

<style scoped>
.family-messages-view {
  padding: 16px;
}

.staff-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.staff-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.staff-item:hover {
  background-color: #f5f7fa;
}

.staff-item.active {
  background-color: #e6f7ff;
}

.staff-info {
  display: flex;
  flex-direction: column;
}

.staff-name {
  font-weight: 500;
  font-size: 14px;
}

.staff-role {
  font-size: 12px;
  color: #909399;
}
</style>
