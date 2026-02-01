import { ref } from 'vue'

const receiverId = ref('')
const receiverName = ref('')
const messages = ref<any[]>([])
const loading = ref(false)
const familyUsers = ref<any[]>([])
const showUserSelector = ref(false)

export {
  receiverId,
  receiverName,
  messages,
  loading,
  familyUsers,
  showUserSelector
}