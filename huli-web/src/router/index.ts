import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router';
import { useAuthStore } from '@/stores/auth'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/LoginView.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/auth/register/family',
    name: 'FamilyRegister',
    component: () => import('@/views/auth/FamilyRegisterView.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/family',
    name: 'Family',
    component: () => import('@/layouts/FamilyLayout.vue'),
    meta: { requiresAuth: true, role: 'family' },
    children: [
      {
        path: '',
        name: 'FamilyRoot',
        redirect: '/family/dashboard'
      },
      {
        path: 'dashboard',
        name: 'FamilyDashboard',
        component: () => import('@/views/family/DashboardView.vue')
      },
      {
        path: 'appointments',
        name: 'Appointments',
        component: () => import('@/views/family/AppointmentsView.vue')
      },
      {
        path: 'messages',
        name: 'Messages',
        component: () => import('@/views/family/MessagesView.vue')
      }
      ,
      {
        path: 'payments',
        name: 'Payments',
        component: () => import('@/views/family/PaymentsView.vue')
      },
      {
        path: 'custom-services',
        name: 'CustomServices',
        component: () => import('@/views/family/CustomServicesView.vue')
      },
      {
        path: 'care-reminders',
        name: 'CareReminders',
        component: () => import('@/views/family/CareRemindersView.vue')
      }
    ]
  },
  {
    path: '/staff',
    name: 'Staff',
    component: () => import('@/layouts/StaffLayout.vue'),
    meta: { requiresAuth: true, role: 'staff' },
    children: [
      {
        path: '',
        name: 'StaffRoot',
        redirect: '/staff/dashboard'
      },
      {
        path: 'dashboard',
        name: 'StaffDashboard',
        component: () => import('@/views/staff/DashboardView.vue')
      },
      
      {
        path: 'patients',
        name: 'StaffPatients',
        component: () => import('@/views/staff/PatientsView.vue')
      },
      {
        path: 'messages',
        name: 'StaffMessages',
        component: () => import('@/views/staff/MessagesView.vue')
      },
      {
        path: 'announcements',
        name: 'StaffAnnouncements',
        component: () => import('@/views/staff/AnnouncementsView.vue')
      },
      {
        path: 'schedule',
        name: 'Schedule',
        component: () => import('@/views/staff/ScheduleView.vue')
      },
      {
        path: 'care-records',
        name: 'CareRecords',
        component: () => import('@/views/staff/CareRecordsView.vue')
      },
      {
        path: 'activity-gallery',
        name: 'ActivityGallery',
        component: () => import('@/views/staff/ActivityGalleryView.vue')
      },
      {
        path: 'activity-gallery/:id',
        name: 'ActivityGalleryDetail',
        component: () => import('@/views/staff/ActivityGalleryDetailView.vue')
      },
      {
        path: 'bed-scheduling',
        name: 'BedScheduling',
        component: () => import('@/views/staff/BedSchedulingView.vue')
      }
    ]
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('@/layouts/AdminLayout.vue'),
    meta: { requiresAuth: true, role: 'admin' },
    children: [
      {
        path: '',
        name: 'AdminRoot',
        redirect: '/admin/dashboard'
      },
      {
        path: 'dashboard',
        name: 'AdminDashboard',
        component: () => import('@/views/admin/DashboardView.vue')
      },
      {
        path: 'users',
        name: 'Users',
        component: () => import('@/views/admin/UsersView.vue')
      },
      {
        path: 'services',
        name: 'Services',
        component: () => import('@/views/admin/ServicesView.vue')
      },
      {
        path: 'elderly',
        name: 'ElderlyManagement',
        component: () => import('@/views/admin/ElderlyManagementView.vue')
      },
      {
        path: 'staff',
        name: 'StaffManagement',
        component: () => import('@/views/admin/StaffManagementView.vue')
      },
      {
        path: 'announcements',
        name: 'Announcements',
        component: () => import('@/views/admin/AnnouncementsView.vue')
      },
      {
        path: 'approvals',
        name: 'Approvals',
        component: () => import('@/views/admin/ApprovalsView.vue')
      },
      {
        path: 'reports',
        name: 'Reports',
        component: () => import('@/views/admin/ReportsView.vue')
      }
    ]
  },
  {
    path: '/forbidden',
    name: 'Forbidden',
    component: () => import('@/views/error/ForbiddenView.vue')
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/error/NotFoundView.vue')
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach(async (to, _from, next) => {
  const authStore = useAuthStore()
  
  console.log('路由守卫检查:', {
    path: to.path,
    name: to.name,
    requiresAuth: to.meta.requiresAuth,
    isAuthenticated: authStore.isAuthenticated,
    userRole: authStore.user?.role,
    metaRole: to.meta.role
  })
  
  // Check authentication - if auth required and not authenticated, redirect to login
  if (to.meta.requiresAuth !== false && !authStore.isAuthenticated) {
    console.log('未认证，重定向到登录页')
    return next({ name: 'Login', query: { redirect: to.fullPath } });
  }
  
  // Check role permission only if user is authenticated and route has role requirement
  if (authStore.isAuthenticated && to.meta.role && authStore.user?.role !== to.meta.role) {
    console.log('角色不匹配，重定向到禁止访问页')
    // In a real app, redirect to Forbidden page or Home
    return next({ name: 'Forbidden' })
  }
  
  // Redirect logged in users away from login page
  if (to.name === 'Login' && authStore.isAuthenticated) {
    const role = authStore.user?.role
    const homeRoute = role === 'admin' ? '/admin' : role === 'staff' ? '/staff' : '/family';
    console.log('已登录用户访问登录页，重定向到:', homeRoute)
    return next(homeRoute);
  }
  
  console.log('路由守卫通过，允许访问')
  next();
});

export default router;
