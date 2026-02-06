<template>
  <div class="reports-view">
    <div class="page-header">
      <h1 class="page-title">数据与报表</h1>
      <p class="page-subtitle">生成各类统计报表，支持图表展示和导出</p>
    </div>
    
    <el-card class="content-card">
      <el-tabs v-model="activeTab" class="report-tabs">
        <el-tab-pane label="生成报表" name="statistics">
          <div class="report-generator">
            <div class="filter-section">
              <el-select 
                v-model="reportType" 
                placeholder="选择报表类型" 
                class="filter-item"
              >
                <el-option label="月度护理记录" value="monthly-care" />
                <el-option label="财务收支统计" value="finance" />
              </el-select>
              <el-date-picker 
                v-model="reportDate" 
                type="month" 
                placeholder="选择年月"
                format="YYYY年MM月"
                value-format="YYYY-MM"
                class="filter-item"
              />
              <el-button 
                type="primary" 
                @click="generateReport"
                :loading="generating"
                :icon="TrendCharts"
                class="generate-btn"
              >
                生成报表
              </el-button>
            </div>
            
            <!-- 报表内容展示 -->
            <div v-if="reportData" class="report-content">
              <div class="report-header">
                <h2 class="report-title">{{ reportTitle }}</h2>
                <div class="report-info">
                  <el-tag type="info" class="info-tag">
                    <el-icon><Clock /></el-icon>
                    生成日期: {{ new Date().toLocaleDateString('zh-CN') }}
                  </el-tag>
                  <el-tag type="info" class="info-tag">
                    <el-icon><Calendar /></el-icon>
                    数据月份: {{ reportDate ? `${reportDate.split('-')[0]}年${reportDate.split('-')[1]}月` : '全部' }}
                  </el-tag>
                </div>
              </div>
              
              <!-- 图表展示 -->
              <div class="chart-section">
                <div class="chart-header">
                  <h3 class="chart-title">数据趋势图表</h3>
                  <el-radio-group v-model="chartType" size="small" class="chart-type-selector">
                    <el-radio-button label="line">折线图</el-radio-button>
                    <el-radio-button label="bar">柱状图</el-radio-button>
                    <el-radio-button label="pie">饼图</el-radio-button>
                  </el-radio-group>
                </div>
                <div class="chart-container">
                  <div ref="chartRef" class="chart"></div>
                </div>
              </div>
              
              <!-- 数据表格 -->
              <div class="table-section">
                <h3 class="table-title">详细数据</h3>
                <el-table 
                  :data="reportTableData" 
                  class="report-table"
                  stripe
                  border
                  max-height="400"
                >
                  <el-table-column 
                    v-for="column in reportColumns" 
                    :key="column.prop" 
                    :prop="column.prop" 
                    :label="column.label"
                    :min-width="column.minWidth || 120"
                    :sortable="column.sortable !== false"
                  />
                </el-table>
              </div>
              
              <!-- 导出操作 -->
              <div class="export-section">
                <el-button 
                  type="success" 
                  @click="exportReport('excel')"
                  :icon="Document"
                  class="export-btn"
                >
                  导出Excel
                </el-button>
