<template>
  <div class="announcements-view">
    <div class="page-header">
      <h1 class="page-title">公告管理</h1>
      <p class="page-subtitle">发布和管理平台公告，指定接收对象</p>
    </div>
    
    <el-card class="content-card">
      <div class="toolbar">
        <el-button 
          type="primary" 
          @click="openAddDialog" 
          class="publish-btn"
          :icon="Plus"
        >
          发布公告
        </el-button>
        <el-input 
          v-model="searchQuery" 
          placeholder="请输入公告标题" 
          class="search-input"
          :prefix-icon="Search"
          clearable
        />
      </div>
      
      <el-table 
        :data="filteredAnnouncements" 
        v-loading="loading"
        class="announcements-table"
        stripe
        border
      >
        <el-table-column prop="title" label="公告标题" min-width="200">
          <template #default="scope">
            <div class="title-cell">
              <span class="title-text">{{ scope.row.title }}</span>
              <el-tag v-if="scope.row.status === 'published'" type="success" size="small">
                已发布
              </el-tag>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="target_role" label="面向群体" width="120">
          <template #default="scope">
            <el-tag :type="getRoleType(scope.row.target_role)" size="small">
              {{ formatRole(scope.row.target_role) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="publish_time" label="发布时间" width="180">
          <template #default="scope">
            <div class="time-cell">
              <el-icon><Clock /></el-icon>
              <span>{{ formatDate(scope.row.publish_time) }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="expire_time" label="过期时间" width="180">
          <template #default="scope">
            <div class="time-cell" :class="{ 'expired': isExpired(scope.row.expire_time) }">
              <el-icon><Warning /></el-icon>
              <span>{{ formatDate(scope.row.expire_time) || '长期有效' }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <div class="action-buttons">
              <el-button 
                type="primary" 
                size="small" 
                @click="openEditDialog(scope.row)"
                :icon="Edit"
                class="action-btn"
              >
                编辑
              </el-button>
              <el-button 
                v-if="scope.row.status === 'published'" 
                type="warning" 
                size="small" 
                @click="handleRetract(scope.row.id)"
                :icon="Refresh"
                class="action-btn"
              >
                撤回
              </el-button>
              <el-button 
                type="danger" 
                size="small" 
                @click="handleDelete(scope.row.id)"
                :icon="Delete"
                class="action-btn"
              >
                删除
              </el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
      
      <el-pagination
        v-if="totalCount > pageSize"
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="totalCount"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        class="pagination"
      />
    </el-card>

    <!-- 发布/编辑公告对话框 -->
    <el-dialog 
      v-model="showDialog" 
      :title="isEdit ? '编辑公告' : '发布公告'" 
      width="600px"
      class="announcement-dialog"
      append-to-body
    >
      <el-form :model="form" label-width="100px" class="announcement-form">
        <el-form-item label="公告标题" required>
          <el-input 
            v-model="form.title" 
            placeholder="请输入公告标题"
            maxlength="100"
            show-word-limit
          />
        </el-form-item>
        <el-form-item label="面向群体" required>
          <el-radio-group v-model="form.target_role" class="target-radio-group">
            <el-radio label="all">全部用户</el-radio>
            <el-radio label="family">家属用户</el-radio>
            <el-radio label="staff">工作人员</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="公告内容" required>
          <el-input 
            v-model="form.content" 
            type="textarea" 
            rows="8" 
            placeholder="请输入公告内容"
            maxlength="2000"
            show-word-limit
          />
        </el-form-item>
        <el-form-item label="过期时间">
          <el-date-picker 
            v-model="form.expire_time" 
            type="datetime" 
            placeholder="选择过期时间（可选）"
            format="YYYY-MM-DD HH:mm"
            value-format="YYYY-MM-DD HH:mm:ss"
            :disabled-date="disabledDate"
          />
          <div class="form-tip">不设置则默认为长期有效</div>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showDialog = false" class="cancel-btn">取消</el-button>
          <el-button 
            type="primary" 
            @click="handleSubmit" 
            :loading="submitLoading"
            class="submit-btn"
          >
            {{ isEdit ? '更新公告' : '发布公告' }}
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Plus, Search, Edit, Refresh, Delete, Clock, Warning } from '@element-plus/icons-vue';
import { getAnnouncements, createAnnouncement, updateAnnouncement, deleteAnnouncement, retractAnnouncement, type Announcement } from '@/services/admin/announcements';

const loading = ref(false);
const showDialog = ref(false);
const isEdit = ref(false);
const submitLoading = ref(false);
const searchQuery = ref('');
const announcements = ref<Announcement[]>([]);
const currentPage = ref(1);
const pageSize = ref(10);
const totalCount = ref(0);

const form = reactive({
  id: 0,
  title: '',
  content: '',
  target_role: 'all',
  expire_time: '',
  status: 'published'
});

const fetchAnnouncements = async () => {
  loading.value = true;
  try {
    const response = await getAnnouncements();
    console.log('获取公告响应:', response);
    announcements.value = response || [];
    totalCount.value = announcements.value.length;
    if (announcements.value.length === 0) {
      console.log('公告列表为空，数据库中没有已发布的公告')
    }
  } catch (error) {
    console.error('获取公告列表失败:', error);
    ElMessage.error('获取公告列表失败');
  } finally {
    loading.value = false;
  }
};

const filteredAnnouncements = computed(() => {
  if (!searchQuery.value) return announcements.value;
  return announcements.value.filter(item => 
    item.title.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

const openAddDialog = () => {
  isEdit.value = false;
  form.id = 0;
  form.title = '';
  form.content = '';
  form.target_role = 'all';
  form.expire_time = '';
  showDialog.value = true;
};

const openEditDialog = (row: Announcement) => {
  isEdit.value = true;
  Object.assign(form, row);
  showDialog.value = true;
};

const handleSubmit = async () => {
  if (!form.title.trim()) {
    ElMessage.warning('请输入公告标题');
    return;
  }
  if (!form.content.trim()) {
    ElMessage.warning('请输入公告内容');
    return;
  }
  
  submitLoading.value = true;
  try {
    if (isEdit.value) {
      await updateAnnouncement(form.id, {
        title: form.title,
        content: form.content,
        target_role: form.target_role,
        expire_time: form.expire_time
      });
      ElMessage.success('更新成功');
    } else {
      await createAnnouncement({
        title: form.title,
        content: form.content,
        target_role: form.target_role,
        expire_time: form.expire_time,
        status: 'published'
      });
      ElMessage.success('发布成功');
    }
    showDialog.value = false;
    fetchAnnouncements();
  } catch (error) {
    ElMessage.error(isEdit.value ? '更新失败' : '发布失败');
  } finally {
    submitLoading.value = false;
  }
};

const handleDelete = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定删除该公告吗？删除后无法恢复。', '删除确认', { 
      type: 'warning',
      confirmButtonText: '确定删除',
      cancelButtonText: '取消'
    });
    await deleteAnnouncement(id);
    ElMessage.success('删除成功');
    fetchAnnouncements();
  } catch (e) {
    // cancelled
  }
};

const handleRetract = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定撤回该公告吗？撤回后用户将无法查看。', '撤回确认', { 
      type: 'warning',
      confirmButtonText: '确定撤回',
      cancelButtonText: '取消'
    });
    await retractAnnouncement(id);
    ElMessage.success('撤回成功');
    fetchAnnouncements();
  } catch (error) {
    ElMessage.error('撤回失败');
  }
};

