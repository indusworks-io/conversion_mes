
<script setup lang="ts">
import { ref, computed } from 'vue';
import StartButtonPopup from '../components/StartButtonPopup.vue';

// Define props, including currentStatus
const props = defineProps<{
  orderId: string;
  workstationId: string;
  currentStatus: string; // Add currentStatus as a prop
}>();

const emit = defineEmits(['update-status']); // Emit event to update status in the parent

const showPopup = ref(false);
const errorMessage = ref<string | null>(null);
const loading = ref(false);
const isStopped = computed(() => props.currentStatus === 'Stopped');

// Start Order Function
const startOrder = async (operator: string) => {
  console.log('Start Order:', props.orderId, 'Operator:', operator);
  loading.value = true;
  errorMessage.value = null;

  try {
    const response = await fetch('/api/method/conversion_mes.api.start_order', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        order_name: props.orderId,
        operator: operator,
      }),
    });

    const data = await response.json();

    if (data.message && data.message.status) {
      console.log('Order started successfully:', data.message.message);
      emit('update-status', 'In Progress'); // Update status in the parent
    } else {
      console.error('Failed to start order:', data.message.message);
      errorMessage.value = data.message.message || 'Failed to start order';
    }
  } catch (error) {
    console.error('Error starting order:', error);
    errorMessage.value = 'Server error';
  } finally {
    loading.value = false;
  }
};

const stopOrder = async () => {
  console.log('Stop Order:', props.orderId);
  loading.value = true;
  errorMessage.value = null;

  try {
    const response = await fetch('/api/method/conversion_mes.api.stop_order', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        order_name: props.orderId,
      }),
    });

    const data = await response.json();

    if (data.message && data.message.status) {
      console.log('Order stopped successfully:', data.message.message);
      emit('update-status', 'Stopped'); // Update status in the parent
      isStopped.value = true;
    } else {
      console.error('Failed to stop order:', data.message.message);
      errorMessage.value = data.message.message || 'Failed to stop order';
    }
  } catch (error) {
    console.error('Error stopping order:', error);
    errorMessage.value = 'Server error';
  } finally {
    loading.value = false;
  }

  showPopup.value = false;
};

const resumeOrder = async () => {
  console.log('Resume Order:', props.orderId);
  loading.value = true;
  errorMessage.value = null;

  try {
    const response = await fetch('/api/method/conversion_mes.api.resume_order', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        order_name: props.orderId,
      }),
    });

    const data = await response.json();

    if (data.message && data.message.status) {
      console.log('Order resumed successfully:', data.message.message);
      emit('update-status', 'In Progress'); // Update status in the parent
      isStopped.value = false;
    } else {
      console.error('Failed to resume order:', data.message.message);
      errorMessage.value = data.message.message || 'Failed to resume order';
    }
  } catch (error) {
    console.error('Error resuming order:', error);
    errorMessage.value = 'Server error';
  } finally {
    loading.value = false;
  }
};

const logScrap = () => {
  console.log('Log Scrap:', props.orderId);
};

const batchSerial = () => {
  console.log('Batch/Serial:', props.orderId);
};

const logOutput = () => {
  console.log('Log Output:', props.orderId);
};

const completeOrder = async () => {
  console.log('Complete Order:', props.orderId);
  loading.value = true;
  errorMessage.value = null;

  try {
    const response = await fetch('/api/method/conversion_mes.api.complete_order', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        order_name: props.orderId,
      }),
    });

    const data = await response.json();

    if (data.message && data.message.status) {
      console.log('Order completed successfully:', data.message.message);
      emit('update-status', 'Completed'); // Update status in the parent
    } else {
      console.error('Failed to complete order:', data.message.message);
      errorMessage.value = data.message.message || 'Failed to complete order';
    }
  } catch (error) {
    console.error('Error completing order:', error);
    errorMessage.value = 'Server error';
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="flex flex-row p-2 space-y-4">
    <!-- Start Button -->
    <button
      v-if="currentStatus === 'Not Started'"
      @click="showPopup = true"
      class="px-6 py-2 bg-green-500 text-white text-sm font-medium rounded hover:bg-green-600 transition-colors uppercase"
    >
      Start
    </button>

    <!-- Stop/Resume Button -->
    <button
      v-if="currentStatus === 'In Progress' || currentStatus === 'Stopped'"
      @click="isStopped ? resumeOrder() : stopOrder()"
      :class="{
        'bg-red-500 hover:bg-red-600': !isStopped,
        'bg-blue-500 hover:bg-blue-600': isStopped,
      }"
      class="px-6 py-2 text-white text-sm font-medium rounded transition-colors uppercase"
    >
      {{ isStopped ? 'Resume' : 'Stop' }}
    </button>

    <!-- Log Scrap Button -->
    <button
      v-if="currentStatus !== 'Not Started'"
      @click="logScrap"
      class="px-6 py-2 bg-blue-500 text-white text-sm font-medium rounded hover:bg-blue-600 transition-colors uppercase"
    >
      Log Scrap
    </button>

    <!-- Batch/Serial Button -->
    <button
      v-if="currentStatus !== 'Not Started'"
      @click="batchSerial"
      class="px-6 py-2 bg-purple-500 text-white text-sm font-medium rounded hover:bg-purple-600 transition-colors uppercase"
    >
      Batch/Serial
    </button>

    <!-- Log Output Button -->
    <button
      v-if="currentStatus !== 'Not Started'"
      @click="logOutput"
      class="px-6 py-2 bg-yellow-500 text-white text-sm font-medium rounded hover:bg-yellow-600 transition-colors uppercase"
    >
      Log Output
    </button>

    <!-- Complete Button -->
    <button
      v-if="currentStatus !== 'Not Started'"
      @click="completeOrder"
      class="px-6 py-2 bg-gray-500 text-white text-sm font-medium rounded hover:bg-gray-600 transition-colors uppercase"
    >
      Complete
    </button>

    <!-- Error Message -->
    <div v-if="errorMessage" class="text-red-500 text-sm mt-2">
      {{ errorMessage }}
    </div>

    <!-- Popup -->
    <StartButtonPopup
      v-if="showPopup"
      :workstationID="props.workstationId"
      @close="showPopup = false"
      @start-order="startOrder"
    />
  </div>