<!-- PDF Export Removed -->
                <el-button 
                  type="info" 
                  @click="saveReport"
                  :icon="Download"
                  class="export-btn"
                >
                  保存报表
                </el-button>
              </div>
            </div>
            
            <!-- 空状态 -->
            <el-empty 
              v-else 
              description="请选择报表类型和日期，然后点击生成报表"
              class="empty-state"
            >
              <template #image>
                <div class="empty-icon">
                  <TrendCharts style="font-size: 64px; color: #c0c4cc;" />
                </div>
              </template>
            </el-empty>
          </div>
        </el-tab-pane>
        
        <el-tab-pane label="历史报表" name="history">
          <div class="history-section">
            <div class="history-header">
              <el-input
                v-model="historySearch"
                placeholder="搜索报表名称"
                class="history-search"
                :prefix-icon="Search"
                clearable
              />
              <el-button 
                type="danger" 
                @click="clearHistory"
                :icon="Delete"
                :disabled="historicalReports.length === 0"
                class="clear-btn"
              >
                清空历史
              </el-button>
            </div>
            
            <el-table 
              :data="filteredHistoricalReports" 
              class="history-table"
              stripe
              border
              v-loading="historyLoading"
            >
              <el-table-column prop="reportName" label="报表名称" min-width="200">
                <template #default="scope">
                  <div class="report-name-cell">
                    <el-icon><Document /></el-icon>
                    <span>{{ scope.row.reportName }}</span>
                  </div>
                </template>
              </el-table-column>
              <el-table-column prop="reportType" label="报表类型" width="120">
                <template #default="scope">
                  <el-tag :type="getReportTypeTag(scope.row.reportType)" size="small">
                    {{ getReportTypeLabel(scope.row.reportType) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="generatedDate" label="生成日期" width="150">
                <template #default="scope">
                  <div class="date-cell">
                    <el-icon><Clock /></el-icon>
                    <span>{{ formatDate(scope.row.generatedDate) }}</span>
                  </div>
                </template>
              </el-table-column>
              <el-table-column prop="dataMonth" label="数据月份" width="120">
                <template #default="scope">
                  <span>{{ formatMonth(scope.row.dataMonth) }}</span>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="200" fixed="right">
                <template #default="scope">
                  <div class="history-actions">

                    <el-button 
                      type="success" 
                      size="small" 
                      @click="downloadReport(scope.row)"
                      :icon="Download"
                      class="action-btn"
                    >
                      下载
                    </el-button>
                    <el-button 
                      type="danger" 
                      size="small" 
                      @click="deleteReport(scope.row.id)"
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
              v-if="totalHistoryCount > historyPageSize"
              v-model:current-page="historyCurrentPage"
              v-model:page-size="historyPageSize"
              :total="totalHistoryCount"
              :page-sizes="[10, 20, 50]"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="handleHistorySizeChange"
              @current-change="handleHistoryCurrentChange"
              class="history-pagination"
            />
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick, watch } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import * as echarts from 'echarts';
import { TrendCharts, Document, Clock, Calendar, Search, Download, Delete } from '@element-plus/icons-vue';
import api from '@/services/api';

interface ReportColumn {
  prop: string;
  label: string;
  minWidth?: number;
  sortable?: boolean;
}

interface ReportTableItem {
  [key: string]: any;
}

interface HistoricalReport {
  id: number;
  reportName: string;
  reportType: string;
  generatedDate: string;
  dataMonth: string;
  fileUrl: string;
}

const activeTab = ref('statistics');
const reportType = ref('monthly-care');
const reportDate = ref<string>('');
const reportData = ref(false);
const generating = ref(false);
const reportTitle = ref('');
const reportColumns = ref<ReportColumn[]>([]);
const reportTableData = ref<ReportTableItem[]>([]);
const chartRef = ref<HTMLElement | null>(null);
const chartType = ref('line');
let chartInstance: echarts.ECharts | null = null;

// 历史报表相关
const historySearch = ref('');
const historyLoading = ref(false);
const historyCurrentPage = ref(1);
const historyPageSize = ref(10);
const totalHistoryCount = ref(0);

// 历史数据
const historicalReports = ref<HistoricalReport[]>([]);

const filteredHistoricalReports = computed(() => {
  if (!historySearch.value) return historicalReports.value;
  return historicalReports.value.filter(item => 
    item.reportName.toLowerCase().includes(historySearch.value.toLowerCase())
  );
});

const generateReport = async () => {
  if (!reportType.value) {
    ElMessage.warning('请选择报表类型');
    return;
  }
  
  generating.value = true;
  try {
    // Call API to fetch real data
    const response = await api.get('/admin/reports/data/', {
      params: {
        type: reportType.value,
        month: reportDate.value || undefined
      }
    });
    
    ElMessage.success('报表生成成功');
    
    // 设置报表标题和数据
    reportTitle.value = getReportTitle(reportType.value, reportDate.value);
    reportColumns.value = getReportColumns(reportType.value);
    
    // Response should be the data array directly or wrapped
    const data = Array.isArray(response) ? response : (response as any).data || [];
    reportTableData.value = data;
    
    reportData.value = true;
    
    // Save to history
    const newReport: HistoricalReport = {
      id: Date.now(),
      reportName: reportTitle.value,
      reportType: reportType.value,
      generatedDate: new Date().toISOString().split('T')[0] || '',
      dataMonth: reportDate.value || new Date().toISOString().slice(0, 7),
      fileUrl: '#'
    };
    historicalReports.value.unshift(newReport);
    
    // 初始化图表
    await nextTick();
    initChart();
  } catch (error) {
    console.error('Fetch report failed', error);
    ElMessage.error('获取报表数据失败');
    reportData.value = false;
  } finally {
    generating.value = false;
  }
};

const getReportTitle = (type: string, date: string) => {
  const dateStr = date || '当期';
  const typeMap: Record<string, string> = {
    'monthly-care': '月度护理记录报表',
    'finance': '财务收支统计报表'
  };
  return `${dateStr} - ${typeMap[type] || '综合报表'}`;
};

const getReportColumns = (type: string): ReportColumn[] => {
  switch (type) {
    case 'monthly-care':
      return [
        { prop: 'elderlyName', label: '老人姓名', minWidth: 120 },
        { prop: 'totalRecords', label: '护理记录数', minWidth: 120, sortable: true },
        { prop: 'notes', label: '备注' }
      ];
    case 'finance':
      return [
        { prop: 'date', label: '日期', minWidth: 120, sortable: true },
        { prop: 'type', label: '收支类型', minWidth: 100 },
        { prop: 'item', label: '项目名称', minWidth: 150 },
        { prop: 'amount', label: '金额 (元)', minWidth: 120, sortable: true }
      ];
    default:
      return [];
  }
};

// getReportData removed - using API

const initChart = () => {
  if (chartRef.value) {
    chartInstance = echarts.init(chartRef.value);
    
    let xAxisData: string[] = [];
    let seriesData: number[] = [];
    const data = reportTableData.value || [];
    
    if (reportType.value === 'monthly-care') {
        xAxisData = data.map((item: any) => item.elderlyName);
        seriesData = data.map((item: any) => item.totalRecords);
    } else if (reportType.value === 'finance') {
        xAxisData = data.map((item: any) => `${item.date}\n${item.item}`);
        seriesData = data.map((item: any) => item.amount);
    }
    
    const option = {
      title: {
        text: getChartTitle(reportType.value),
        left: 'center',
        textStyle: {
          fontSize: 16,
          fontWeight: 'normal'
        }
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        }
      },
      legend: {
        data: ['数据'],
        top: 30
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: xAxisData,
        axisLabel: { interval: 0, rotate: 30 }
      },
      yAxis: {
        type: 'value'
      },
      series: [
        {
          name: '数据',
          data: seriesData,
          type: chartType.value,
          barMaxWidth: 50,
          itemStyle: {
            color: '#409EFF'
          }
        }
      ]
    };
    
    chartInstance.setOption(option);
  }
};

