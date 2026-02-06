<template>
  <div class="staff-management-view">
    <h1>员工信息管理</h1>
    <el-card>
      <div style="margin-bottom: 20px">
        <el-button type="primary" @click="openAddDialog">添加员工</el-button>
        <el-input v-model="searchQuery" placeholder="请输入员工姓名" style="width: 300px; margin-left: 20px" />
      </div>
      <el-table :data="filteredStaff" style="margin-bottom: 20px" v-loading="isLoading">
        <el-table-column label="姓名">
          <template #default="scope">
            {{ scope.row.user?.real_name || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="性别">
            <template #default="scope">
                {{ scope.row.user?.gender === 'male' ? '男' : '女' }}
            </template>
        </el-table-column>
        <el-table-column prop="position" label="职位" />
        <el-table-column prop="department" label="部门" />
        <el-table-column label="联系电话">
          <template #default="scope">
            {{ scope.row.user?.phone || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="邮箱">
          <template #default="scope">
            {{ scope.row.user?.email || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="状态">
            <template #default="scope">
                <el-tag :type="scope.row.user?.status === 'active' ? 'success' : 'info'">
                    {{ scope.row.user?.status === 'active' ? '在职' : '离职/禁用' }}
                </el-tag>
            </template>
        </el-table-column>
        <el-table-column label="操作" width="280">
          <template #default="scope">
            <el-button type="primary" size="small" @click="openEditDialog(scope.row)">
              编辑
            </el-button>
            <el-button type="danger" size="small" @click="handleDelete(scope.row.id || scope.row.user?.id)">
              删除
            </el-button>
            <el-button type="success" size="small" @click="openAccountDialog(scope.row)">
              管理账户
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        :total="staff.length"
      />
    </el-card>

    <!-- 添加员工对话框 -->
    <el-dialog v-model="showAddDialog" title="添加员工信息" width="800px">
      <el-form :model="addForm" label-width="120px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="姓名">
              <el-input v-model="addForm.name" />
            </el-form-item>
            <el-form-item label="性别">
              <el-select v-model="addForm.gender">
                <el-option label="男" value="male" />
                <el-option label="女" value="female" />
              </el-select>
            </el-form-item>
            <el-form-item label="职位">
              <el-input v-model="addForm.position" />
            </el-form-item>
            <el-form-item label="部门">
              <el-select v-model="addForm.department">
                <el-option label="护理部" value="nursing" />
                <el-option label="行政部" value="admin" />
                <el-option label="财务部" value="finance" />
                <el-option label="保洁部" value="cleaning" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话">
              <el-input v-model="addForm.phone" />
            </el-form-item>
            <el-form-item label="邮箱">
              <el-input v-model="addForm.email" />
            </el-form-item>
             <el-form-item label="用户名">
              <el-input v-model="addForm.username" placeholder="默认为手机号" />
            </el-form-item>
             <el-form-item label="初始密码">
              <el-input v-model="addForm.password" placeholder="默认123456" show-password />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showAddDialog = false">取消</el-button>
          <el-button type="primary" @click="handleAddStaff">保存</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 编辑员工对话框 -->
    <el-dialog v-model="showEditDialog" title="编辑员工信息" width="800px">
      <el-form :model="editForm" label-width="120px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="姓名">
              <el-input v-model="editForm.name" />
            </el-form-item>
            <el-form-item label="性别">
              <el-select v-model="editForm.gender">
                <el-option label="男" value="male" />
                <el-option label="女" value="female" />
              </el-select>
            </el-form-item>
            <el-form-item label="职位">
              <el-input v-model="editForm.position" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="部门">
              <el-select v-model="editForm.department">
                <el-option label="护理部" value="nursing" />
                <el-option label="行政部" value="admin" />
                <el-option label="财务部" value="finance" />
                <el-option label="保洁部" value="cleaning" />
              </el-select>
            </el-form-item>
            <el-form-item label="联系电话">
              <el-input v-model="editForm.phone" />
            </el-form-item>
            <el-form-item label="邮箱">
              <el-input v-model="editForm.email" />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showEditDialog = false">取消</el-button>
          <el-button type="primary" @click="handleUpdateStaff">保存</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 管理账户对话框 -->
    <el-dialog v-model="showAccountDialog" title="账户管理" width="500px">
        <el-form :model="accountForm" label-width="100px">
            <el-form-item label="当前用户">
                <el-input v-model="accountForm.username" disabled />
            </el-form-item>
            <el-form-item label="重置密码">
                <el-input v-model="accountForm.newPassword" placeholder="请输入新密码" show-password />
            </el-form-item>
             <el-form-item label="账户状态">
              <el-select v-model="accountForm.status">
                <el-option label="在职" value="active" />
                <el-option label="离职/禁用" value="inactive" />
              </el-select>
            </el-form-item>
        </el-form>
        <template #footer>
            <el-button @click="showAccountDialog = false">取消</el-button>
            <el-button type="primary" @click="handleUpdateAccount">更新</el-button>
        </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { getStaffList, createStaff, updateStaff, deleteStaff, type StaffUser } from '@/services/staff';

const showAddDialog = ref(false);
const showEditDialog = ref(false);
const showAccountDialog = ref(false);
const searchQuery = ref('');
const currentPage = ref(1);
const pageSize = ref(10);
const isLoading = ref(false);
const staff = ref<StaffUser[]>([]);

const loadStaff = async () => {
  isLoading.value = true;
  try {
    const data = await getStaffList();
    staff.value = data;
  } catch (error) {
    console.error('Failed to load staff:', error);
    ElMessage.error('加载员工列表失败');
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  loadStaff();
});

const filteredStaff = computed(() => {
  const query = searchQuery.value.toLowerCase();
  return staff.value.filter(item => 
    item.user?.real_name?.toLowerCase().includes(query) || false
  );
});

// 表单数据
const addForm = reactive({
  name: '',
  gender: 'male',
  position: '',
  department: 'nursing',
  phone: '',
  email: '',
  username: '',
  password: '',
});

const editForm = reactive({
  id: 0,
  userId: 0,
  name: '',
  gender: 'male',
  position: '',
  department: 'nursing',
  phone: '',
  email: '',
});

const accountForm = reactive({
    staffId: 0,
    userId: 0,
    username: '',
    newPassword: '',
    status: 'active'
});

const openAddDialog = () => {
    Object.assign(addForm, {
        name: '', gender: 'male', position: '', department: 'nursing',
        phone: '', email: '', username: '', password: ''
    });
    showAddDialog.value = true;
};

const openEditDialog = (row: StaffUser) => {
    // 根据后端定义，StaffUser 的 primary_key 是 user 字段 (OneToOneField)
    // 所以 staffId 实际上就是 userId
    const id = row.user.id;
    
    if (!id) {
        console.error('Cannot find staff/user ID for row:', row);
        ElMessage.error('无法获取员工ID');
        return;
    }
    
    editForm.id = Number(id);
    editForm.userId = Number(id);
    editForm.name = row.user.real_name;
    editForm.gender = row.user.gender || 'male';
    editForm.position = row.position;
    editForm.department = row.department;
    editForm.phone = row.user.phone;
    editForm.email = row.user.email || '';
    showEditDialog.value = true;
};

const openAccountDialog = (row: StaffUser) => {
    // 根据后端定义，StaffUser 的 primary_key 是 user 字段 (OneToOneField)
    // 所以 staffId 实际上就是 userId
    const id = row.user.id;
    
    if (!id) {
        console.error('Cannot find staff/user ID for row:', row);
        ElMessage.error('无法获取员工ID');
        return;
    }
    
    accountForm.staffId = Number(id);
    accountForm.userId = Number(id);
    accountForm.username = row.user.username;
    accountForm.newPassword = '';
    accountForm.status = row.user.status;
    showAccountDialog.value = true;
};

const handleAddStaff = async () => {
  if (!addForm.name || !addForm.phone) {
      ElMessage.warning('姓名和电话为必填项');
      return;
  }
  try {
    await createStaff({
      user: {
        username: addForm.username || addForm.phone,
        password: addForm.password || '123456',
        real_name: addForm.name,
        phone: addForm.phone,
        email: addForm.email,
        role: 'staff',
        gender: addForm.gender
      },
      position: addForm.position,
      department: addForm.department
    });
    ElMessage.success('员工添加成功');
    showAddDialog.value = false;
    loadStaff();
  } catch (error) {
    console.error('Add staff failed:', error);
    ElMessage.error('员工添加失败');
  }
};

const handleUpdateStaff = async () => {
    try {
        await updateStaff(editForm.id, {
            user: {
                username: '', // Not updating username here
                real_name: editForm.name,
                phone: editForm.phone,
                email: editForm.email,
                role: 'staff',
                gender: editForm.gender
            },
            position: editForm.position,
            department: editForm.department
        });
        ElMessage.success('更新成功');
        showEditDialog.value = false;
        loadStaff();
    } catch (error) {
        ElMessage.error('更新失败');
    }
};

const handleDelete = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定删除该员工吗？此操作不可恢复', '警告', {
        type: 'warning',
        confirmButtonText: '确定删除',
        cancelButtonText: '取消'
    });
    await deleteStaff(id);
    ElMessage.success('员工删除成功');
    loadStaff();
  } catch (e) {
    if (e !== 'cancel') {
        console.error(e);
        ElMessage.error('员工删除失败');
    }
  }
};

const handleUpdateAccount = async () => {
    try {
        // Update user status and password via dedicated endpoint or updateStaff
        // Assuming updateStaff can handle nested user updates including status
        // But password usually requires separate endpoint or special handling
        
        // Use a direct API call for user update if needed, or rely on updateStaff
        // backend's StaffUserViewSet should handle nested user updates
        
        const updateData: any = {
             user: {
                 role: 'staff', // required by type definition
                 status: accountForm.status
             }
        };
        if (accountForm.newPassword) {
            updateData.user.password = accountForm.newPassword;
        }
        
        // Note: Check if backend supports partial nested update for user
        // If not, might need to provide all user fields.
        // For safety, let's assume we need a specific user update endpoint or full payload.
        // Let's try updateStaff first.
        
        await updateStaff(accountForm.staffId, updateData);
        
        ElMessage.success('账户更新成功');
        showAccountDialog.value = false;
        loadStaff();
    } catch (error) {
        ElMessage.error('账户更新失败');
    }
};
</script>

<style scoped>
.staff-management-view {
  padding: 20px;
}
</style>
