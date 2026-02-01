<template>
  <div class="approvals-view">
    <div class="page-header">
      <h1 class="page-title">消息审批</h1>
      <p class="page-subtitle">处理员工请假、家属探视预约的审批</p>
    </div>
    
    <el-card class="content-card">
      <el-tabs v-model="activeTab" class="approval-tabs" @tab-change="fetchData">
        <el-tab-pane name="register">
          <template #label>
            <span class="tab-label">
              <el-icon><User /></el-icon>
              注册申请
              <el-badge v-if="registerPendingCount > 0" :value="registerPendingCount" class="tab-badge" />
            </span>
          </template>
          
          <div class="tab-content">
            <div class="tab-header">
              <div class="stats-cards">
                <el-card class="stat-card">
                  <div class="stat-content">
                    <div class="stat-number">{{ registerApprovals.length }}</div>
                    <div class="stat-label">总申请数</div>
                  </div>
                  <el-icon class="stat-icon"><Document /></el-icon>
                </el-card>
                <el-card class="stat-card">
                  <div class="stat-content">
                    <div class="stat-number">{{ registerPendingCount }}</div>
                    <div class="stat-label">待审批</div>
                  </div>
                  <el-icon class="stat-icon warning"><Clock /></el-icon>
                </el-card>
                <el-card class="stat-card">
                  <div class="stat-content">
                    <div class="stat-number">{{ registerApprovedCount }}</div>
                    <div class="stat-label">已批准</div>
                  </div>
                  <el-icon class="stat-icon success"><CircleCheck /></el-icon>
                </el-card>
              </div>
              
              <div class="filter-controls">
                <el-select v-model="registerStatusFilter" placeholder="状态筛选" class="filter-select">
                  <el-option label="全部状态" value="" />
                  <el-option label="待审批" value="pending" />
                  <el-option label="已批准" value="approved" />
                  <el-option label="已拒绝" value="rejected" />
                </el-select>
                <el-input
                  v-model="registerSearch"
                  placeholder="搜索申请人姓名/用户名/身份证"
                  class="filter-search"
                  :prefix-icon="Search"
                  clearable
                />
              </div>
            </div>
            
            <el-table 
              :data="filteredRegisterApprovals" 
              class="approval-table"
              stripe
              border
              v-loading="loading"
              max-height="500"
            >
              <el-table-column type="selection" width="55" />
              <el-table-column prop="real_name" label="家属姓名" min-width="120">
                <template #default="scope">
                  <div class="family-info">
                    <el-avatar :size="32" class="family-avatar">
                      {{ (scope.row.real_name || '?')[0] }}
                    </el-avatar>
                    <span class="family-name">{{ scope.row.real_name }}</span>
                  </div>
                </template>
              </el-table-column>
              <el-table-column prop="username" label="申请用户名" min-width="120" />
              <el-table-column prop="phone" label="联系电话" width="120" />
              <el-table-column prop="patient_id_card" label="关联老人身份证" min-width="180" />
              <el-table-column prop="relationship" label="关系" width="80" />
              <el-table-column prop="created_at" label="申请时间" width="160">
                <template #default="scope">
                  <div class="date-info">
                    <el-icon><Calendar /></el-icon>
                    <span>{{ formatDate(scope.row.created_at) }}</span>
                  </div>
                </template>
              </el-table-column>
              <el-table-column prop="status" label="状态" width="100" fixed="right">
                <template #default="scope">
                  <el-tag 
                    :type="getStatusType(scope.row.status)" 
                    size="small"
                    class="status-tag"
                  >
                    {{ getStatusLabel(scope.row.status) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="180" fixed="right">
                <template #default="scope">
                  <div class="action-buttons">
                    <el-button 
                      v-if="scope.row.status === 'pending'" 
                      type="success" 
                      size="small" 
                      @click="handleApproveRegister(scope.row.id)"
                      :icon="CircleCheck"
                      class="approve-btn"
                    >
                      批准
                    </el-button>
                    <el-button 
                      v-if="scope.row.status === 'pending'" 
                      type="danger" 
                      size="small" 
                      @click="handleRejectRegister(scope.row.id)"
                      :icon="CircleClose"
                      class="reject-btn"
                    >
                      拒绝
                    </el-button>
                    <el-button 
                      v-if="scope.row.status !== 'pending'" 
                      type="info" 
                      size="small" 
                      @click="viewRegisterDetail(scope.row)"
                      :icon="View"
                      class="detail-btn"
                    >
                      详情
                    </el-button>
                  </div>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>

        <el-tab-pane name="visit">
          <template #label>
            <span class="tab-label">
              <el-icon><User /></el-icon>
              探访申请
              <el-badge v-if="visitPendingCount > 0" :value="visitPendingCount" class="tab-badge" />
            </span>
          </template>
          
          <div class="tab-content">
            <div class="tab-header">
              <div class="stats-cards">
                <el-card class="stat-card">
                  <div class="stat-content">
                    <div class="stat-number">{{ visitApprovals.length }}</div>
                    <div class="stat-label">总申请数</div>
                  </div>
                  <el-icon class="stat-icon"><Document /></el-icon>
                </el-card>
                <el-card class="stat-card">
                  <div class="stat-content">
                    <div class="stat-number">{{ visitPendingCount }}</div>
                    <div class="stat-label">待审批</div>
                  </div>
                  <el-icon class="stat-icon warning"><Clock /></el-icon>
                </el-card>
                <el-card class="stat-card">
                  <div class="stat-content">
                    <div class="stat-number">{{ visitApprovedCount }}</div>
                    <div class="stat-label">已批准</div>
                  </div>
                  <el-icon class="stat-icon success"><CircleCheck /></el-icon>
                </el-card>
              </div>
              
              <div class="filter-controls">
                <el-select v-model="visitStatusFilter" placeholder="状态筛选" class="filter-select">
                  <el-option label="全部状态" value="" />
                  <el-option label="待审批" value="pending" />
                  <el-option label="已批准" value="approved" />
                  <el-option label="已拒绝" value="rejected" />
                </el-select>
                <el-date-picker
                  v-model="visitDateFilter"
                  type="date"
                  placeholder="选择日期"
                  class="filter-date"
                />
                <el-input
                  v-model="visitSearch"
                  placeholder="搜索老人或家属姓名"
                  class="filter-search"
                  :prefix-icon="Search"
                  clearable
                />
              </div>
            </div>
            
            <el-table 
              :data="filteredVisitApprovals" 
              class="approval-table"
              stripe
              border
              v-loading="loading"
              max-height="500"
            >
              <el-table-column type="selection" width="55" />
              <el-table-column prop="patient_name" label="老人姓名" min-width="120">
                <template #default="scope">
                  <div class="patient-info">
                    <el-avatar :size="32" class="patient-avatar">
                      {{ String(scope.row.patient_name || '?').charAt(0) }}
                    </el-avatar>
                    <span class="patient-name">{{ scope.row.patient_name }}</span>
                  </div>
                </template>
              </el-table-column>
              <el-table-column prop="family_name" label="家属姓名" min-width="120">
                <template #default="scope">
                  <div class="family-info">
                    <el-avatar :size="32" class="family-avatar">
                      {{ String(scope.row.family_name || '?').charAt(0) }}
                    </el-avatar>
                    <span class="family-name">{{ scope.row.family_name }}</span>
                  </div>
                </template>
              </el-table-column>
              <el-table-column prop="relationship" label="关系" width="80" />
              <el-table-column prop="date" label="探访日期" width="120">
                <template #default="scope">
                  <div class="date-info">
                    <el-icon><Calendar /></el-icon>
                    <span>{{ scope.row.date }}</span>
                  </div>
                </template>
              </el-table-column>
              <el-table-column prop="time_slot" label="探访时间" width="120">
                <template #default="scope">
                  <el-tag size="small" type="info">{{ scope.row.time_slot }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="notes" label="探访原因/备注" min-width="200">
                <template #default="scope">
                  <el-tooltip :content="scope.row.notes" placement="top" :disabled="!scope.row.notes">
                    <div class="notes-cell">{{ scope.row.notes || '无备注' }}</div>
                  </el-tooltip>
                </template>
              </el-table-column>
              <el-table-column prop="status" label="状态" width="100" fixed="right">
                <template #default="scope">
                  <el-tag 
                    :type="getStatusType(scope.row.status)" 
                    size="small"
                    class="status-tag"
                  >
                    {{ getStatusLabel(scope.row.status) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="180" fixed="right">
                <template #default="scope">
                  <div class="action-buttons">
                    <el-button 
                      v-if="scope.row.status === 'pending'" 
                      type="success" 
                      size="small" 
                      @click="handleApproveVisit(scope.row.id)"
                      :icon="CircleCheck"
                      class="approve-btn"
                    >
                      批准
                    </el-button>
                    <el-button 
                      v-if="scope.row.status === 'pending'" 
                      type="danger" 
                      size="small" 
                      @click="handleRejectVisit(scope.row.id)"
                      :icon="CircleClose"
                      class="reject-btn"
                    >
                      拒绝
                    </el-button>
                    <el-button 
                      v-if="scope.row.status !== 'pending'" 
                      type="info" 
                      size="small" 
                      @click="viewVisitDetail(scope.row)"
                      :icon="View"
                      class="detail-btn"
                    >
                      详情
                    </el-button>
                  </div>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>
        
        <el-tab-pane name="leave">
          <template #label>
            <span class="tab-label">
              <el-icon><Calendar /></el-icon>
              请假申请
              <el-badge v-if="leavePendingCount > 0" :value="leavePendingCount" class="tab-badge" />
            </span>
          </template>
          
          <div class="tab-content">
            <div class="tab-header">
              <div class="stats-cards">
                <el-card class="stat-card">
                  <div class="stat-content">
                    <div class="stat-number">{{ leaveApprovals.length }}</div>
                    <div class="stat-label">总申请数</div>
                  </div>
                  <el-icon class="stat-icon"><Document /></el-icon>
                </el-card>
                <el-card class="stat-card">
                  <div class="stat-content">
                    <div class="stat-number">{{ leavePendingCount }}</div>
                    <div class="stat-label">待审批</div>
                  </div>
                  <el-icon class="stat-icon warning"><Clock /></el-icon>
                </el-card>
                <el-card class="stat-card">
                  <div class="stat-content">
                    <div class="stat-number">{{ leaveApprovedCount }}</div>
                    <div class="stat-label">已批准</div>
                  </div>
                  <el-icon class="stat-icon success"><CircleCheck /></el-icon>
                </el-card>
              </div>
              
              <div class="filter-controls">
                <el-select v-model="leaveStatusFilter" placeholder="状态筛选" class="filter-select">
                  <el-option label="全部状态" value="" />
                  <el-option label="待审批" value="pending" />
                  <el-option label="已批准" value="approved" />
                  <el-option label="已拒绝" value="rejected" />
                </el-select>
                <el-date-picker
                  v-model="leaveDateFilter"
                  type="date"
                  placeholder="申请日期"
                  class="filter-date"
                />
                <el-input
                  v-model="leaveSearch"
                  placeholder="搜索员工姓名"
                  class="filter-search"
                  :prefix-icon="Search"
                  clearable
                />
              </div>
            </div>
            
            <el-table 
              :data="filteredLeaveApprovals" 
              class="approval-table"
              stripe
              border
              v-loading="loading"
              max-height="500"
            >
              <el-table-column type="selection" width="55" />
              <el-table-column prop="staff_name" label="员工姓名" min-width="120">
                <template #default="scope">
                  <div class="staff-info">
                    <el-avatar :size="32" class="staff-avatar">
                      {{ String(scope.row.staff_name || '?').charAt(0) }}
                    </el-avatar>
                    <span class="staff-name">{{ scope.row.staff_name }}</span>
                  </div>
                </template>
              </el-table-column>
              <el-table-column prop="department" label="部门" width="120">
                <template #default="scope">
                  <el-tag size="small" type="info">{{ scope.row.department }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="leave_type" label="请假类型" width="100">
                <template #default="scope">
                  <el-tag size="small" :type="getLeaveTypeTag(scope.row.leave_type)">
                    {{ getLeaveTypeLabel(scope.row.leave_type) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="start_date" label="开始日期" width="120">
                <template #default="scope">
                  <div class="date-info">
                    <el-icon><Calendar /></el-icon>
                    <span>{{ scope.row.start_date }}</span>
                  </div>
                </template>
              </el-table-column>
              <el-table-column prop="end_date" label="结束日期" width="120">
                <template #default="scope">
                  <div class="date-info">
                    <el-icon><Calendar /></el-icon>
                    <span>{{ scope.row.end_date }}</span>
                  </div>
                </template>
              </el-table-column>
              <el-table-column prop="days" label="天数" width="80">
                <template #default="scope">
                  <el-tag size="small" type="warning">{{ scope.row.days }}天</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="reason" label="请假原因" min-width="200">
                <template #default="scope">
                  <el-tooltip :content="scope.row.reason" placement="top" :disabled="!scope.row.reason">
                    <div class="reason-cell">{{ scope.row.reason || '无说明' }}</div>
                  </el-tooltip>
                </template>
              </el-table-column>
              <el-table-column prop="status" label="状态" width="100" fixed="right">
                <template #default="scope">
                  <el-tag 
                    :type="getStatusType(scope.row.status)" 
                    size="small"
                    class="status-tag"
                  >
                    {{ getStatusLabel(scope.row.status) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="180" fixed="right">
                <template #default="scope">
                  <div class="action-buttons">
                    <el-button 
                      v-if="scope.row.status === 'pending'" 
                      type="success" 
                      size="small" 
                      @click="handleApproveLeave(scope.row.id)"
                      :icon="CircleCheck"
                      class="approve-btn"
                    >
                      批准
                    </el-button>
                    <el-button 
                      v-if="scope.row.status === 'pending'" 
                      type="danger" 
                      size="small" 
                      @click="handleRejectLeave(scope.row.id)"
                      :icon="CircleClose"
                      class="reject-btn"
                    >
                      拒绝
                    </el-button>
                    <el-button 
                      v-if="scope.row.status !== 'pending'" 
                      type="info" 
                      size="small" 
                      @click="viewLeaveDetail(scope.row)"
                      :icon="View"
                      class="detail-btn"
                    >
                      详情
                    </el-button>
                  </div>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>
    
    <!-- 详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="申请详情"
      width="600px"
      class="detail-dialog"
    >
      <div class="detail-content" v-if="currentDetail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="申请类型">{{ getApplicationType(currentDetail.type) }}</el-descriptions-item>
          <el-descriptions-item label="申请状态">
            <el-tag :type="getStatusType(currentDetail.status)">{{ getStatusLabel(currentDetail.status) }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="申请人">{{ currentDetail.applicant }}</el-descriptions-item>
          <el-descriptions-item label="申请时间">{{ currentDetail.application_date }}</el-descriptions-item>
          <el-descriptions-item label="相关说明" :span="2">{{ currentDetail.description || '无' }}</el-descriptions-item>
          <el-descriptions-item label="审批意见" :span="2" v-if="currentDetail.approval_comment">
            {{ currentDetail.approval_comment }}
          </el-descriptions-item>
          <el-descriptions-item label="审批时间" v-if="currentDetail.approval_date">
            {{ currentDetail.approval_date }}
          </el-descriptions-item>
          <el-descriptions-item label="审批人" v-if="currentDetail.approver">
            {{ currentDetail.approver }}
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { 
  User, Calendar, Document, Clock, CircleCheck, CircleClose, 
  View, Search 
} from '@element-plus/icons-vue';
import { 
  getApprovals, 
  approveVisit, rejectVisit, 
  approveLeave, rejectLeave,
  approveRegisterApplication, rejectRegisterApplication,
  type VisitApproval, 
  type LeaveApproval,
  type RegisterApplication
} from '@/services/admin/approvals';

const activeTab = ref('register');
const loading = ref(false);
const detailDialogVisible = ref(false);
const currentDetail = ref<any>(null);

// 注册申请相关
const registerApprovals = ref<RegisterApplication[]>([]);
const registerStatusFilter = ref('');
const registerSearch = ref('');

// 探访申请相关
const visitApprovals = ref<VisitApproval[]>([]);
const visitStatusFilter = ref('');
const visitDateFilter = ref('');
const visitSearch = ref('');

// 请假申请相关
const leaveApprovals = ref<LeaveApproval[]>([]);
const leaveStatusFilter = ref('');
const leaveDateFilter = ref('');
const leaveSearch = ref('');

// 统计数据
const registerPendingCount = computed(() => registerApprovals.value.filter(item => item.status === 'pending').length);
const registerApprovedCount = computed(() => registerApprovals.value.filter(item => item.status === 'approved').length);
const visitPendingCount = computed(() => visitApprovals.value.filter(item => item.status === 'pending').length);
const visitApprovedCount = computed(() => visitApprovals.value.filter(item => item.status === 'approved').length);
const leavePendingCount = computed(() => leaveApprovals.value.filter(item => item.status === 'pending').length);
const leaveApprovedCount = computed(() => leaveApprovals.value.filter(item => item.status === 'approved').length);

// 筛选后的数据
const filteredRegisterApprovals = computed(() => {
  let filtered = registerApprovals.value;
  
  if (registerStatusFilter.value) {
    filtered = filtered.filter(item => item.status === registerStatusFilter.value);
  }
  
  if (registerSearch.value) {
    filtered = filtered.filter(item => 
      (item.real_name || '').includes(registerSearch.value) ||
      (item.username || '').includes(registerSearch.value) ||
      (item.patient_id_card || '').includes(registerSearch.value)
    );
  }
  
  return filtered;
});

const filteredVisitApprovals = computed(() => {
  let filtered = visitApprovals.value;
  
  if (visitStatusFilter.value) {
    filtered = filtered.filter(item => item.status === visitStatusFilter.value);
  }
  
  if (visitSearch.value) {
    filtered = filtered.filter(item => 
      (item.patient_name || '').includes(visitSearch.value) || 
      (item.family_name || '').includes(visitSearch.value)
    );
  }
  
  return filtered;
});

const filteredLeaveApprovals = computed(() => {
  let filtered = leaveApprovals.value;
  
  if (leaveStatusFilter.value) {
    filtered = filtered.filter(item => item.status === leaveStatusFilter.value);
  }
  
  if (leaveSearch.value) {
    filtered = filtered.filter(item => 
      (item.staff_name || '').includes(leaveSearch.value)
    );
  }
  
  return filtered;
});

const fetchData = async () => {
  loading.value = true;
  try {
    const data = await getApprovals();
    registerApprovals.value = data.register_approvals || [];
    visitApprovals.value = data.visit_approvals || [];
    leaveApprovals.value = data.leave_approvals || [];
    if (registerApprovals.value.length === 0 && visitApprovals.value.length === 0 && leaveApprovals.value.length === 0) {
      console.log('审批列表为空，数据库中没有待审批的数据')
    }
  } catch (error) {
    console.error('获取审批列表失败:', error);
    ElMessage.error('获取审批列表失败');
  } finally {
    loading.value = false;
  }
};

const handleApproveRegister = async (id: number) => {
  try {
    await approveRegisterApplication(id);
    ElMessage.success('注册申请已批准');
    fetchData();
  } catch (error) {
    ElMessage.error('操作失败');
  }
};

const handleRejectRegister = async (id: number) => {
  try {
    const reason = await ElMessageBox.prompt('请输入拒绝原因', '拒绝申请', {
      confirmButtonText: '确定拒绝',
      cancelButtonText: '取消',
      inputPattern: /^[\s\S]{2,200}$/,
      inputErrorMessage: '请输入2-200个字符的拒绝原因'
    });
    
    await rejectRegisterApplication(id, reason.value);
    ElMessage.success('注册申请已拒绝');
    fetchData();
  } catch (e) {
    // cancelled or validation failed
  }
};

const handleApproveVisit = async (id: number) => {
  try {
    await approveVisit(id);
    ElMessage.success('探访申请已批准');
    fetchData();
  } catch (error) {
    ElMessage.error('操作失败');
  }
};

const handleRejectVisit = async (id: number) => {
  try {
    const reason = await ElMessageBox.prompt('请输入拒绝原因', '拒绝申请', {
      confirmButtonText: '确定拒绝',
      cancelButtonText: '取消',
      inputPattern: /^[\s\S]{2,200}$/,
      inputErrorMessage: '请输入2-200个字符的拒绝原因'
    });
    
    await rejectVisit(id, reason);
    ElMessage.success('探访申请已拒绝');
    fetchData();
  } catch (e) {
    // cancelled or validation failed
  }
};

const handleApproveLeave = async (id: number) => {
  try {
    await approveLeave(id);
    ElMessage.success('请假申请已批准');
    fetchData();
  } catch (error) {
    ElMessage.error('操作失败');
  }
};

const handleRejectLeave = async (id: number) => {
  try {
    const reason = await ElMessageBox.prompt('请输入拒绝原因', '拒绝申请', {
      confirmButtonText: '确定拒绝',
      cancelButtonText: '取消',
      inputPattern: /^[\s\S]{2,200}$/,
      inputErrorMessage: '请输入2-200个字符的拒绝原因'
    });
    
    await rejectLeave(id, reason);
    ElMessage.success('请假申请已拒绝');
    fetchData();
  } catch (e) {
    // cancelled or validation failed
  }
};

const viewRegisterDetail = (row: RegisterApplication) => {
  currentDetail.value = {
    type: 'register',
    applicant: `${row.real_name} (申请家属)`,
    application_date: row.created_at,
    status: row.status,
    description: `申请账号: ${row.username}, 关联老人身份证: ${row.patient_id_card}, 关系: ${row.relationship}`,
    approver: row.approved_by,
    approval_date: row.approved_at,
    approval_comment: row.rejection_reason
  };
  detailDialogVisible.value = true;
};

const viewVisitDetail = (row: VisitApproval) => {
  currentDetail.value = {
    type: 'visit',
    applicant: `${row.family_name} (家属)`,
    application_date: row.created_at,
    status: row.status,
    description: row.notes,
    approver: row.reviewer,
    approval_date: row.reviewed_at,
    approval_comment: row.review_comment
  };
  detailDialogVisible.value = true;
};

const viewLeaveDetail = (row: LeaveApproval) => {
  currentDetail.value = {
    type: 'leave',
    applicant: row.staff_name,
    application_date: row.created_at,
    status: row.status,
    description: `请假类型: ${getLeaveTypeLabel(row.leave_type)}，请假 ${row.days} 天，原因: ${row.reason}`,
    approver: row.reviewer,
    approval_date: row.reviewed_at,
    approval_comment: row.review_comment
  };
  detailDialogVisible.value = true;
};

const getStatusType = (status: string): string => {
  const types: Record<string, string> = {
    pending: 'warning',
    approved: 'success',
    rejected: 'danger'
  };
  return types[status] || 'info';
};

const getStatusLabel = (status: string): string => {
  const labels: Record<string, string> = {
    pending: '待审批',
    approved: '已批准',
    rejected: '已拒绝'
  };
  return labels[status] || status;
};

const getLeaveTypeTag = (type: string): string => {
  const tags: Record<string, string> = {
    sick: 'danger',
    personal: 'warning',
    annual: 'success',
    emergency: 'danger'
  };
  return tags[type] || 'info';
};

const getLeaveTypeLabel = (type: string): string => {
  const labels: Record<string, string> = {
    sick: '病假',
    personal: '事假',
    annual: '年假',
    emergency: '紧急假'
  };
  return labels[type] || type;
};

const getApplicationType = (type: string): string => {
    const types: Record<string, string> = {
      register: '注册申请',
      visit: '探访申请',
      leave: '请假申请'
    };
    return types[type] || type;
  };

const formatDate = (dateStr: string): string => {
  return new Date(dateStr).toLocaleDateString('zh-CN');
};

onMounted(fetchData);
</script>

<style scoped>
.approvals-view {
  padding: 24px;
  background: #f5f7fa;
  min-height: calc(100vh - 120px);
}

.page-header {
  margin-bottom: 24px;
  padding: 0 8px;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 8px 0;
}

.page-subtitle {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

.content-card {
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.approval-tabs :deep(.el-tabs__header) {
  margin-bottom: 0;
}

.approval-tabs :deep(.el-tabs__item) {
  font-size: 16px;
  font-weight: 500;
  padding: 0 24px;
}

.tab-label {
  display: flex;
  align-items: center;
  gap: 8px;
  position: family;
}

.tab-badge {
  position: absolute;
  top: -8px;
  right: -8px;
}

.tab-content {
  padding: 24px;
}

.tab-header {
  margin-bottom: 24px;
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  border-radius: 8px;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.stat-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stat-number {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.stat-icon {
  font-size: 32px;
  color: #c0c4cc;
  align-self: flex-end;
}

.stat-icon.warning {
  color: #e6a23c;
}

.stat-icon.success {
  color: #67c23a;
}

.filter-controls {
  display: flex;
  gap: 16px;
  align-items: center;
  padding: 16px;
  background: #f8f9fb;
  border-radius: 8px;
  border: 1px solid #ebeef5;
}

.filter-select,
.filter-date,
.filter-search {
  min-width: 160px;
}

.approval-table {
  border-radius: 6px;
}

.patient-info,
.family-info,
.user-info,
.staff-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.patient-avatar,
.family-avatar,
.user-avatar,
.staff-avatar {
  background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%);
  color: white;
  font-weight: 500;
}

.patient-name,
.family-name,
.user-id,
.staff-name {
  font-weight: 500;
  color: #303133;
}

.date-info,
.patient-link {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #606266;
}

.notes-cell,
.reason-cell {
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 14px;
  color: #606266;
}

.status-tag {
  font-weight: 500;
}

.action-buttons {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.approve-btn,
.reject-btn,
.detail-btn {
  transition: all 0.3s ease;
  border-radius: 4px;
  font-weight: 500;
}

.approve-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(103, 194, 58, 0.3);
}

.reject-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(245, 108, 108, 0.3);
}

.detail-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(144, 147, 153, 0.3);
}

.approve-btn:active,
.reject-btn:active,
.detail-btn:active {
  transform: translateY(0);
}

.detail-dialog :deep(.el-dialog__header) {
  padding: 24px 24px 16px;
  border-bottom: 1px solid #ebeef5;
  margin: 0;
}

.detail-dialog :deep(.el-dialog__title) {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.detail-content {
  padding: 24px 0;
}

.detail-dialog :deep(.el-descriptions__label) {
  font-weight: 500;
  color: #606266;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .approvals-view {
    padding: 16px;
  }
  
  .stats-cards {
    grid-template-columns: 1fr;
  }
  
  .filter-controls {
    flex-direction: column;
    align-items: stretch;
  }
  
  .filter-select,
  .filter-date,
  .filter-search {
    min-width: auto;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .tab-content {
    padding: 16px;
  }
}

@media (max-width: 480px) {
  .page-title {
    font-size: 20px;
  }
  
  .approval-tabs :deep(.el-tabs__item) {
    font-size: 14px;
    padding: 0 16px;
  }
  
  .patient-info,
  .family-info,
  .user-info,
  .staff-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}
</style>