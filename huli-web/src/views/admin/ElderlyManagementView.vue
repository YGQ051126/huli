<template>
  <div class="elderly-management-view">
    <h1>老人信息管理</h1>
    <el-card>
      <!-- 操作栏 -->
      <div class="operation-bar">
        <el-button type="primary" @click="showAddDialog = true" :icon="Plus">
          添加老人
        </el-button>
        <div class="search-box">
          <el-input 
            v-model="searchQuery" 
            placeholder="请输入老人姓名或身份证号" 
            style="width: 300px; margin-left: 20px"
            :prefix-icon="Search"
            clearable
          />
          <el-select 
            v-model="health_level_filter" 
            placeholder="健康等级"
            style="width: 150px; margin-left: 10px"
            clearable
          >
            <el-option label="良好" value="good" />
            <el-option label="一般" value="normal" />
            <el-option label="较差" value="poor" />
          </el-select>
          <el-select 
            v-model="care_level_filter" 
            placeholder="护理等级"
            style="width: 150px; margin-left: 10px"
            clearable
          >
            <el-option label="一级护理" value="level1" />
            <el-option label="二级护理" value="level2" />
            <el-option label="三级护理" value="level3" />
          </el-select>
        </div>
      </div>
      
      <!-- 老人列表 -->
      <el-table 
        :data="filteredElderly" 
        style="margin-bottom: 20px"
        :loading="isLoading"
        stripe
        border
        empty-text="暂无老人数据"
      >
        <el-table-column type="index" label="序号" width="80" />
        <el-table-column prop="name" label="姓名" width="120" />
        <el-table-column prop="age" label="年龄" width="80" />
        <el-table-column prop="gender" label="性别" width="80">
          <template #default="scope">
            <el-tag :type="scope.row.gender === 'male' ? 'primary' : 'success'">
              {{ scope.row.gender === 'male' ? '男' : '女' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="idCard" label="身份证号" width="200" />
        <el-table-column prop="phone" label="联系电话" width="150" />
        <el-table-column prop="health_level" label="健康等级" width="120">
          <template #default="scope">
            <el-tag 
              :type="scope.row.health_level === 'good' ? 'success' : scope.row.health_level === 'normal' ? 'warning' : 'danger'"
            >
              {{ scope.row.health_level === 'good' ? '良好' : scope.row.health_level === 'normal' ? '一般' : '较差' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="care_level" label="护理等级" width="120">
          <template #default="scope">
            <el-tag :type="scope.row.care_level === 'level1' ? 'primary' : scope.row.care_level === 'level2' ? 'info' : 'success'">
              {{ scope.row.care_level === 'level1' ? '一级护理' : scope.row.care_level === 'level2' ? '二级护理' : '三级护理' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="room_number" label="房间号" width="100">
          <template #default="scope">
            {{ scope.row.room_number || '未分配' }}
          </template>
        </el-table-column>
        <el-table-column prop="bed_id" label="床位ID" width="100" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button type="primary" size="small" @click="showDetailDialog(scope.row)">
              详情
            </el-button>
            <el-button type="warning" size="small" @click="openEditDialog(scope.row)">
              编辑
            </el-button>
            <el-button type="danger" size="small" @click="handleDelete(scope.row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="elderly.length"
        />
      </div>
    </el-card>

    <!-- 添加老人对话框 -->
    <el-dialog v-model="showAddDialog" title="添加老人信息" width="800px" :close-on-click-modal="false">
      <el-form 
        :model="addForm" 
        label-width="120px"
        ref="addFormRef"
        :rules="formRules"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="姓名" prop="name">
              <el-input v-model="addForm.name" placeholder="请输入老人姓名" />
            </el-form-item>
            <el-form-item label="性别" prop="gender">
              <el-select v-model="addForm.gender" placeholder="请选择性别">
                <el-option label="男" value="male" />
                <el-option label="女" value="female" />
              </el-select>
            </el-form-item>
            <el-form-item label="年龄" prop="age">
              <el-input v-model.number="addForm.age" type="number" placeholder="请输入年龄" min="0" max="150" />
            </el-form-item>
            <el-form-item label="身份证号" prop="idCard">
              <el-input v-model="addForm.idCard" placeholder="请输入身份证号" maxlength="18" show-word-limit />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话" prop="phone">
              <el-input v-model="addForm.phone" placeholder="请输入联系电话" maxlength="11" show-word-limit />
            </el-form-item>
            <el-form-item label="健康等级" prop="health_level">
              <el-select v-model="addForm.health_level" placeholder="请选择健康等级">
                <el-option label="良好" value="good" />
                <el-option label="一般" value="normal" />
                <el-option label="较差" value="poor" />
              </el-select>
            </el-form-item>
            <el-form-item label="护理等级" prop="care_level">
              <el-select v-model="addForm.care_level" placeholder="请选择护理等级">
                <el-option label="一级护理" value="level1" />
                <el-option label="二级护理" value="level2" />
                <el-option label="三级护理" value="level3" />
              </el-select>
            </el-form-item>
            <el-form-item label="房间号" prop="room">
              <el-input v-model="addForm.room" placeholder="请输入房间号（如：101）" maxlength="3" />
            </el-form-item>
            <el-form-item label="床位号" prop="bed_id">
              <el-input v-model="addForm.bed_id" placeholder="请输入床位号（1-9）" maxlength="1" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="居住地址" prop="address">
          <el-input v-model="addForm.address" type="textarea" :rows="3" placeholder="请输入居住地址" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="resetAddForm">取消</el-button>
          <el-button type="primary" @click="addElderly" :loading="isSubmitting">保存</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 编辑老人对话框 -->
    <el-dialog v-model="showEditDialog" title="编辑老人信息" width="800px" :close-on-click-modal="false">
      <el-form 
        :model="editForm" 
        label-width="120px"
        ref="editFormRef"
        :rules="formRules"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="姓名" prop="name">
              <el-input v-model="editForm.name" placeholder="请输入老人姓名" />
            </el-form-item>
            <el-form-item label="性别" prop="gender">
              <el-select v-model="editForm.gender" placeholder="请选择性别">
                <el-option label="男" value="male" />
                <el-option label="女" value="female" />
              </el-select>
            </el-form-item>
            <el-form-item label="年龄" prop="age">
              <el-input v-model.number="editForm.age" type="number" placeholder="请输入年龄" min="0" max="150" />
            </el-form-item>
            <el-form-item label="身份证号" prop="idCard">
              <el-input v-model="editForm.idCard" placeholder="请输入身份证号" maxlength="18" show-word-limit />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话" prop="phone">
              <el-input v-model="editForm.phone" placeholder="请输入联系电话" maxlength="11" show-word-limit />
            </el-form-item>
            <el-form-item label="健康等级" prop="health_level">
              <el-select v-model="editForm.health_level" placeholder="请选择健康等级">
                <el-option label="良好" value="good" />
                <el-option label="一般" value="normal" />
                <el-option label="较差" value="poor" />
              </el-select>
            </el-form-item>
            <el-form-item label="护理等级" prop="care_level">
              <el-select v-model="editForm.care_level" placeholder="请选择护理等级">
                <el-option label="一级护理" value="level1" />
                <el-option label="二级护理" value="level2" />
                <el-option label="三级护理" value="level3" />
              </el-select>
            </el-form-item>
            <el-form-item label="房间号" prop="room">
              <el-input v-model="editForm.room" placeholder="请输入房间号（如：101）" maxlength="3" />
            </el-form-item>
            <el-form-item label="床位号" prop="bed_id">
              <el-input v-model="editForm.bed_id" placeholder="请输入床位号（1-9）" maxlength="1" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="居住地址" prop="address">
          <el-input v-model="editForm.address" type="textarea" :rows="3" placeholder="请输入居住地址" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showEditDialog = false">取消</el-button>
          <el-button type="primary" @click="updateElderly" :loading="isSubmitting">保存</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 老人详情对话框 -->
    <el-dialog v-model="showDetailDialogVisible" title="老人详情" width="800px">
      <div class="detail-content" v-if="selectedElderly">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="姓名">{{ selectedElderly.name }}</el-descriptions-item>
          <el-descriptions-item label="年龄">{{ selectedElderly.age }}岁</el-descriptions-item>
          <el-descriptions-item label="性别">{{ selectedElderly.gender === 'male' ? '男' : '女' }}</el-descriptions-item>
          <el-descriptions-item label="身份证号">{{ selectedElderly.idCard }}</el-descriptions-item>
          <el-descriptions-item label="联系电话">{{ selectedElderly.phone }}</el-descriptions-item>
          <el-descriptions-item label="健康等级">
            <el-tag :type="selectedElderly.health_level === 'good' ? 'success' : selectedElderly.health_level === 'normal' ? 'warning' : 'danger'">
              {{ selectedElderly.health_level === 'good' ? '良好' : selectedElderly.health_level === 'normal' ? '一般' : '较差' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="护理等级">
            <el-tag :type="selectedElderly.care_level === 'level1' ? 'primary' : selectedElderly.care_level === 'level2' ? 'info' : 'success'">
              {{ selectedElderly.care_level === 'level1' ? '一级护理' : selectedElderly.care_level === 'level2' ? '二级护理' : '三级护理' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="房间号">{{ selectedElderly.room_number || '未分配' }}</el-descriptions-item>
          <el-descriptions-item label="床位ID">{{ selectedElderly.bbed_id}}</el-descriptions-item>
          <el-descriptions-item label="居住地址" :span="2">{{ selectedElderly.address }}</el-descriptions-item>
        </el-descriptions>
      </div>
    </el-dialog>
    
    <!-- 删除确认对话框 -->
    <el-dialog
      v-model="showDeleteConfirm"
      title="确认删除"
      width="400px"
      center
    >
      <template #header>
        <div class="dialog-header">
          <el-icon :size="24" color="var(--danger-color)"><Warning /></el-icon>
          <span>确认删除</span>
        </div>
      </template>
      <div>确定要删除老人 <span class="text-danger">{{ selectedDeleteElderly?.name }}</span> 的信息吗？</div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showDeleteConfirm = false">取消</el-button>
          <el-button type="danger" @click="confirmDelete" :loading="isSubmitting">
            确定删除
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import { Plus, Search, Warning } from '@element-plus/icons-vue';
import type { FormInstance, FormRules } from 'element-plus';
import { getPatients, createPatient, updatePatient, deletePatient, getRooms } from '@/services/patients';
import type { Patient } from '@/types/patient';

const getBeijingDateString = (): string => {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
};

// 表单引用
const addFormRef = ref<FormInstance>();
const editFormRef = ref<FormInstance>();

// 状态管理
const showAddDialog = ref(false);
const showEditDialog = ref(false);
const showDetailDialogVisible = ref(false);
const showDeleteConfirm = ref(false);
const isLoading = ref(false);
const isSubmitting = ref(false);

// 房间数据
const rooms = ref<any[]>([]);

// 筛选条件
const searchQuery = ref('');
const health_level_filter = ref('');
const care_level_filter = ref('');
const currentPage = ref(1);
const pageSize = ref(20);

// 选中的老人
const selectedElderly = ref<any>(null);
const selectedDeleteElderly = ref<any>(null);

// 老人数据
const elderly = ref<Patient[]>([]);

// 表单规则
const formRules = reactive<FormRules>({
  name: [
    { required: true, message: '请输入老人姓名', trigger: 'blur' },
    { min: 2, max: 20, message: '姓名长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  age: [
    { required: true, message: '请输入年龄', trigger: 'blur' },
    { type: 'number', min: 0, max: 150, message: '年龄必须在 0 到 150 之间', trigger: 'blur' }
  ],
  gender: [
    { required: true, message: '请选择性别', trigger: 'change' }
  ],
  idCard: [
    { required: true, message: '请输入身份证号', trigger: 'blur' },
    { pattern: /(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/, message: '身份证号格式不正确', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入联系电话', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '手机号格式不正确', trigger: 'blur' }
  ],
  health_level: [
    { required: true, message: '请选择健康等级', trigger: 'change' }
  ],
  care_level: [
    { required: true, message: '请选择护理等级', trigger: 'change' }
  ],
  room: [
    { required: true, message: '请选择房间号', trigger: 'change' }
  ],
  bed_id: [
    { required: true, message: '请输入床位号', trigger: 'blur' },
    { pattern: /^[1-9]$/, message: '床位号必须是1-9之间的数字', trigger: 'blur' }
  ],
  address: [
    { required: true, message: '请输入居住地址', trigger: 'blur' }
  ]
});

// 筛选后的老人数据
const filteredElderly = computed(() => {
  return elderly.value.filter(item => 
    (item.name.includes(searchQuery.value) || item.idCard.includes(searchQuery.value))
    // 目前Patient类型没有healthLevel和nursingLevel属性，暂时注释掉这些筛选条件
    // && (!healthLevelFilter.value || item.healthLevel === healthLevelFilter.value)
    // && (!nursingLevelFilter.value || item.nursingLevel === nursingLevelFilter.value)
  );
});

// 添加表单
const addForm = reactive({
  name: '',
  age: 0,
  gender: 'male',
  idCard: '',
  phone: '',
  health_level: 'good',
  care_level: 'level1',
  room: '',
  bed_id: '',
  address: '',
});

// 编辑表单
const editForm = reactive({
  id: '',
  name: '',
  age: 0,
  gender: 'male',
  idCard: '',
  phone: '',
  health_level: 'good',
  care_level: 'level1',
  room: '',
  bed_id: '',
  address: '',
});

// 加载数据
onMounted(async () => {
  loadElderlyData();
  loadRooms();
});

const loadRooms = async () => {
  try {
    console.log('开始加载房间数据...');
    const data = await getRooms();
    console.log('加载房间数据成功:', data);
    console.log('房间数据长度:', data.length);
    rooms.value = data;
    console.log('房间数据设置完成:', rooms.value);
    
    if (data.length === 0) {
      console.warn('警告: 没有获取到任何房间数据');
    }
  } catch (error) {
    console.error('加载房间数据失败:', error);
    console.error('错误详情:', JSON.stringify(error, null, 2));
    // 显示用户友好的错误消息
    ElMessage.error('加载房间数据失败，请稍后重试');
  }
};

const loadElderlyData = async () => {
  isLoading.value = true;
  try {
    // 调用API获取数据
    const data = await getPatients();
    elderly.value = data;
    ElMessage.success('加载老人数据成功');
  } catch (error) {
    ElMessage.error('加载老人数据失败');
    console.error('加载老人数据失败:', error);
  } finally {
    isLoading.value = false;
  }
};

// 添加老人
const addElderly = async () => {
  if (!addFormRef.value) return;
  
  try {
    await addFormRef.value.validate();
    isSubmitting.value = true;
    
    // 字段映射：前端表单字段 -> 后端API字段
    const patientData = {
      name: addForm.name,
      gender: addForm.gender,
      age: addForm.age,
      id_card: addForm.idCard,
      phone: addForm.phone,
      address: addForm.address,
      health_level: addForm.health_level,
      care_level: addForm.care_level,
      room: addForm.room,
      bed_id: addForm.bed_id,
      admission_date: getBeijingDateString(),
      status: 'active',
    };
    
    // 调用API添加数据
    await createPatient(patientData as any);
    
    // 重新从数据库加载数据，确保显示的是数据库中的真实数据
    await loadElderlyData();
    
    ElMessage.success('老人信息添加成功');
    resetAddForm();
  } catch (error) {
    ElMessage.error('老人信息添加失败');
    console.error('添加老人失败:', error);
  } finally {
    isSubmitting.value = false;
  }
};

// 重置添加表单
const resetAddForm = () => {
  addFormRef.value?.resetFields();
  // 重置后重新设置默认值
  addForm.health_level = 'good';
  addForm.care_level = 'level1';
  addForm.gender = 'male';
  showAddDialog.value = false;
};

// 更新老人信息
const updateElderly = async () => {
  if (!editFormRef.value) return;
  
  try {
    await editFormRef.value.validate();
    isSubmitting.value = true;
    
    // 字段映射：前端表单字段 -> 后端API字段
    const patientData = {
      name: editForm.name,
      gender: editForm.gender,
      age: editForm.age,
      id_card: editForm.idCard,
      phone: editForm.phone,
      address: editForm.address,
      health_level: editForm.health_level,
      care_level: editForm.care_level,
      room: editForm.room,
      bed_id: editForm.bed_id,
      admission_date: elderly.value.find(item => String(item.id) === String(editForm.id))?.admission_date || getBeijingDateString(),
      status: 'active',
    };
    
    // 调用API更新数据
    const updatedPatient = await updatePatient(editForm.id.toString(), patientData as any);
    
    // 更新本地数据
    const index = elderly.value.findIndex(item => String(item.id) === String(editForm.id));
    if (index !== -1) {
      elderly.value[index] = updatedPatient;
    }
    
    ElMessage.success('老人信息更新成功');
    showEditDialog.value = false;
  } catch (error) {
    ElMessage.error('老人信息更新失败');
    console.error('更新老人失败:', error);
  } finally {
    isSubmitting.value = false;
  }
};

// 显示详情对话框
const showDetailDialog = (elderly: any) => {
  selectedElderly.value = elderly;
  showDetailDialogVisible.value = true;
};

// 打开编辑对话框
const openEditDialog = (elderly: any) => {
  // 正确映射字段，填充编辑表单
  editForm.id = elderly.id;
  editForm.name = elderly.name;
  editForm.age = elderly.age;
  editForm.gender = elderly.gender;
  editForm.idCard = elderly.id_card;
  editForm.phone = elderly.phone;
  editForm.health_level = elderly.health_level;
  editForm.care_level = elderly.care_level;
  editForm.bed_id = elderly.bed_id;
  editForm.address = elderly.address;
  // 设置房间号 - 如果elderly.room存在则使用room.id，否则使用room字段
  editForm.room = elderly.room ? (typeof elderly.room === 'object' ? elderly.room.id : elderly.room) : '';
  showEditDialog.value = true;
};

// 处理删除
const handleDelete = (elderly: any) => {
  selectedDeleteElderly.value = elderly;
  showDeleteConfirm.value = true;
};

// 确认删除
const confirmDelete = async () => {
  try {
    isSubmitting.value = true;
    
    // 调用API删除数据
    await deletePatient(selectedDeleteElderly.value?.id.toString());
    
    // 更新本地数据
    elderly.value = elderly.value.filter(item => String(item.id) !== String(selectedDeleteElderly.value?.id));
    
    ElMessage.success('老人信息删除成功');
    showDeleteConfirm.value = false;
  } catch (error) {
    ElMessage.error('老人信息删除失败');
    console.error('删除老人失败:', error);
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<style scoped>
.elderly-management-view {
  padding: 20px;
}

.operation-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 10px;
}

.search-box {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.pagination-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

.detail-content {
  padding: 20px 0;
}

.dialog-header {
  display: flex;
  align-items: center;
  gap: 10px;
}

.text-danger {
  color: var(--danger-color);
  font-weight: 500;
}

/* 响应式设计 */
@media screen and (max-width: 768px) {
  .operation-bar {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-box {
    margin-left: 0;
  }
  
  .el-input,
  .el-select {
    width: 100% !important;
    margin-left: 0 !important;
  }
  
  .el-table {
    font-size: 13px;
  }
  
  .el-table-column {
    width: auto !important;
  }
  
  .el-table-column--fixed-right {
    width: 150px !important;
  }
}
</style>