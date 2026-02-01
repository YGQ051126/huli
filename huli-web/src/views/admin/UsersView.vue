<template>
  <div class="users-view">
    <div class="header-actions">
      <h1 class="page-title">用户管理</h1>
      <el-button type="primary" @click="openAddDialog">添加用户</el-button>
    </div>

    <el-card>
      <div class="search-bar">
        <el-input 
          v-model="searchQuery" 
          placeholder="搜索用户名或姓名" 
          style="width: 300px" 
          clearable 
          @input="handleSearch"
        />
      </div>

      <el-table :data="filteredUsers" v-loading="isLoading" stripe border>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="用户名" width="150" />
        <el-table-column prop="real_name" label="真实姓名" width="120" />
        <el-table-column prop="role" label="角色" width="120">
          <template #default="{ row }">
            <el-tag :type="getRoleTagType(row.role)">{{ getRoleLabel(row.role) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="phone" label="电话" width="150" />
        <el-table-column prop="email" label="邮箱" width="200" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'info'">{{ row.status === 'active' ? '活跃' : '停用' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" fixed="right" width="200">
          <template #default="{ row }">
            <el-button size="small" @click="openEditDialog(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 用户表单对话框 -->
    <el-dialog 
      v-model="dialogVisible" 
      :title="isEditMode ? '编辑用户' : '添加用户'"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" :disabled="isEditMode" placeholder="请输入用户名" />
        </el-form-item>
        
        <el-form-item 
          label="密码" 
          prop="password" 
          v-if="!isEditMode"
        >
          <el-input v-model="form.password" type="password" show-password placeholder="请输入密码" />
        </el-form-item>

        <el-form-item label="真实姓名" prop="real_name">
          <el-input v-model="form.real_name" placeholder="请输入真实姓名" />
        </el-form-item>

        <el-form-item label="角色" prop="role">
          <el-select v-model="form.role" placeholder="请选择角色" :disabled="isEditMode">
            <el-option label="管理员" value="admin" />
            <el-option label="员工" value="staff" />
            <el-option label="家属" value="family" />
          </el-select>
        </el-form-item>

        <el-form-item label="电话" prop="phone">
          <el-input v-model="form.phone" placeholder="请输入电话号码" />
        </el-form-item>

        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" placeholder="请输入邮箱" />
        </el-form-item>

        <el-form-item label="状态" prop="status" v-if="isEditMode">
          <el-select v-model="form.status">
            <el-option label="活跃" value="active" />
            <el-option label="停用" value="inactive" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm" :loading="isSubmitting">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { getUsers, createUser, updateUser, deleteUser } from '@/services/admin/users'
import type { User } from '@/types/user'

const isLoading = ref(false)
const isSubmitting = ref(false)
const users = ref<User[]>([])
const searchQuery = ref('')
const dialogVisible = ref(false)
const isEditMode = ref(false)
const formRef = ref<FormInstance>()

const form = reactive({
  id: '',
  username: '',
  password: '',
  real_name: '',
  role: 'staff',
  phone: '',
  email: '',
  status: 'active'
})

const rules = reactive<FormRules>({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少 6 位', trigger: 'blur' }
  ],
  real_name: [
    { required: true, message: '请输入真实姓名', trigger: 'blur' }
  ],
  role: [
    { required: true, message: '请选择角色', trigger: 'change' }
  ],
  phone: [
    { required: true, message: '请输入电话号码', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入有效的手机号', trigger: 'blur' }
  ]
})

const filteredUsers = computed(() => {
  if (!searchQuery.value) return users.value
  const query = searchQuery.value.toLowerCase()
  return users.value.filter(user => 
    user.username.toLowerCase().includes(query) || 
    (user.real_name && user.real_name.toLowerCase().includes(query))
  )
})

const loadUsers = async () => {
  isLoading.value = true
  try {
    users.value = await getUsers()
  } catch (error) {
    console.error('Load users error:', error)
    ElMessage.error('加载用户列表失败')
  } finally {
    isLoading.value = false
  }
}

const handleSearch = () => {
  // Client-side filtering handled by computed property
}

const openAddDialog = () => {
  isEditMode.value = false
  form.id = ''
  form.username = ''
  form.password = ''
  form.real_name = ''
  form.role = 'staff'
  form.phone = ''
  form.email = ''
  form.status = 'active'
  dialogVisible.value = true
}

const openEditDialog = (row: User) => {
  isEditMode.value = true
  form.id = String(row.id)
  form.username = row.username
  form.password = '' // Password not editable here
  form.real_name = row.real_name
  form.role = row.role
  form.phone = row.phone
  form.email = row.email || ''
  form.status = row.status
  dialogVisible.value = true
}

const submitForm = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      isSubmitting.value = true
      try {
        if (isEditMode.value) {
          await updateUser(form.id, {
            real_name: form.real_name,
            phone: form.phone,
            email: form.email,
            status: form.status as 'active' | 'inactive' | 'pending'
          })
          ElMessage.success('更新成功')
        } else {
          await createUser({
            username: form.username,
            password: form.password,
            real_name: form.real_name,
            role: form.role as any,
            phone: form.phone,
            email: form.email,
            status: 'active'
          })
          ElMessage.success('创建成功')
        }
        dialogVisible.value = false
        loadUsers()
      } catch (error) {
        console.error('Submit error:', error)
        ElMessage.error(isEditMode.value ? '更新失败' : '创建失败')
      } finally {
        isSubmitting.value = false
      }
    }
  })
}

const handleDelete = (row: User) => {
  ElMessageBox.confirm(
    `确定要删除用户 "${row.username}" 吗？`,
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(async () => {
    try {
      await deleteUser(String(row.id))
      ElMessage.success('删除成功')
      loadUsers()
    } catch (error) {
      console.error('Delete error:', error)
      ElMessage.error('删除失败')
    }
  })
}

const getRoleLabel = (role: string) => {
  const map: Record<string, string> = {
    admin: '管理员',
    staff: '员工',
    family: '家属'
  }
  return map[role] || role
}

const getRoleTagType = (role: string) => {
  const map: Record<string, string> = {
    admin: 'danger',
    staff: 'primary',
    family: 'success'
  }
  return map[role] || 'info' as any
}

const formatDate = (dateStr: string) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString()
}

onMounted(() => {
  loadUsers()
})
</script>

<style scoped>
.users-view {
  padding: 20px;
}
.header-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.page-title {
  font-size: 24px;
  font-weight: bold;
  margin: 0;
}
.search-bar {
  margin-bottom: 20px;
}
</style>
