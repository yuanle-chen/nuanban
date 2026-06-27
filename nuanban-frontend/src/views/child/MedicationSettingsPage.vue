<template>
  <div class="min-h-screen bg-gray-50 pb-20">
    <!-- 顶部 -->
    <div class="bg-gradient-to-r from-blue-500 to-cyan-400 text-white p-6 pb-16 rounded-b-3xl">
      <div class="flex items-center gap-3 mb-4">
        <button @click="$router.back()" class="text-white text-lg">← 返回</button>
        <h1 class="text-xl font-bold">用药设置</h1>
      </div>
      <p class="text-white/80 text-sm">为老人设置用药计划</p>
    </div>

    <!-- 添加计划按钮 -->
    <div class="px-4 -mt-8">
      <button
        @click="showAddModal = true"
        class="w-full py-4 bg-white rounded-2xl shadow-md flex items-center justify-center gap-2 text-blue-500 font-semibold hover:bg-blue-50 transition-colors"
      >
        <span class="text-xl">+</span>
        <span>添加用药计划</span>
      </button>
    </div>

    <!-- 用药计划列表 -->
    <div class="px-4 mt-6">
      <div v-if="plans.length === 0" class="text-center text-gray-400 py-12">
        <p class="text-5xl mb-3">💊</p>
        <p>暂无用药计划</p>
        <p class="text-sm mt-1">点击上方按钮添加</p>
      </div>

      <div v-else class="space-y-4">
        <div
          v-for="plan in plans"
          :key="plan.id"
          class="bg-white rounded-2xl p-5 shadow-sm"
        >
          <div class="flex items-start justify-between mb-3">
            <div>
              <h3 class="text-lg font-bold text-gray-800">{{ plan.medication_name }}</h3>
              <p class="text-sm text-gray-500">{{ plan.dosage }} · {{ plan.frequency }}</p>
            </div>
            <div class="flex gap-2">
              <button
                @click="editPlan(plan)"
                class="p-2 text-blue-500 hover:bg-blue-50 rounded-lg"
              >
                ✏️
              </button>
              <button
                @click="togglePlan(plan)"
                class="p-2 rounded-lg"
                :class="plan.is_active ? 'text-green-500 hover:bg-green-50' : 'text-gray-400 hover:bg-gray-50'"
              >
                {{ plan.is_active ? '✅' : '⏸️' }}
              </button>
            </div>
          </div>
          <div class="flex flex-wrap gap-2">
            <span
              v-for="time in plan.reminder_times"
              :key="time"
              class="px-3 py-1 bg-blue-50 text-blue-600 rounded-full text-sm font-medium"
            >
              {{ time }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- 添加/编辑弹窗 -->
    <div
      v-if="showAddModal"
      class="fixed inset-0 bg-black/50 flex items-end justify-center z-50"
      @click.self="closeModal"
    >
      <div class="bg-white w-full max-w-sm rounded-t-3xl p-6 animate-slide-up">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-xl font-bold text-gray-800">
            {{ editingPlan ? '编辑用药计划' : '添加用药计划' }}
          </h2>
          <button @click="closeModal" class="text-gray-400 text-2xl">×</button>
        </div>

        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">药品名称 *</label>
            <input
              v-model="form.medication_name"
              type="text"
              placeholder="如：降压药"
              class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-300"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">剂量 *</label>
            <input
              v-model="form.dosage"
              type="text"
              placeholder="如：每次1片"
              class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-300"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">服用频率 *</label>
            <select
              v-model="form.frequency"
              class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-300"
            >
              <option value="每日一次">每日一次</option>
              <option value="每日两次">每日两次</option>
              <option value="每日三次">每日三次</option>
              <option value="饭后服用">饭后服用</option>
              <option value="睡前服用">睡前服用</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">提醒时间 *</label>
            <div class="flex flex-wrap gap-2 mb-2">
              <span
                v-for="(time, idx) in form.reminder_times"
                :key="idx"
                class="px-3 py-1 bg-blue-100 text-blue-600 rounded-full text-sm flex items-center gap-1"
              >
                {{ time }}
                <button @click="removeTime(idx)" class="ml-1 text-blue-400 hover:text-blue-600">×</button>
              </span>
            </div>
            <div class="flex gap-2">
              <input
                v-model="newTime"
                type="time"
                class="flex-1 px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-300"
              />
              <button
                @click="addTime"
                class="px-4 py-3 bg-blue-500 text-white rounded-xl hover:bg-blue-600"
              >
                添加
              </button>
            </div>
          </div>

          <button
            @click="handleSave"
            :disabled="saving"
            class="w-full py-3 bg-gradient-to-r from-blue-500 to-cyan-400 text-white font-semibold rounded-xl hover:opacity-90 transition-opacity disabled:opacity-50"
          >
            {{ saving ? '保存中...' : '保存' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useFamilyStore } from '../../stores/family'
import { getMedicationPlans, createMedicationPlan, updateMedicationPlan } from '../../api/medication'

const familyStore = useFamilyStore()
const plans = ref<any[]>([])
const showAddModal = ref(false)
const editingPlan = ref<any>(null)
const saving = ref(false)
const newTime = ref('')

const form = ref({
  medication_name: '',
  dosage: '',
  frequency: '每日一次',
  reminder_times: [] as string[],
})

function resetForm() {
  form.value = {
    medication_name: '',
    dosage: '',
    frequency: '每日一次',
    reminder_times: [],
  }
  newTime.value = ''
  editingPlan.value = null
}

function addTime() {
  if (!newTime.value) return
  if (form.value.reminder_times.includes(newTime.value)) {
    alert('该时间已添加')
    return
  }
  form.value.reminder_times.push(newTime.value)
  form.value.reminder_times.sort()
  newTime.value = ''
}

function removeTime(idx: number) {
  form.value.reminder_times.splice(idx, 1)
}

async function loadPlans() {
  if (!familyStore.currentElder?.id) return
  try {
    const res: any = await getMedicationPlans(familyStore.currentElder.id)
    plans.value = res
  } catch (error) {
    console.error('加载用药计划失败', error)
  }
}

function editPlan(plan: any) {
  editingPlan.value = plan
  form.value = {
    medication_name: plan.medication_name,
    dosage: plan.dosage,
    frequency: plan.frequency,
    reminder_times: [...plan.reminder_times],
  }
  showAddModal.value = true
}

async function togglePlan(plan: any) {
  try {
    await updateMedicationPlan(plan.id, { is_active: !plan.is_active })
    await loadPlans()
  } catch (err: any) {
    alert(err.response?.data?.detail || '操作失败')
  }
}

function closeModal() {
  showAddModal.value = false
  resetForm()
}

async function handleSave() {
  if (!form.value.medication_name) {
    alert('请输入药品名称')
    return
  }
  if (!form.value.dosage) {
    alert('请输入剂量')
    return
  }
  if (form.value.reminder_times.length === 0) {
    alert('请至少添加一个提醒时间')
    return
  }
  if (!familyStore.currentElder?.id) {
    alert('请先绑定老人')
    return
  }

  saving.value = true
  try {
    if (editingPlan.value) {
      await updateMedicationPlan(editingPlan.value.id, form.value)
    } else {
      await createMedicationPlan({
        elder_user_id: familyStore.currentElder.id,
        ...form.value,
      })
    }
    alert('保存成功！')
    closeModal()
    await loadPlans()
  } catch (err: any) {
    alert(err.response?.data?.detail || '保存失败')
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  if (!familyStore.currentElder) {
    await familyStore.fetchElders()
  }
  loadPlans()
})
</script>

<style>
@keyframes slide-up {
  from { transform: translateY(100%); }
  to { transform: translateY(0); }
}
.animate-slide-up {
  animation: slide-up 0.3s ease-out;
}
</style>