const handleSizeChange = (val: number) => {
  pageSize.value = val;
  currentPage.value = 1;
};

const handleCurrentChange = (val: number) => {
  currentPage.value = val;
};

const formatRole = (role: string) => {
  const map: Record<string, string> = { all: '全部用户', family: '家属用户', staff: '工作人员' };
  return map[role] || role;
};

const getRoleType = (role: string) => {
  const map: Record<string, string> = { all: 'primary', family: 'success', staff: 'warning' };
  return map[role] || 'info';
};

const formatDate = (str: string) => {
  if (!str) return '';
  return new Date(str).toLocaleString('zh-CN');
};

const isExpired = (expireTime: string) => {
  if (!expireTime) return false;
  return new Date(expireTime) < new Date();
};

const disabledDate = (date: Date) => {
  return date < new Date();
};

onMounted(fetchAnnouncements);
</script>

<style scoped>
.announcements-view {
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

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 16px 0;
}

.publish-btn {
  background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%);
  border: none;
  font-weight: 500;
  transition: all 0.3s ease;
}

.publish-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}

.search-input {
  width: 300px;
}

.search-input :deep(.el-input__wrapper) {
  border-radius: 6px;
}

.announcements-table {
  border-radius: 6px;
}

.title-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}

.title-text {
  font-weight: 500;
  color: #303133;
  flex: 1;
}

.time-cell {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #606266;
}

.time-cell.expired {
  color: #f56c6c;
}

.time-cell :deep(.el-icon) {
  font-size: 14px;
}

.action-buttons {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.action-btn {
  transition: all 0.3s ease;
  border-radius: 4px;
}

.action-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.pagination {
  margin-top: 24px;
  display: flex;
  justify-content: center;
}

.announcement-dialog :deep(.el-dialog__header) {
  padding: 24px 24px 16px;
  border-bottom: 1px solid #ebeef5;
  margin: 0;
}

.announcement-dialog :deep(.el-dialog__title) {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.announcement-dialog :deep(.el-dialog__body) {
  padding: 24px;
}

.announcement-form :deep(.el-form-item__label) {
  font-weight: 500;
  color: #606266;
}

.target-radio-group {
  display: flex;
  gap: 16px;
}

.form-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 0 0 0;
  border-top: 1px solid #ebeef5;
}

.cancel-btn {
  border-radius: 4px;
}

.submit-btn {
  background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%);
  border: none;
  border-radius: 4px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.submit-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}

.submit-btn:active {
  transform: translateY(0);
}

.submit-btn.is-disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .announcements-view {
    padding: 16px;
  }
  
  .toolbar {
    flex-direction: column;
    align-items: stretch;
    gap: 16px;
  }
  
  .search-input {
    width: 100%;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .announcement-dialog {
    width: 90% !important;
  }
}

@media (max-width: 480px) {
  .page-title {
    font-size: 20px;
  }
  
  .target-radio-group {
    flex-direction: column;
    gap: 8px;
  }
}
</style>