const getChartTitle = (type: string): string => {
  const titles: Record<string, string> = {
    'monthly-care': '月度护理记录趋势',
    'health-status': '健康状况变化趋势',
    'finance': '财务收支对比'
  };
  return titles[type] || '数据趋势';
};

const exportReport = async (format: 'excel' | 'pdf') => {
  if (format === 'pdf') {
    ElMessage.warning('PDF导出功能暂未开放');
    return;
  }
  
  ElMessage.success(`正在导出${format === 'excel' ? 'Excel' : 'PDF'}格式报表`);
  
  try {
    const response = await api.get('/admin/reports/export/', {
      params: {
        type: reportType.value,
        month: reportDate.value || undefined
      },
      responseType: 'blob'
    });
    
    // Create blob link to download
    // Api interceptor returns response.data directly if it doesn't have {code, data} structure
    // So response is the Blob object here
    const blob = new Blob([response as any], { 
      type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' 
    });
    
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    
    // Filename logic
    const dateStr = reportDate.value || 'all';
    const filename = `report_${reportType.value}_${dateStr}.xlsx`;
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
    
    ElMessage.success('导出成功');
  } catch (error) {
    console.error('Export failed', error);
    ElMessage.error('导出失败');
  }
};

const saveReport = () => {
  ElMessage.success('报表已保存到历史记录');
};

const downloadReport = async (report: HistoricalReport) => {
  ElMessage.success(`正在下载报表: ${report.reportName}`);
  try {
    // 模拟下载 - 实际上应该调用后端导出接口
    // 这里我们重用 export 接口逻辑，传入历史记录的类型
    // 注意：真实场景下历史记录应该存储了生成好的文件路径(fileUrl)
    // 如果没有文件路径，则实时生成导出
    
    if (report.fileUrl && report.fileUrl !== '#') {
        window.open(report.fileUrl, '_blank');
        return;
    }

    const response = await api.get('/admin/reports/export/', {
      params: {
        type: report.reportType,
        month: report.dataMonth
      },
      responseType: 'blob' // Important for file download
    });
    
    // Create blob link to download
    const url = window.URL.createObjectURL(new Blob([response as any]));
    const link = document.createElement('a');
    link.href = url;
    // Filename logic
    const filename = `${report.reportName}.xlsx`;
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
  } catch (error) {
    console.error('Download failed', error);
    ElMessage.error('下载失败');
  }
};

const deleteReport = (id: number) => {
  ElMessageBox.confirm('确定删除该历史报表吗？', '删除确认', {
    type: 'warning',
    confirmButtonText: '确定删除',
    cancelButtonText: '取消'
  }).then(() => {
    const index = historicalReports.value.findIndex(item => item.id === id);
    if (index > -1) {
      historicalReports.value.splice(index, 1);
      ElMessage.success('删除成功');
    }
  });
};

const clearHistory = () => {
  ElMessageBox.confirm('确定清空所有历史报表吗？此操作不可恢复。', '清空确认', {
    type: 'warning',
    confirmButtonText: '确定清空',
    cancelButtonText: '取消'
  }).then(() => {
    historicalReports.value = [];
    ElMessage.success('历史报表已清空');
  }).catch(() => {
    // 用户取消操作
  });
};

