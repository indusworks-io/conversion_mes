<script setup lang="ts">
import { ref, watch } from 'vue';
import { createDocumentResource } from 'frappe-ui'; // Assuming you're using Frappe UI

const props = defineProps<{
  orderId: string;
  workstationId: string;
  operator: string | null;
  show: boolean;
}>();

const emit = defineEmits(['close', 'logged','update-status']);

const operator = ref<string>(props.operator || '');
console.log(props.operator)
const itemName = ref<string>('');
const batchSerialNumber = ref<string>('');
const loading = ref(false);
const errorMessage = ref<string | null>(null);

// Fetch Manufacturing Order details using createDocumentResource
const orderDetails = createDocumentResource({
  doctype: 'Manufacturing Order',
  name: props.orderId, // Use the orderId prop to fetch the specific order
  fields: ['operator', 'planned_output'], // Fetch operator and planned_output
  auto: true, // Automatically fetch data when the component is mounted
  onSuccess() {
      
  },
  onError(error: any) {
    console.error('Error fetching manufacturing order:', error);
    errorMessage.value = 'Failed to fetch order details';
  },
});


// Watch for changes in `show` to reload data when the popup is opened
watch(
  () => props.show,
  (newVal) => {
    if (newVal) {
      orderDetails.reload(); // Reload data when the popup is opened
    }
  }
);

const logBatchSerial = async () => {
  if (!operator.value || !batchSerialNumber.value) {
    errorMessage.value = 'Please fill in all fields.';
    return;
  }

  loading.value = true;
  errorMessage.value = null;

  try {
    const response = await fetch('/api/method/conversion_mes.api.log_batch_serial_number', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        order_name: props.orderId,
        operator: operator.value,
        
        batch_serial_number: batchSerialNumber.value,
      }),
    });

    const data = await response.json();

    if (data) {
      console.log('Batch/Serial logged successfully:');
      emit('update-status');
      emit('logged', {
        operator: operator.value,
        
        batchSerialNumber: batchSerialNumber.value,
      });
      emit('close');
    } else {
      console.error('Failed to log batch/serial:', data.message);
      errorMessage.value = data.message || 'Failed to log batch/serial number';
    }
  } catch (error) {
    console.error('Error logging batch/serial:', error);
    errorMessage.value = 'Server error';
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div v-if="show" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
    <div class="bg-white border border-black p-6 rounded-lg shadow-lg w-96">
      <h2 class="text-lg font-bold mb-4">Log Batch/Serial Number</h2>

      <!-- Error Message -->
      <div v-if="errorMessage" class="text-red-500 text-sm mb-3">
        {{ errorMessage }}
      </div>

      <!-- Operator Input -->
      <!-- <label class="block mb-2 text-sm font-medium text-black">Operator:</label>
      <input
        v-model="operator"
        type="text"
        class="w-full border border-black rounded-md px-3 py-2 text-black bg-white"
        placeholder="Enter operator name"
        readonly
      /> -->

      <!-- Batch/Serial Number Input -->
      <label class="block mb-2 text-sm font-medium text-black mt-3">Batch/Serial Number:</label>
      <input
        v-model="batchSerialNumber"
        type="text"
        class="w-full border border-black rounded-md px-3 py-2 text-black bg-white"
        placeholder="Enter batch/serial number"
      />

      <!-- Buttons -->
      <div class="mt-4 flex justify-between">
        <button
          @click="emit('close')"
          class="px-4 py-2 border border-black text-black rounded-md bg-white hover:bg-gray-100"
        >
          Cancel
        </button>
        <button
          @click="logBatchSerial"
          :disabled="loading"
          class="px-4 py-2 bg-black text-white rounded-md hover:bg-gray-800 disabled:opacity-50"
        >
          {{ loading ? 'Logging...' : 'Log' }}
        </button>
      </div>
    </div>
  </div>
</template>