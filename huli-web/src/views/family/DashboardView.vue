<template>
  <div class="dashboard-container">
    <div class="header">
      <h2>欢迎回来，{{ userStore.user?.real_name || userStore.user?.username }}</h2>
    </div>

    <div v-if="loading" class="loading-state">
      <el-skeleton :rows="5" animated />
    </div>

    <div v-else class="dashboard-content">
      <!--1. 院民概况卡片 -->
      <el-card class="patient-card">
        <template #header>
          <div class="card-header">
            <span>院民概况</span>
            <el-tag v-if="dashboardData.patient" type="success">{{ dashboardData.patient.status }}</el-tag>
          </div>
        </template>
        <div v-if="dashboardData.patient" class="patient-info">
          <el-avatar :size="64" :src="dashboardData.patient.avatar || ''" />
          <div class="info-details">
            <h3>{{ dashboardData.patient.name }}</h3>
            <p v-if="dashboardData.patient.room">房间: {{ dashboardData.patient.room.room_number }}</p>
            <p v-if="dashboardData.patient.bed_id">床位号: {{ dashboardData.patient.bed_id }}</p>
            <p>护理等级: {{ dashboardData.patient.care_level }}</p>
            <p>健康评估: {{ dashboardData.patient.health_level }}</p>
          </div>
        </div>
        <div v-else class="empty-state">
          暂无关联院民信息
        </div>
      </el-card>

      <!--2. 快捷入口与统计 -->
      <div class="stats-row">
        <el-card class="stat-card" shadow="hover" @click="$router.push('/family/bills')">
          <div class="stat-content">
            <el-icon :size="24" color="#E6A23C"><Money /></el-icon>
            <div class="stat-text">
              <div class="label">待缴费账单</div>
              <div class="value">{{ dashboardData.unpaid_bills_count || 0 }}</div>
            </div>
          </div>
        </el-card>
        <el-card class="stat-card" shadow="hover" @click="$router.push('/family/messages')">
          <div class="stat-content">
            <el-icon :size="24" color="#409EFF"><ChatDotRound /></el-icon>
            <div class="stat-text">
              <div class="label">消息</div>
              <div class="value">查看</div>
            </div>
          </div>
        </el-card>
         <el-card class="stat-card" shadow="hover" @click="$router.push('/family/appointments')">
          <div class="stat-content">
            <el-icon :size="24" color="#67C23A"><Calendar /></el-icon>
            <div class="stat-text">
              <div class="label">探视预约</div>
              <div class="value">申请</div>
            </div>
          </div>
        </el-card>
      </div>

      <!--3. 最新通知 -->
      <el-card class="notifications-card">
        <template #header>
          <div class="card-header">
            <span>系统通知</span>
            <el-button link type="primary" @click="$router.push('/family/notifications')">查看全部</el-button>
          </div>
        </template>
        <el-timeline v-if="dashboardData.recent_notifications?.length">
          <el-timeline-item
            v-for="(item, index) in dashboardData.recent_notifications"
            :key="index"
            :timestamp="new Date(item.created_at).toLocaleDateString()"
            :type="item.status === 'unread' ? 'primary' : 'info'"
          >
            {{ item.title }}
          </el-timeline-item>
        </el-timeline>
        <div v-else class="empty-state">暂无通知</div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useUserStore } from '@/stores/user';
import { getFamilyDashboard } from '@/services/patients';
import { Money, ChatDotRound, Calendar } from '@element-plus/icons-vue';

const userStore = useUserStore();
const loading = ref(true);
const dashboardData = ref<any>({});

onMounted(async () => {
  try {
    const res = await getFamilyDashboard();
    dashboardData.value = res;
  } catch (error) {
    console.error(error);
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}

.header {
  margin-bottom: 20px;
  padding: 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 8px;
  color: white;
}

.header h2 {
  margin: 0;
  font-size: 24px;
}

.dashboard-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.patient-card {
  flex: 1;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.patient-info {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
}

.patient-info h3 {
  margin: 0 0 8px 0;
}

.patient-info p {
  margin: 4px 0;
  color: #666;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.stat-card {
  cursor: pointer;
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.stat-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 20px;
}

.stat-text {
  text-align: center;
}

.stat-text .label {
  font-size: 14px;
  color: #666;
}

.stat-text .value {
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
}

.notifications-card {
  flex: 1;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #999;
}
</style>
