<template>
  <div class="login-container">
    <div class="login-form-wrapper">
      <div class="login-title">
        <h1>家属账号注册</h1>
        <p>填写关联院民信息及关系证明</p>
      </div>
      <el-card class="login-card">
        <el-form 
          :model="form" 
          :rules="rules" 
          ref="formRef"
          label-position="top"
        >
          <el-form-item label="用户名" prop="username">
            <el-input v-model="form.username" placeholder="设置登录用户名" :prefix-icon="User" />
          </el-form-item>
          
          <el-form-item label="密码" prop="password">
            <el-input 
              v-model="form.password" 
              type="password" 
              placeholder="设置登录密码" 
              :prefix-icon="Lock" 
              show-password 
            />
          </el-form-item>
          
          <el-form-item label="确认密码" prop="confirmPassword">
            <el-input 
              v-model="form.confirmPassword" 
              type="password" 
              placeholder="再次输入密码" 
              :prefix-icon="Lock" 
              show-password 
            />
          </el-form-item>

          <el-form-item label="真实姓名" prop="real_name">
            <el-input v-model="form.real_name" placeholder="您的真实姓名" />
          </el-form-item>

          <el-form-item label="联系电话" prop="phone">
            <el-input v-model="form.phone" placeholder="您的手机号码" />
          </el-form-item>

          <el-divider>关联信息</el-divider>

          <el-form-item label="关联院民身份证号" prop="patient_id_card">
            <el-input v-model="form.patient_id_card" placeholder="请输入关联老人的身份证号" />
          </el-form-item>

          <el-form-item label="与院民关系" prop="relationship">
            <el-select v-model="form.relationship" placeholder="请选择关系" style="width: 100%">
              <el-option label="子女" value="child" />
              <el-option label="配偶" value="spouse" />
              <el-option label="亲戚" value="relative" />
              <el-option label="其他" value="other" />
            </el-select>
          </el-form-item>
          
          <!-- 暂时简化文件上传，或者后续添加 -->
          <!-- <el-form-item label="关系证明文件" prop="proof_file">
             <el-upload ...>
               <el-button type="primary">点击上传</el-button>
             </el-upload>
          </el-form-item> -->

          <el-form-item>
            <el-button 
              type="primary" 
              @click="handleRegister" 
              :loading="isLoading"
              block
              size="large"
            >
              提交注册
            </el-button>
            <div style="margin-top: 10px; text-align: center; width: 100%">
              <el-button type="text" @click="router.push('/login')">已有账号？去登录</el-button>
            </div>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { User, Lock } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { registerFamily } from '@/services/auth'

const router = useRouter()
const formRef = ref<FormInstance>()
const isLoading = ref(false)

const form = reactive({
  username: '',
  password: '',
  confirmPassword: '',
  real_name: '',
  phone: '',
  patient_id_card: '',
  relationship: ''
})

const validatePass2 = (_rule: any, value: any, callback: any) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== form.password) {
    callback(new Error('两次输入密码不一致!'))
  } else {
    callback()
  }
}

const rules = reactive<FormRules>({
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ],
  confirmPassword: [{ validator: validatePass2, trigger: 'blur' }],
  real_name: [{ required: true, message: '请输入真实姓名', trigger: 'blur' }],
  phone: [{ required: true, message: '请输入手机号码', trigger: 'blur' }],
  patient_id_card: [{ required: true, message: '请输入关联老人身份证号', trigger: 'blur' }],
  relationship: [{ required: true, message: '请选择关系', trigger: 'change' }]
})

const handleRegister = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    isLoading.value = true
    
    // 构造提交数据
    const submitData = {
      user: {
        username: form.username,
        password: form.password,
        real_name: form.real_name,
        phone: form.phone,
        role: 'family'
      },
      patient_id_card: form.patient_id_card,
      relationship: form.relationship
    }
    
    await registerFamily(submitData)
    ElMessage.success('注册成功，请登录')
    router.push('/login')
    
  } catch (error: any) {
    console.error('Register failed:', error)
    const msg = error.response?.data?.message || error.message || '注册失败'
    ElMessage.error(msg)
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-form-wrapper {
  width: 100%;
  max-width: 460px;
  animation: fadeIn 0.5s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
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
  background-color: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
}

.login-card :deep(.el-card__body) {
  padding: 40px 30px;
}
</style>