</template>
=======
<template>
  <div class="bg-gray-100 p-8">
    <div class="max-w-4xl mx-auto">
      <div class="grid grid-cols-4 gap-8">
        <!-- Left side - State Display -->
        <div class="col-span-1 bg-white p-6 rounded-lg shadow-md">
          <h2 class="text-lg font-semibold mb-4">Current State</h2>
          <div :class="{
            'text-sm font-medium': true,
            'text-orange-500': currentState === 'Not Started',
            'text-blue-500': currentState === 'In Progress',
            'text-green-500': currentState === 'Complete'
          }">
            {{ currentState }}
          </div>
        </div>

        <!-- Right side - Buttons -->
        <div class="col-span-3 space-y-4">
          <template v-if="!isStarted">
            <button
              @click="handleStart"
              class="flex items-center gap-2 bg-green-500 text-white px-6 py-3 rounded-md hover:bg-green-600 transition-colors"
            >
              <Play class="w-5 h-5" />
              START
            </button>
          </template>
          <template v-else>
            <div class="space-y-4">
              <div class="flex gap-4">
                <button
                  @click="handleStepComplete('BATCH/SERIAL')"
                  :class="{
                    'flex items-center gap-2 px-6 py-3 rounded-md transition-colors': true,
                    'bg-blue-500 text-white hover:bg-blue-600': true
                  }"
                >
                  <FileSpreadsheet class="w-5 h-5" />
                  BATCH/SERIAL
                </button>

                <button
                  @click="handleStepComplete('LOG OUTPUT')"
                  :class="{
                    'flex items-center gap-2 px-6 py-3 rounded-md transition-colors': true,
                    'bg-blue-500 text-white hover:bg-blue-600': true
                  }"
                >
                  <FileOutput class="w-5 h-5" />
                  LOG OUTPUT
                </button>

                <button
                  @click="handleStepComplete('LOG SCRAP')"
                  :class="{
                    'flex items-center gap-2 px-6 py-3 rounded-md transition-colors': true,
                    'bg-blue-500 text-white hover:bg-blue-600': true
                  }"
                >
                  <FileWarning class="w-5 h-5" />
                  LOG SCRAP
                </button>
              </div>

              <div class="flex gap-4">
                <button
                  @click="handleComplete"
                  :disabled="completedSteps.length < 3"
                  :class="{
                    'flex items-center gap-2 px-6 py-3 rounded-md transition-colors': true,
                    'bg-gray-300 cursor-not-allowed': completedSteps.length < 3,
                    'bg-green-500 text-white hover:bg-green-600': completedSteps.length === 3
                  }"
                >
                  <CheckCircle class="w-5 h-5" />
                  COMPLETE
                </button>

                <button
                  @click="handleStopResume"
                  :class="{
                    'flex items-center gap-2 px-6 py-3 rounded-md transition-colors': true,
                    'bg-red-500 text-white hover:bg-red-600': !isPaused,
                    'bg-blue-500 text-white hover:bg-blue-600': isPaused
                  }"
                >
                  <StopCircle v-if="!isPaused" class="w-5 h-5" />
                  <Play v-else class="w-5 h-5" />
                  {{ isPaused ? 'RESUME' : 'STOP' }}
                </button>
              </div>
            </div>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { Play, FileSpreadsheet, FileOutput, FileWarning, CheckCircle, StopCircle } from 'lucide-vue-next';

const isStarted = ref(false);
const isPaused = ref(false);
const currentState = ref('Not Started');
const completedSteps = ref<string[]>([]);

const handleStart = () => {
  isStarted.value = true;
  currentState.value = 'In Progress';
};

const handleStepComplete = (step: string) => {
  if (!completedSteps.value.includes(step)) {
    completedSteps.value.push(step);
  }

  if (completedSteps.value.length === 3) {
    currentState.value = 'Complete';
  }
};

const handleComplete = () => {
  if (completedSteps.value.length === 3) {
    currentState.value = 'Complete';
  }
};

const handleStopResume = () => {
  isPaused.value = !isPaused.value;
  if (isPaused.value) {
    currentState.value = 'Paused';
  } else {
    currentState.value = 'In Progress';
  }
};
</script>