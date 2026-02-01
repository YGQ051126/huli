<template>
  <div class="care-reminders-view">
    <h1>关怀提醒</h1>
    <el-card>
      <el-tabs v-model="activeTab">
        <el-tab-pane label="生日提醒" name="birthday">
          <el-table :data="birthdayReminders" style="margin-top: 20px">
            <el-table-column prop="elderlyName" label="老人姓名" />
            <el-table-column prop="birthday" label="生日" />
            <el-table-column prop="relationship" label="关系" />
            <el-table-column label="操作">
              <template #default="_scope">
                <el-button type="primary" size="small" @click="showGiftDialog = true">
                  送祝福
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="节日活动" name="festival">
          <el-table :data="festivalPlans" style="margin-top: 20px">
            <el-table-column prop="festivalName" label="节日名称" />
            <el-table-column prop="festivalDate" label="节日日期" />
            <el-table-column prop="planDescription" label="活动安排" />
            <el-table-column prop="participants" label="参与人数" />
            <el-table-column label="操作">
              <template #default="scope">
                <el-button type="success" size="small" @click="participateFestival(scope.row)">
                  报名参加
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <!-- 送祝福对话框 -->
    <el-dialog v-model="showGiftDialog" title="送祝福" width="600px">
      <el-form :model="giftForm" label-width="120px">
        <el-form-item label="祝福类型">
          <el-radio-group v-model="giftForm.giftType">
            <el-radio label="text">文字祝福</el-radio>
            <el-radio label="voice">语音祝福</el-radio>
            <el-radio label="gift">实物礼物</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item v-if="giftForm.giftType === 'text'" label="祝福内容">
          <el-input v-model="giftForm.content" type="textarea" rows="5" placeholder="请输入您的祝福内容..." />
        </el-form-item>
        <el-form-item v-if="giftForm.giftType === 'gift'" label="礼物描述">
          <el-input v-model="giftForm.giftDescription" placeholder="请输入礼物名称或描述" />
        </el-form-item>
        <el-form-item v-if="giftForm.giftType === 'gift'" label="配送方式">
          <el-select v-model="giftForm.deliveryType">
            <el-option label="寄送到院" value="home" />
            <el-option label="自行送达" value="pickup" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showGiftDialog = false">取消</el-button>
          <el-button type="primary" @click="submitGift">发送祝福</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { ElMessage } from 'element-plus';

const activeTab = ref('birthday');
const showGiftDialog = ref(false);

// 模拟数据
const birthdayReminders = ref([
  { id: 1, elderlyName: '张大爷', birthday: '2025-12-15', relationship: '父亲' },
  { id: 2, elderlyName: '李奶奶', birthday: '2025-12-20', relationship: '母亲' },
]);

const festivalPlans = ref([
  { id: 1, festivalName: '圣诞节联欢', festivalDate: '2025-12-25', planDescription: '院内举办圣诞联欢晚会，邀请家属参加，有精彩节目表演和礼品赠送。', participants: 50 },
  { id: 2, festivalName: '元旦茶话会', festivalDate: '2026-01-01', planDescription: '共迎新年，茶点招待，院长致辞。', participants: 30 },
]);

const giftForm = reactive({
  giftType: 'text',
  content: '',
  giftDescription: '',
  deliveryType: 'home',
});

const participateFestival = (plan: any) => {
  // 这里应该调用API报名参加
  ElMessage.success(`已成功报名参加${plan.festivalName}，期待您的到来`);
};

const submitGift = () => {
  // 这里应该调用API提交
  ElMessage.success('祝福已送达');
  showGiftDialog.value = false;
};
</script>

<style scoped>
.care-reminders-view {
  padding: 20px;
}
</style>