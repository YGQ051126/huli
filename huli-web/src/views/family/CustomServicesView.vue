<template>
  <div class="custom-services-view">
    <div class="page-header">
      <h2>个性化服务定制</h2>
      <p class="subtitle">为您的家人提供专属的额外照护服务</p>
    </div>

    <el-tabs v-model="activeTab" class="service-tabs">
      <!-- Tab 1: Service Catalog -->
      <el-tab-pane label="服务订购" name="catalog">
        <div class="catalog-container">
          <!-- Patient Selector -->
          <div class="patient-selector" v-if="patients.length > 0">
            <span class="label">服务对象：</span>
            <el-radio-group v-model="selectedPatientId">
              <el-radio-button v-for="p in patients" :key="p.id" :label="p.id">
                {{ p.name }}
              </el-radio-button>
            </el-radio-group>
          </div>
          <el-alert v-else title="未找到关联的老人信息" type="warning" show-icon :closable="false" />

          <!-- Service List -->
          <div class="service-list" v-loading="loadingServices">
            <el-row :gutter="20">
              <el-col :span="8" v-for="service in serviceTypes" :key="service.id">
                <el-card 
                  class="service-card" 
                  :class="{ 'is-selected': selectedServiceIds.includes(service.id) }"
                  @click="toggleService(service.id)"
                  shadow="hover"
                >
                  <div class="card-header">
                    <span class="service-name">{{ service.name }}</span>
                    <el-checkbox 
                      :model-value="selectedServiceIds.includes(service.id)" 
                      @change="toggleService(service.id)"
                      class="service-checkbox"
                      @click.stop
                    >&nbsp;</el-checkbox>
                  </div>
                  <div class="service-desc">{{ service.description }}</div>
                  <div class="service-footer">
                    <span class="service-type">
                      <el-tag size="small">{{ formatServiceType(service.service_type) }}</el-tag>
                    </span>
                    <span class="service-price">?{{ service.price }}</span>
                  </div>
                </el-card>
              </el-col>
            </el-row>
          </div>

          <!-- Bottom Bar -->
          <div class="bottom-bar">
            <div class="total-info">
              <span>已选服务: {{ selectedServiceIds.length }} 项</span>
              <span class="total-price">总计: <span class="price-num">?{{ totalAmount }}</span></span>
            </div>
            <el-button 
              type="primary" 
              size="large" 
              :disabled="selectedServiceIds.length === 0 || !selectedPatientId"
              @click="handlePay"
            >
              立即支付
            </el-button>
          </div>
        </div>
      </el-tab-pane>

      <!-- Tab 2: Order History -->
      <el-tab-pane label="订单记录" name="history">
        <el-table :data="orders" v-loading="loadingOrders" stripe style="width: 100%">
          <el-table-column prop="order_no" label="订单号" width="180" />
          <el-table-column prop="patient_name" label="服务对象" width="120" />
          <el-table-column label="服务内容">
            <template #default="scope">
              <el-tag v-for="item in scope.row.items" :key="item.id" size="small" style="margin-right: 5px">
                {{ item.service_name }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="total_amount" label="总金额" width="120">
            <template #default="scope">?{{ scope.row.total_amount }}</template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="120">
            <template #default="scope">
              <el-tag :type="getStatusType(scope.row.status)">{{ formatStatus(scope.row.status) }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="下单时间" width="180">
            <template #default="scope">{{ formatDate(scope.row.created_at) }}</template>
          </el-table-column>
          <el-table-column label="操作" width="150" fixed="right">
            <template #default="scope">
              <el-button 
                v-if="['completed', 'rated'].includes(scope.row.status)" 
                link type="primary" 
                @click="viewFeedback(scope.row)"
              >
                查看反馈
              </el-button>
              <el-button 
                v-if="scope.row.status === 'completed'" 
                link type="warning" 
                @click="openReview(scope.row)"
              >
                去评价
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>

    <!-- Payment Confirm Dialog -->
    <el-dialog v-model="showPaymentDialog" title="支付确认" width="500px">
      <div class="payment-confirm">
        <div class="confirm-item">
          <span class="label">服务对象：</span>
          <span class="value">{{ getPatientName(selectedPatientId) }}</span>
        </div>
        <div class="confirm-item">
          <span class="label">服务清单：</span>
          <div class="value-list">
            <div v-for="s in selectedServicesList" :key="s.id">
              {{ s.name }} (?{{ s.price }})
            </div>
          </div>
        </div>
        <div class="confirm-item total">
          <span class="label">支付总额：</span>
          <span class="value price">?{{ totalAmount }}</span>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showPaymentDialog = false">取消</el-button>
          <el-button type="primary" :loading="submittingOrder" @click="confirmPay">确认支付</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- Feedback View Dialog -->
    <el-dialog v-model="showFeedbackDialog" title="服务反馈" width="600px">
      <div v-if="currentOrder?.feedback" class="feedback-detail">
        <div class="feedback-info">
          <span class="staff">执行员工：{{ currentOrder.feedback.staff_name || '工作人员' }}</span>
          <span class="time">{{ formatDate(currentOrder.feedback.created_at) }}</span>
        </div>
        <div class="feedback-content">{{ currentOrder.feedback.content }}</div>
        <div class="feedback-images" v-if="currentOrder.feedback.images && currentOrder.feedback.images.length">
          <el-image 
            v-for="img in currentOrder.feedback.images" 
            :key="img.id" 
            :src="img.image" 
            :preview-src-list="currentOrder.feedback.images.map((i: any) => i.image)"
            fit="cover"
            class="feedback-img"
          />
        </div>
      </div>
      <div v-else class="no-data">暂无反馈信息</div>
    </el-dialog>

    <!-- Review Dialog -->
    <el-dialog v-model="showReviewDialog" title="服务评价" width="500px">
      <el-form :model="reviewForm" label-width="80px">
        <el-form-item label="评分">
          <el-rate v-model="reviewForm.rating" />
        </el-form-item>
        <el-form-item label="评价内容">
          <el-input v-model="reviewForm.comment" type="textarea" rows="4" placeholder="请输入您的评价..." />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showReviewDialog = false">取消</el-button>
          <el-button type="primary" :loading="submittingReview" @click="submitReviewForm">提交评价</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import { 
  getServiceTypes, getServiceOrders, createServiceOrder, submitServiceReview,
  type ServiceType, type ServiceOrder 
} from '@/services/services';
import { getPatients } from '@/services/patients';
import type { Patient } from '@/types/patient';

const activeTab = ref('catalog');
const loadingServices = ref(false);
const loadingOrders = ref(false);
const submittingOrder = ref(false);
const submittingReview = ref(false);

const serviceTypes = ref<ServiceType[]>([]);
const orders = ref<ServiceOrder[]>([]);
const patients = ref<Patient[]>([]);

const selectedPatientId = ref<string | number | null>(null);
const selectedServiceIds = ref<number[]>([]);

const showPaymentDialog = ref(false);
const showFeedbackDialog = ref(false);
const showReviewDialog = ref(false);

const currentOrder = ref<ServiceOrder | null>(null);
const reviewForm = ref({ rating: 5, comment: '' });

// Fetch Data
const fetchData = async () => {
  loadingServices.value = true;
  try {
    const [servicesRes, patientsRes] = await Promise.all([
      getServiceTypes(),
      getPatients()
    ]);
    // Handle potential paginated response or direct array
    serviceTypes.value = Array.isArray(servicesRes) ? servicesRes : (servicesRes as any).results || [];
    patients.value = Array.isArray(patientsRes) ? patientsRes : (patientsRes as any).results || [];
    
    if (patients.value.length > 0) {
      selectedPatientId.value = patients.value[0]?.id ?? null;
    }
  } catch (error) {
    console.error(error);
    ElMessage.error('加载数据失败');
  } finally {
    loadingServices.value = false;
  }
};

const fetchOrders = async () => {
  loadingOrders.value = true;
  try {
    const res = await getServiceOrders();
    orders.value = Array.isArray(res) ? res : (res as any).results || [];
  } catch (error) {
    console.error(error);
  } finally {
    loadingOrders.value = false;
  }
};

onMounted(() => {
  fetchData();
  fetchOrders(); // Pre-load orders
});

// Computed
const selectedServicesList = computed(() => {
  return serviceTypes.value.filter((s: ServiceType) => selectedServiceIds.value.includes(s.id));
});

const totalAmount = computed(() => {
  return selectedServicesList.value.reduce((sum: number, s: ServiceType) => sum + Number(s.price), 0).toFixed(2);
});

// Actions
const toggleService = (id: number) => {
  const index = selectedServiceIds.value.indexOf(id);
  if (index === -1) {
    selectedServiceIds.value.push(id);
  } else {
    selectedServiceIds.value.splice(index, 1);
  }
};

const handlePay = () => {
  showPaymentDialog.value = true;
};

const getPatientName = (id: string | number | null) => {
  const p = patients.value.find(p => String(p.id) === String(id));
  return p ? p.name : 'Unknown';
};

const confirmPay = async () => {
  if (!selectedPatientId.value) return;
  
  submittingOrder.value = true;
  try {
    // Simulate payment process (e.g., wait 1s)
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Call API to create order
    await createServiceOrder({
      patient_id: selectedPatientId.value,
      service_ids: selectedServiceIds.value
    });
    
    ElMessage.success('支付成功，订单已生成');
    showPaymentDialog.value = false;
    selectedServiceIds.value = []; // Reset selection
    
    // Switch to history tab and refresh
    activeTab.value = 'history';
    fetchOrders();
    
  } catch (error) {
    console.error(error);
    ElMessage.error('支付失败或创建订单失败');
  } finally {
    submittingOrder.value = false;
  }
};

const viewFeedback = (order: ServiceOrder) => {
  currentOrder.value = order;
  showFeedbackDialog.value = true;
};

const openReview = (order: ServiceOrder) => {
  currentOrder.value = order;
  reviewForm.value = { rating: 5, comment: '' };
  showReviewDialog.value = true;
};

const submitReviewForm = async () => {
  if (!currentOrder.value) return;
  submittingReview.value = true;
  try {
    await submitServiceReview(currentOrder.value.id, reviewForm.value);
    ElMessage.success('评价提交成功');
    showReviewDialog.value = false;
    fetchOrders(); // Refresh status
  } catch (error) {
    ElMessage.error('评价提交失败');
  } finally {
    submittingReview.value = false;
  }
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
</script>

<style scoped>
.custom-services-view {
  padding: 20px;
}
.page-header {
  margin-bottom: 20px;
}
.subtitle {
  color: #666;
  font-size: 14px;
  margin-top: 5px;
}

.patient-selector {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}
.label {
  font-weight: bold;
}

.service-card {
  cursor: pointer;
  margin-bottom: 20px;
  transition: all 0.3s;
  border: 1px solid #ebeef5;
}
.service-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.service-card.is-selected {
  border-color: var(--primary-color);
  background-color: var(--el-color-primary-light-9);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}
.service-name {
  font-weight: bold;
  font-size: 16px;
}
.service-desc {
  color: #666;
  font-size: 13px;
  height: 40px;
  overflow: hidden;
  margin-bottom: 10px;
}
.service-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.service-price {
  color: #f56c6c;
  font-weight: bold;
  font-size: 16px;
}

.bottom-bar {
  position: fixed;
  bottom: 0;
  left: 240px; /* Sidebar width */
  right: 0;
  background: white;
  padding: 15px 30px;
  box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 100;
}
.total-info {
  font-size: 16px;
}
.total-price {
  margin-left: 20px;
  font-weight: bold;
}
.price-num {
  color: #f56c6c;
  font-size: 24px;
}

/* Payment Confirm */
.payment-confirm {
  padding: 10px;
}
.confirm-item {
  margin-bottom: 15px;
  display: flex;
}
.confirm-item .label {
  width: 100px;
  color: #666;
}
.confirm-item .value {
  flex: 1;
  font-weight: 500;
}
.confirm-item.total .price {
  color: #f56c6c;
  font-size: 20px;
  font-weight: bold;
}

/* Feedback */
.feedback-detail {
  padding: 10px;
}
.feedback-info {
  margin-bottom: 15px;
  display: flex;
  justify-content: space-between;
  color: #666;
  font-size: 13px;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}
.feedback-content {
  font-size: 15px;
  line-height: 1.6;
  margin-bottom: 20px;
  white-space: pre-wrap;
}
.feedback-images {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}
.feedback-img {
  width: 100px;
  height: 100px;
  border-radius: 4px;
  border: 1px solid #eee;
}

@media screen and (max-width: 768px) {
  .bottom-bar {
    left: 0;
  }
}
</style>
