<template>
  <div class="services-view">
    <div class="page-header">
      <h2>个性化服务管理</h2>
    </div>

    <el-card>
      <el-tabs v-model="activeTab" @tab-click="handleTabClick">
        <!-- Tab 1: Service Types -->
        <el-tab-pane label="服务项目管理" name="types">
          <div class="toolbar">
            <el-button type="primary" :icon="Plus" @click="openServiceDialog()">新增服务</el-button>
          </div>
          <el-table :data="serviceTypes" v-loading="loadingTypes" stripe>
            <el-table-column prop="name" label="服务名称" />
            <el-table-column prop="service_type" label="类型">
              <template #default="scope">{{ formatServiceType(scope.row.service_type) }}</template>
            </el-table-column>
            <el-table-column prop="price" label="价格">
              <template #default="scope">?{{ scope.row.price }}</template>
            </el-table-column>
            <el-table-column prop="description" label="描述" show-overflow-tooltip />
            <el-table-column label="操作" width="180">
              <template #default="scope">
                <el-button link type="primary" @click="openServiceDialog(scope.row)">编辑</el-button>
                <el-button link type="danger" @click="handleDeleteService(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <!-- Tab 2: Orders -->
        <el-tab-pane label="订单管理" name="orders">
          <el-table :data="orders" v-loading="loadingOrders" stripe>
            <el-table-column prop="order_no" label="订单号" width="150" />
            <el-table-column prop="family_name" label="家属" width="100" />
            <el-table-column prop="patient_name" label="老人" width="100" />
            <el-table-column prop="total_amount" label="金额" width="100" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="scope">
                <el-tag :type="getStatusType(scope.row.status)">{{ formatStatus(scope.row.status) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="paid_at" label="支付时间" width="160">
              <template #default="scope">{{ formatDate(scope.row.paid_at) }}</template>
            </el-table-column>
            <el-table-column label="服务项">
              <template #default="scope">
                <el-tag v-for="item in scope.row.items" :key="item.id" size="small" class="mr-1">
                  {{ item.service_name }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <!-- Tab 3: Stats -->
        <el-tab-pane label="统计报表" name="stats">
          <div class="stats-container">
            <div class="toolbar">
              <el-button type="success" :icon="Download" @click="exportStats">导出报表</el-button>
            </div>
            <div ref="chartRef" style="width: 100%; height: 400px;"></div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <!-- Service Dialog -->
    <el-dialog v-model="showServiceDialog" :title="editingService ? '编辑服务' : '新增服务'" width="500px">
      <el-form :model="serviceForm" label-width="80px">
        <el-form-item label="名称">
          <el-input v-model="serviceForm.name" />
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="serviceForm.service_type">
            <el-option label="日常护理" value="daily" />
            <el-option label="医疗服务" value="medical" />
            <el-option label="娱乐活动" value="recreation" />
            <el-option label="个性化服务" value="custom" />
            <el-option label="咨询服务" value="consultation" />
          </el-select>
        </el-form-item>
        <el-form-item label="价格">
          <el-input-number v-model="serviceForm.price" :precision="2" :step="10" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="serviceForm.description" type="textarea" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showServiceDialog = false">取消</el-button>
          <el-button type="primary" @click="submitService">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Plus, Download } from '@element-plus/icons-vue';
import * as echarts from 'echarts';
import { 
  getServiceTypes, getServiceOrders, getServiceStats, 
  createServiceType, updateServiceType, deleteServiceType,
  type ServiceType, type ServiceOrder 
} from '@/services/services';

const activeTab = ref('types');
const loadingTypes = ref(false);
const loadingOrders = ref(false);

const serviceTypes = ref<ServiceType[]>([]);
const orders = ref<ServiceOrder[]>([]);
const statsData = ref<any[]>([]);

const showServiceDialog = ref(false);
const editingService = ref<ServiceType | null>(null);
const serviceForm = ref({
  name: '',
  service_type: 'custom',
  price: 0,
  description: ''
});

const chartRef = ref<HTMLElement | null>(null);
let chartInstance: echarts.ECharts | null = null;

onMounted(() => {
  fetchTypes();
});

const handleTabClick = (tab: any) => {
  if (tab.props.name === 'orders') {
    fetchOrders();
  } else if (tab.props.name === 'stats') {
    fetchStats();
  }
};

// Types
const fetchTypes = async () => {
  loadingTypes.value = true;
  try {
    const res = await getServiceTypes();
    serviceTypes.value = Array.isArray(res) ? res : (res as any).results || [];
  } catch (e) {
    console.error(e);
  } finally {
    loadingTypes.value = false;
  }
};

const openServiceDialog = (service?: ServiceType) => {
  if (service) {
    editingService.value = service;
    serviceForm.value = { ...service };
  } else {
    editingService.value = null;
    serviceForm.value = { name: '', service_type: 'custom', price: 0, description: '' };
  }
  showServiceDialog.value = true;
};

const submitService = async () => {
  try {
    if (editingService.value) {
      await updateServiceType(editingService.value.id, serviceForm.value);
      ElMessage.success('更新成功');
    } else {
      await createServiceType(serviceForm.value);
      ElMessage.success('创建成功');
    }
    showServiceDialog.value = false;
    fetchTypes();
  } catch (e) {
    ElMessage.error('操作失败');
  }
};

const handleDeleteService = async (service: ServiceType) => {
  try {
    await ElMessageBox.confirm('确定删除该服务吗？', '提示', { type: 'warning' });
    await deleteServiceType(service.id);
    ElMessage.success('删除成功');
    fetchTypes();
  } catch (e) {
    // Cancelled or error
  }
};

// Orders
const fetchOrders = async () => {
  loadingOrders.value = true;
  try {
    const res = await getServiceOrders();
    orders.value = Array.isArray(res) ? res : (res as any).results || [];
  } catch (e) {
    console.error(e);
  } finally {
    loadingOrders.value = false;
  }
};

// Stats
const fetchStats = async () => {
  try {
    const res = await getServiceStats();
    statsData.value = Array.isArray(res) ? res : (res as any).results || [];
    renderChart();
  } catch (e) {
    console.error(e);
  }
};

const renderChart = () => {
  nextTick(() => {
    if (chartRef.value) {
      if (!chartInstance) {
        chartInstance = echarts.init(chartRef.value);
      }
      
      const dates = statsData.value.map(d => formatMonth(d.month));
      const values = statsData.value.map(d => d.total);
      
      const option = {
        title: { text: '个性化服务月度收入统计' },
        tooltip: { trigger: 'axis' },
        xAxis: { type: 'category', data: dates },
        yAxis: { type: 'value' },
        series: [{ data: values, type: 'bar', itemStyle: { color: '#409eff' } }]
      };
      
      chartInstance.setOption(option);
    }
  });
};

const exportStats = () => {
  if (statsData.value.length === 0) {
    ElMessage.warning('暂无数据可导出');
    return;
  }
  
  const header = ['月份', '总收入'];
  const rows = statsData.value.map(d => [
    formatMonth(d.month),
    d.total
  ]);
  
  const csvContent = [
    header.join(','),
    ...rows.map(row => row.join(','))
  ].join('\n');
  
  const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = `服务收入统计_${new Date().toLocaleDateString()}.csv`;
  link.click();
};

// Helpers
const formatServiceType = (type: string) => {
  const map: Record<string, string> = {
    'daily': '日常护理',
    'medical': '医疗服务',
    'recreation': '娱乐活动',
    'custom': '个性化服务',
    'consultation': '咨询服务'
  };
  return map[type] || type;
};

const formatStatus = (status: string) => {
  const map: Record<string, string> = {
    'pending': '待处理',
    'processing': '进行中',
    'completed': '已完成',
    'rated': '已评价',
    'cancelled': '已取消'
  };
  return map[status] || status;
};

const getStatusType = (status: string) => {
  const map: Record<string, string> = {
    'pending': 'warning',
    'processing': 'primary',
    'completed': 'success',
    'rated': 'info',
    'cancelled': 'danger'
  };
  return map[status] || 'info';
};

const formatDate = (dateStr: string) => {
  if (!dateStr) return '';
  return new Date(dateStr).toLocaleString();
};

const formatMonth = (dateStr?: string) => {
  if (!dateStr) return '';
  // Try to handle YYYY-MM-DD manually to avoid timezone issues
  const match = dateStr.match(/^(\d{4})-(\d{2})/);
  if (match) {
    return `${match[1]}年${parseInt(match[2] || '0')}月`;
  }
  const date = new Date(dateStr);
  if (isNaN(date.getTime())) return dateStr;
  return `${date.getFullYear()}年${date.getMonth() + 1}月`;
};
</script>

<style scoped>
.services-view {
  padding: 20px;
}
.page-header {
  margin-bottom: 20px;
}
.toolbar {
  margin-bottom: 20px;
}
.mr-1 {
  margin-right: 4px;
}
</style>
