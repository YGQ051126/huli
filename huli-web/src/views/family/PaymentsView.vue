<template>
  <div class="payments-view">
    <!-- 顶部 -->
    <div class="header">
      <div class="title-section">
        <h2 class="page-title">月度费用明细</h2>
        <span class="current-month">当前账期: {{ currentMonth }}</span>
      </div>
      <el-button 
        type="primary" 
        :icon="Refresh" 
        :loading="refreshing" 
        @click="handleRefresh"
      >
        刷新账单
      </el-button>
    </div>

    <!-- 列表 -->
    <el-card class="list-card" shadow="never">
      <el-table 
        ref="tableRef"
        :data="bills" 
        v-loading="loading" 
        @selection-change="handleSelectionChange"
        row-key="id"
      >
        <el-table-column type="selection" width="55" :selectable="canSelect" />
        <el-table-column prop="id" label="账单编号" width="100" />
        <el-table-column prop="bill_type" label="费用类型" width="120">
            <template #default="{ row }">
                {{ getBillTypeLabel(row.bill_type) }}
            </template>
        </el-table-column>
        <el-table-column prop="total_amount" label="金额 (元)" width="120">
          <template #default="{ row }">
            <span class="amount">? {{ Number(row.total_amount).toFixed(2) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="出账日期" width="180">
            <template #default="{ row }">
                {{ formatDate(row.created_at) }}
            </template>
        </el-table-column>
        <el-table-column prop="status" label="状态">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">{{ getStatusLabel(row.status) }}</el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 底部工具栏 -->
    <div class="footer-toolbar">
      <div class="left">
        <el-checkbox 
          v-model="allSelected" 
          :indeterminate="isIndeterminate" 
          @change="toggleSelectAll"
          :disabled="bills.length === 0"
        >
          全选
        </el-checkbox>
        <span class="selected-count" v-if="selectedBills.length > 0">
            已选 {{ selectedBills.length }} 项
        </span>
      </div>
      <div class="right">
        <div class="total-info">
            合计: <span class="total-amount">? {{ totalAmount.toFixed(2) }}</span>
        </div>
        <el-button 
            type="primary" 
            size="large" 
            :disabled="selectedBills.length === 0"
            @click="handlePay"
        >
            立即支付
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Refresh } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox, type TableInstance } from 'element-plus'
import { getBills, refreshBills, createPayment, type Bill } from '@/services/family/payment'
import dayjs from 'dayjs'

const bills = ref<Bill[]>([])
const loading = ref(false)
const refreshing = ref(false)
const selectedBills = ref<Bill[]>([])
const tableRef = ref<TableInstance>()

const currentMonth = computed(() => dayjs().format('YYYY-MM'))

const totalAmount = computed(() => {
    return selectedBills.value.reduce((sum, bill) => {
        return sum + (Number(bill.total_amount) - Number(bill.paid_amount))
    }, 0)
})

const allSelected = computed({
    get: () => bills.value.length > 0 && selectedBills.value.length === bills.value.filter(b => b.status !== 'paid').length,
    set: (_val) => { /* handled by toggleSelectAll */ }
})

const isIndeterminate = computed(() => {
    return selectedBills.value.length > 0 && selectedBills.value.length < bills.value.filter(b => b.status !== 'paid').length
})

const fetchBills = async () => {
    loading.value = true
    try {
        const res = await getBills()
        // Ensure res is an array
        bills.value = Array.isArray(res) ? res : (res as any).results || []
    } catch (error) {
        ElMessage.error('获取账单失败')
        bills.value = []
    } finally {
        loading.value = false
    }
}

const handleRefresh = async () => {
    refreshing.value = true
    try {
        const res = await refreshBills()
        if (res.created > 0) {
            ElMessage.success(`已生成 ${res.created} 条新账单`)
        } else {
            ElMessage.info('暂无新账单')
        }
        await fetchBills()
    } catch (error) {
        ElMessage.error('刷新失败')
    } finally {
        refreshing.value = false
    }
}

const handleSelectionChange = (selection: Bill[]) => {
    selectedBills.value = selection
}

const canSelect = (row: Bill) => {
    return row.status !== 'paid'
}

const toggleSelectAll = (val: boolean) => {
    if (val) {
        const selectable = bills.value.filter(b => b.status !== 'paid')
        selectable.forEach(row => {
            tableRef.value?.toggleRowSelection(row, true)
        })
    } else {
        tableRef.value?.clearSelection()
    }
}

const handlePay = async () => {
    if (selectedBills.value.length === 0) return

    try {
        await ElMessageBox.confirm(
            `已选 ${selectedBills.value.length} 笔账单，合计 ? ${totalAmount.value.toFixed(2)}，确认支付？`,
            '支付确认',
            {
                confirmButtonText: '确认',
                cancelButtonText: '取消',
                type: 'warning'
            }
        )
        
        // Call API
        const billIds = selectedBills.value.map(b => b.id)
        await createPayment(billIds)
        
        ElMessage.success('支付成功')
        selectedBills.value = [] // Clear selection
        await fetchBills() // Refresh list
        
    } catch (error) {
        if (error !== 'cancel') {
            ElMessage.error('支付发起失败')
        }
    }
}

const formatDate = (date: string) => dayjs(date).format('YYYY-MM-DD HH:mm')

const getBillTypeLabel = (type: string) => {
    const map: Record<string, string> = {
        monthly: '月度账单',
        service: '服务账单',
        deposit: '押金',
        other: '其他'
    }
    return map[type] || type
}

const getStatusLabel = (status: string) => {
    const map: Record<string, string> = {
        unpaid: '未支付',
        paid: '已支付',
        partially_paid: '部分支付'
    }
    return map[status] || status
}

const getStatusType = (status: string) => {
    const map: Record<string, string> = {
        unpaid: 'danger',
        paid: 'success',
        partially_paid: 'warning'
    }
    return map[status] || 'info'
}

onMounted(fetchBills)
</script>

<style scoped>
.payments-view {
    padding: 20px;
    padding-bottom: 80px; /* Space for footer */
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.title-section {
    display: flex;
    align-items: baseline;
    gap: 12px;
}

.page-title {
    margin: 0;
    font-size: 20px;
}

.current-month {
    color: #909399;
    font-size: 14px;
}

.list-card {
    border-radius: 8px;
}

.amount {
    font-weight: bold;
    color: #303133;
}

.footer-toolbar {
    position: fixed;
    bottom: 0;
    left: 200px; /* Sidebar width approx */
    right: 0;
    height: 64px;
    background: #fff;
    box-shadow: 0 -2px 12px rgba(0, 0, 0, 0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 24px;
    z-index: 100;
}

.left {
    display: flex;
    align-items: center;
    gap: 16px;
}

.right {
    display: flex;
    align-items: center;
    gap: 24px;
}

.total-info {
    font-size: 16px;
}

.total-amount {
    font-size: 24px;
    font-weight: bold;
    color: #f56c6c;
    margin-left: 8px;
}

@media (max-width: 768px) {
    .footer-toolbar {
        left: 0;
    }
}
</style>
