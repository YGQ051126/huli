<template>
  <div class="login-container">
    <div class="login-form-wrapper">
      <div class="login-title">
        <h1>护理平台管理系统</h1>
        <p>请登录您的账号</p>
      </div>
      <el-card class="login-card">
        <el-form 
          :model="form" 
          :rules="rules" 
          ref="formRef"
          label-position="top"
        >
          <el-form-item label="用户名" prop="username">
            <el-input 
              v-model="form.username" 
              placeholder="请输入用户名"
              size="large"
              :prefix-icon="User"
            />
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input 
              v-model="form.password" 
              type="password" 
              placeholder="请输入密码"
              size="large"
              :prefix-icon="Lock"
              show-password
            />
          </el-form-item>
          <el-form-item>
            <el-button 
              type="primary" 
              @click="handleLogin" 
              size="large"
              :loading="isLoading"
              block
            >
              登录
            </el-button>
          </el-form-item>
          <div class="login-footer">
            <div style="margin-bottom: 20px; text-align: center;">
              <el-button type="text" @click="router.push('/auth/register/family')">家属账号注册</el-button>
            </div>
          <div class="login-tips">
            <span class="login-tip">家属账号：family / family123</span>
            <span class="login-tip">员工账号：staff3 / staff123</span>
            <span class="login-tip">管理员账号：admin / admin123</span>
          </div>
        </div>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'
import { User, Lock } from '@element-plus/icons-vue'
import type { FormInstance, FormRules } from 'element-plus'

const userStore = useUserStore()
const router = useRouter()
const formRef = ref<FormInstance>()
const isLoading = ref(false)

const form = reactive({
  username: '',
  password: ''
})

const rules = reactive<FormRules>({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ]
})

const handleLogin = async () => {
  console.log('开始登录，表单数据:', form)
  if (!formRef.value) {
    console.error('formRef未初始化')
    return
  }
  
  try {
    console.log('开始表单验证')
    await formRef.value.validate()
    console.log('表单验证通过')
    isLoading.value = true
    
    console.log('调用userStore.login，用户名:', form.username)
    // 调用登录方法
    await userStore.login({ 
      username: form.username, 
      password: form.password 
    })
    
    console.log('login方法执行完成，用户信息:', userStore.user)
    
    // 确保用户信息存在
    if (!userStore.user) {
      console.error('登录失败：用户信息未设置')
      return
    }
    
    // 根据角色跳转到对应页面
    const role = userStore.user.role
    console.log('用户角色:', role)
    let homePath = '/family/dashboard'
    
    if (role === 'admin') {
      homePath = '/admin/dashboard'
    } else if (role === 'staff') {
      homePath = '/staff/dashboard' // 直接跳转到员工仪表盘页面
    }
    
    console.log('跳转到:', homePath)
    router.push(homePath)
  } catch (error) {
    console.error('Login failed:', error)
    const message = error instanceof Error ? error.message : 'Unknown Error'
    // Use Element Plus instead of alert to avoid encoding issues
    const { ElMessage } = await import('element-plus')
    ElMessage.error(`Login Failed: ${message}`)
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-form-wrapper {
  width: 100%;
  max-width: 420px;
  animation: fadeIn 0.5s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.login-title {
  text-align: center;
  margin-bottom: 30px;
  color: #ffffff;
}

.login-title h1 {
  font-size: 28px;
  font-weight: 600;
  margin-bottom: 10px;
}

.login-title p {
  font-size: 16px;
  opacity: 0.9;
  color: #ffffff;
  margin: 0;
}

.login-card {
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border: none;
  overflow: hidden;
  background-color: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
}

.login-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
}

.login-card .el-card__body {
  padding: 40px 30px;
}

.login-footer {
  margin-top: 20px;
  text-align: center;
  font-size: 13px;
  color: var(--text-secondary);
}

.login-tip {
  background-color: var(--bg-color);
  padding: 6px 12px;
  border-radius: 15px;
  display: inline-block;
}

.login-tips {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 16px;
}

/* 响应式设计 */
@media screen and (max-width: 576px) {
  .login-card .el-card__body {
    padding: 30px 20px;
  }
  
  .login-title h1 {
    font-size: 24px;
  }
  
  .login-title p {
    font-size: 14px;
  }
  
  .login-tips {
    gap: 6px;
  }
  
  .login-tip {
    font-size: 12px;
  }
}
</style>
