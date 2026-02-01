<template>
  <div style="padding:24px">
    <el-result icon="warning" title="禁止访问" sub-title="您没有访问该页面的权限">
      <template #extra>
        <el-button type="primary" @click="$router.push('/login')">返回登录</el-button>
      </template>
    </el-result>
  </div>
</template>

<script setup lang="ts">
</script>
