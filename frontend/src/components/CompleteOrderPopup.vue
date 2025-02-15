<script setup lang="ts">
import { ref, computed, reactive } from 'vue';
import { createDocumentResource } from 'frappe-ui';

const props = defineProps<{
  orderId: string;
}>();

const emit = defineEmits(['close', 'update-status']);

// Fetch Manufacturing Order details using createDocumentResource
const orderdetails = createDocumentResource({
  doctype: 'Manufacturing Order',
  name: props.orderId,
  auto: true,
});

// Function to calculate the sum of completed quantities for a specific item
const getCompletedQty = (itemCode) => {
  if (!orderdetails?.doc?.output_logs || !Array.isArray(orderdetails.doc.output_logs)) {
    return 0;
  }

  return orderdetails.doc.output_logs
    .filter(log => log.item === itemCode)
    .reduce((sum, log) => sum + (log?.quantity || 0), 0);
};

// Function to calculate the sum of scraped quantities for a specific item
const getScrapedQty = (itemCode) => {
  if (!orderdetails?.doc?.scrap_logs || !Array.isArray(orderdetails.doc.scrap_logs)) {
    return 0;
  }

  return orderdetails.doc.scrap_logs
    .filter(log => log.item === itemCode)
    .reduce((sum, log) => sum + (log?.quantity || 0), 0);
};


// Toast notification state
const showToast = ref(false);
const toastMessage = ref('');

// Function to show toast for 2 seconds
const showSuccessToast = (message: string) => {
  toastMessage.value = message;
  showToast.value = true;
  setTimeout(() => {
    showToast.value = false;
  }, 2000);
};


// Function to complete the order
const completeOrder = async () => {
  try {
    const response = await fetch('/api/method/conversion_mes.api.complete_order', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        order_name: props.orderId,
      }),
    });

    const data = await response.json();

    if (data.message.message) {
      console.log('Order completed successfully:', data.message.message);
      showSuccessToast(data.message.message); // Show success popup
      emit('update-status'); // Emit event to update status
      emit('close'); // Close the popup
    } else {
      console.error('Failed to complete order:', data.message);
    }
  } catch (error) {
    console.error('Error completing order:', error);
  }
};
</script>

<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
    <div class="bg-white p-6 rounded-lg shadow-lg w-auto">
      <h2 class="text-lg font-semibold mb-4">Complete Manufacturing Order</h2>

      <!-- Output Item Table -->
      <table class="min-w-full border border-black text-black">
        <thead class="bg-gray-100">
          <tr>
            <th class="px-4 py-2 border">S. No.</th>
            <th class="px-4 py-2 border">Item Code</th>
            <th class="px-4 py-2 border">UOM</th>
            <th class="px-4 py-2 border">Planed Qty</th>
            <th class="px-4 py-2 border">Completed Qty</th>
            <th class="px-4 py-2 border">Scraped Qty</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in orderdetails.doc.planned_output" :key="index">
            <td class="px-4 py-2 border text-center">{{ index + 1 }}</td>
            <td class="px-4 py-2 border">{{ item.item }}</td>
            <td class="px-4 py-2 border text-center">{{ item.uom }}</td>
            <td class="px-4 py-2 border text-center">{{ item.quantity }}</td>
            <td class="px-4 py-2 border text-center">{{ getCompletedQty(item.item) }}</td>
            <td class="px-4 py-2 border text-center">{{ getScrapedQty(item.item) }}</td>
          </tr>
        </tbody>
      </table>

      <!-- Action Buttons -->
      <div class="flex justify-end mt-4">
        <button @click="emit('close')" class="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600">
          Cancel
        </button>
        <button @click="completeOrder" class="ml-2 px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600">
          Complete
        </button>

        
      </div>

       <!-- Toast Notification -->
       <div
          v-if="showToast"
          class="fixed bottom-4 right-4 bg-green-500 text-white px-4 py-2 rounded-lg shadow-md transition-opacity duration-300"
        >
          {{ toastMessage }}
        </div>
    </div>
  </div>
</template>