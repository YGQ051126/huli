<template>
  <el-container class="staff-layout" style="height: 100%">
    <!-- 顶部导航栏 -->
    <el-header class="staff-header">
      <div class="header-left">
        <el-button
          type="text"
          @click="toggleCollapse"
          :icon="isCollapse ? 'Menu' : 'Fold'"
          class="menu-toggle-btn"
        >
        </el-button>
        <div class="logo">
          <el-icon><HomeFilled /></el-icon>
          <span class="logo-text">护理平台 - 员工端</span>
        </div>
        <el-breadcrumb separator="/" class="breadcrumb">
          <el-breadcrumb-item :to="{ path: '/staff/dashboard' }">工作台</el-breadcrumb-item>
          <el-breadcrumb-item>{{ currentPageTitle }}</el-breadcrumb-item>
        </el-breadcrumb>
      </div>
      <div class="header-right">
        <el-dropdown>
          <el-button type="text" :icon="'User'" class="user-btn">
            <span>{{ username }}</span>
            <el-icon class="el-icon--right"><ArrowDown /></el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item>个人中心</el-dropdown-item>
              <el-dropdown-item>排班管理</el-dropdown-item>
              <el-dropdown-item>系统设置</el-dropdown-item>
              <el-dropdown-item divided @click="handleLogout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </el-header>
    
    <el-container class="main-container">
      <!-- 侧边栏 -->
      <el-aside
        :width="isCollapse ? '80px' : '240px'"
        class="staff-sidebar"
        :class="{ 'sidebar-collapsed': isCollapse }"
      >
        <el-menu
          router
          :default-active="activeMenu"
          :collapse="isCollapse"
          unique-opened
          :background-color="'var(--sidebar-bg)'"
          text-color="#fff"
          active-text-color="var(--primary-color)"
        >
          <el-menu-item index="/staff/dashboard" :icon="'Monitor'">
            <template #title>
              <span>工作台</span>
            </template>
          </el-menu-item>
          <el-menu-item index="/staff/patients" :icon="'UserFilled'">
            <template #title>
              <span>患者管理</span>
            </template>
          </el-menu-item>
          <el-menu-item index="/staff/messages" :icon="'Message'">
            <template #title>
              <span>沟通中心</span>
            </template>
          </el-menu-item>
          <el-menu-item index="/staff/announcements" :icon="'Document'">
            <template #title>
              <span>公告中心</span>
            </template>
          </el-menu-item>
          <el-menu-item index="/staff/care-records" :icon="'Document'">
            <template #title>
              <span>护理记录</span>
            </template>
          </el-menu-item>
          
          <el-menu-item index="/staff/activity-gallery">
            <template #title>
              <span>活动相册</span>
            </template>
          </el-menu-item>
          <el-menu-item index="/staff/bed-scheduling" :icon="'Grid'">
            <template #title>
              <span>床位调度</span>
            </template>
          </el-menu-item>
          <el-menu-item index="/staff/schedule" :icon="'Calendar'">
            <template #title>
              <span>排班管理</span>
            </template>
          </el-menu-item>
        </el-menu>
      </el-aside>
      
      <!-- 主内容区域 -->
      <el-main class="staff-main">
        <router-view v-slot="{ Component }">
          <transition name="fade-transform" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';

const route = useRoute();
const router = useRouter();

// 侧边栏折叠状态
const isCollapse = ref(false);

// 用户名
const username = ref('护理人员');

// 用户状态管理
const userStore = useUserStore();

// 切换侧边栏折叠状态
const toggleCollapse = () => {
  isCollapse.value = !isCollapse.value;
};

// 当前激活菜单
const activeMenu = computed(() => {
  return route.path;
});

// 当前页面标题
const currentPageTitle = computed(() => {
    const titleMap: Record<string, string> = {
      '/staff/dashboard': '工作台',
      '/staff/patients': '患者管理',
      '/staff/messages': '沟通中心',
      '/staff/announcements': '公告中心',
      '/staff/care-records': '护理记录',
      '/staff/activity-gallery': '活动相册',
      '/staff/bed-scheduling': '床位调度',
      '/staff/schedule': '排班管理'
    };
    return titleMap[route.path] || '员工中心';
  });

// 退出登录
const handleLogout = () => {
  // 调用userStore的logout方法清除用户状态和token
  userStore.logout();
  // 跳转到登录页面
  router.push('/login');
};

// 监听路由变化，更新页面标题
watch(
  () => route.path,
  () => {
    // 可以在这里添加页面访问记录等逻辑
  }
);
</script>

<style scoped>
.staff-layout {
  font-family: var(--font-family);
  background-color: var(--bg-color);
}

/* 顶部导航栏 */
.staff-header {
  background-color: var(--header-bg);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
  height: 64px;
  z-index: 100;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

/* Logo */
.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 500;
  color: var(--primary-color);
}

/* 面包屑 */
.breadcrumb {
  margin: 0;
  font-size: 14px;
}

/* 侧边栏 */
.staff-sidebar {
  background-color: var(--sidebar-bg);
  transition: width 0.3s ease;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.sidebar-collapsed .el-menu-item .el-icon,
.sidebar-collapsed .el-sub-menu .el-sub-menu__icon-arrow {
  margin-right: 0;
}

/* 菜单切换按钮 */
.menu-toggle-btn {
  font-size: 18px;
  color: var(--text-primary);
  padding: 8px;
}

.menu-toggle-btn:hover {
  color: var(--primary-color);
  background-color: var(--bg-color);
}

/* 用户按钮 */
.user-btn {
  color: var(--text-primary);
  font-size: 14px;
  padding: 8px 16px;
  border-radius: var(--border-radius);
  transition: var(--transition-base);
}

.user-btn:hover {
  background-color: var(--bg-color);
}

/* 主内容区域 */
.staff-main {
  padding: 24px;
  overflow-y: auto;
  background-color: var(--bg-color);
}

/* 动画效果 */
.fade-transform-enter-active,
.fade-transform-leave-active {
  transition: all 0.3s ease;
}

.fade-transform-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.fade-transform-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

/* 响应式设计 */
@media screen and (max-width: 768px) {
  .logo-text {
    display: none;
  }
  
  .breadcrumb {
    display: none;
  }
  
  .staff-sidebar {
    position: fixed;
    left: 0;
    top: 64px;
    bottom: 0;
    z-index: 999;
    width: 240px;
    transition: transform 0.3s ease;
  }
  
  .sidebar-collapsed {
    transform: translateX(-100%);
  }
}
</style>