const handleHistorySizeChange = (val: number) => {
  historyPageSize.value = val;
  historyCurrentPage.value = 1;
};

const handleHistoryCurrentChange = (val: number) => {
  historyCurrentPage.value = val;
};

const getReportTypeTag = (type: string): string => {
  const tags: Record<string, string> = {
    'monthly-care': 'primary',
    'health-status': 'success',
    'finance': 'danger'
  };
  return tags[type] || 'info';
};

const getReportTypeLabel = (type: string): string => {
  const labels: Record<string, string> = {
    'monthly-care': '护理记录',
    'health-status': '健康分析',
    'finance': '财务统计'
  };
  return labels[type] || type;
};

const formatDate = (str: string): string => {
  return new Date(str).toLocaleDateString('zh-CN');
};

const formatMonth = (month: string): string => {
  const [year, m] = month.split('-');
  return `${year}年${m}月`;
};

// 监听图表类型变化
watch(chartType, () => {
  if (chartInstance) {
    initChart();
  }
});

onMounted(() => {
  // 设置默认日期为当前月份
  const now = new Date();
  reportDate.value = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`;
});
</script>

<style scoped>
.reports-view {
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

.report-tabs :deep(.el-tabs__header) {
  margin-bottom: 24px;
}

.report-tabs :deep(.el-tabs__item) {
  font-size: 16px;
  font-weight: 500;
}

.filter-section {
  display: flex;
  gap: 16px;
  align-items: center;
  margin-bottom: 32px;
  padding: 20px;
  background: #f8f9fb;
  border-radius: 8px;
  border: 1px solid #ebeef5;
}

.filter-item {
  min-width: 180px;
}

.generate-btn {
  background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%);
  border: none;
  font-weight: 500;
  transition: all 0.3s ease;
}

.generate-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}

.generate-btn:active {
  transform: translateY(0);
}

.report-content {
  padding: 8px;
}

.report-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  padding-bottom: 20px;
  border-bottom: 2px solid #ebeef5;
}

.report-title {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
  margin: 0;
}

.report-info {
  display: flex;
  gap: 16px;
}

.info-tag {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
}

.chart-section {
  margin-bottom: 32px;
  padding: 24px;
  background: #ffffff;
  border-radius: 8px;
  border: 1px solid #ebeef5;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.chart-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin: 0;
}

.chart-type-selector {
  display: flex;
}

.chart-container {
  height: 400px;
  border: 1px solid #ebeef5;
  border-radius: 6px;
  overflow: hidden;
}

.chart {
  width: 100%;
  height: 100%;
}

.table-section {
  margin-bottom: 32px;
  padding: 24px;
  background: #ffffff;
  border-radius: 8px;
  border: 1px solid #ebeef5;
}

.table-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 16px 0;
}

.report-table {
  border-radius: 6px;
}

.export-section {
  display: flex;
  justify-content: center;
  gap: 16px;
  padding: 24px;
  background: #ffffff;
  border-radius: 8px;
  border: 1px solid #ebeef5;
}

.export-btn {
  transition: all 0.3s ease;
  border-radius: 6px;
  font-weight: 500;
}

.export-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.export-btn:active {
  transform: translateY(0);
}

.empty-state {
  margin: 60px 0;
}

.empty-icon {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 16px;
}

.history-section {
  padding: 8px;
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.history-search {
  width: 300px;
}

.clear-btn {
  transition: all 0.3s ease;
  border-radius: 6px;
}

.clear-btn:hover:not(.is-disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(245, 108, 108, 0.3);
}

.clear-btn:active:not(.is-disabled) {
  transform: translateY(0);
}

.history-table {
  border-radius: 6px;
}

.report-name-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}

.date-cell {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #606266;
}

.history-actions {
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

.action-btn:active {
  transform: translateY(0);
}

.history-pagination {
  margin-top: 24px;
  display: flex;
  justify-content: center;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .reports-view {
    padding: 16px;
  }
  
  .filter-section {
    flex-direction: column;
    align-items: stretch;
  }
  
  .filter-item {
    min-width: auto;
  }
  
  .report-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  
  .report-info {
    flex-direction: column;
    gap: 8px;
  }
  
  .chart-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  
  .chart-type-selector {
    width: 100%;
  }
  
  .export-section {
    flex-direction: column;
    align-items: center;
  }
  
  .history-header {
    flex-direction: column;
    align-items: stretch;
    gap: 16px;
  }
  
  .history-search {
    width: 100%;
  }
  
  .history-actions {
    flex-direction: column;
  }
}

@media (max-width: 480px) {
  .page-title {
    font-size: 20px;
  }
  
  .chart-container {
    height: 300px;
  }
}
</style>