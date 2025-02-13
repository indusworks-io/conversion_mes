<script setup lang="ts">
import { ref } from 'vue';
import StartButtonPopup from '../components/StartButtonPopup.vue';
import BatchSerialPopup from './BatchSerialPopup.vue';

// Define props
const props = defineProps<{
  orderId: string;
  workstationId: string;
  currentStatus: string;
}>();

const emit = defineEmits(['update-status']); // Emit event to update status in the parent

const showBatchSerialPopup = ref(false);
const showPopup = ref(false);
const errorMessage = ref<string | null>(null);
const loading = ref(false);

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
      emit('update-status', 'In Progress'); // Change status to "In Progress"
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

// Stop Order Function
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
      emit('update-status', 'Not Started'); // Change status back to "Not Started"
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

const logScrap = () => {
  console.log('Log Scrap:', props.orderId);
};

const batchSerial = () => {
  console.log('Batch/Serial:', props.orderId);
};
const handleBatchSerialLogged = (data: any) => {
  console.log('Batch/Serial logged:', data);
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
    <!-- Start/Stop Toggle Button -->
    <button
      v-if="currentStatus === 'Not Started' || currentStatus === 'Stopped'"
      @click="showPopup = true"
      class="px-6 py-2 bg-green-500 text-white text-sm font-medium rounded hover:bg-green-600 transition-colors uppercase"
    >
      Start
    </button>

    <button
      v-if="currentStatus === 'In Progress'"
      @click="stopOrder"
      class="px-6 py-2 bg-red-500 text-white text-sm font-medium rounded hover:bg-red-600 transition-colors uppercase"
    >
      Stop
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
      @click="showBatchSerialPopup = true"
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
      
      v-if="currentStatus !== 'Not Started' && currentStatus !== 'Completed'"
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

    <!-- Popup Component -->
    <BatchSerialPopup
      v-if="showBatchSerialPopup"
      :orderId="orderId"
      :workstationId="workstationId"
      :show="showBatchSerialPopup"
      @close="showBatchSerialPopup = false"
      @logged="handleBatchSerialLogged"
    />
  </div>
</template>
