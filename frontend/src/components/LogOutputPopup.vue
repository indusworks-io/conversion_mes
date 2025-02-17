<script setup lang="ts">
import { ref, computed, reactive } from 'vue';
import { createDocumentResource } from 'frappe-ui';

const props = defineProps<{
  orderId: string;
  operator: string;
}>();

const emit = defineEmits(['close','update-status']);

// Fetch Manufacturing Order details using createDocumentResource
const orderdetails = createDocumentResource({
  doctype: 'Manufacturing Order',
  name: props.orderId,
  auto: true,
});

// Reactive object to track added quantities for each item
const addedQuantities = reactive({});

// Initialize added quantities for each item in planned_output
orderdetails.doc.planned_output?.forEach(item => {
  addedQuantities[item.item] = 0;
});

const logOutput = async () => {
  try {
    // Filter items with addedQuantities > 0
    const itemsToUpdate = orderdetails.doc.planned_output.filter(
      item => addedQuantities[item.item] > 0
    );

    // If no items need to be updated, close the popup
    if (itemsToUpdate.length === 0) {
      console.log('No items to update.');
      emit('close');
      return;
    }

    // Iterate over filtered items and send requests
    for (const item of itemsToUpdate) {
      const response = await fetch('/api/method/conversion_mes.api.log_output', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          order_name: props.orderId,
          operator: props.operator,
          item: item.item,
          quantity: addedQuantities[item.item], // Send the added quantity
        }),
      });

      const data = await response.json();

      if (data) {
        console.log('Output logged successfully for item:', item.item, data);
        emit('update-status');
      } else {
        console.error('Failed to log output for item:', item.item, data.message);
      }
    }

    emit('close'); // Close the popup after successful logging
  } catch (error) {
    console.error('Error logging output:', error);
  }
};

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
    .reduce((sum, log) => sum + (log?.scrap_log?.quantity || 0), 0);
};
</script>

<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
    <div class="bg-white p-6 rounded-lg shadow-lg w-auto">
      <h2 class="text-lg font-semibold mb-4">Log Output</h2>

      <div>
        <table class="min-w-full border border-black text-black">
          <thead class="bg-gray-100">
            <tr>
              <th class="px-4 py-2 border">S. No.</th>
              <th class="px-4 py-2 border">Item Code</th>
              <th class="px-4 py-2 border">UOM</th>
              <th class="px-4 py-2 border">Planed Qty</th>
              <th class="px-4 py-2 border">Completed Qty</th>
              <th class="px-4 py-2 border"></th>
              <th class="px-4 py-2 border">Add</th>
              <th class="px-4 py-2 border"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in orderdetails.doc.planned_output" :key="index">
              <td class="px-4 py-2 border text-center">{{ index + 1 }}</td>
              <td class="px-4 py-2 border">{{ item.item }}</td>
              <td class="px-4 py-2 border text-center">{{ item.uom }}</td>
              <td class="px-4 py-2 border text-center">{{ item.quantity }}</td>
              <td class="px-4 py-2 border text-center">{{ getCompletedQty(item.item) }}</td>
              <td class="px-4 py-2 border text-center">
                <button @click="addedQuantities[item.item] -= 1" :disabled="addedQuantities[item.item] <= 0" class="px-6 py-3 bg-red-500 text-white rounded">−</button>
              </td>
              <td class="px-4 py-2 border text-center">
                <input 
                  type="number" 
                  v-model="addedQuantities[item.item]" 
                  min="0" 
                  class="text-center p-2 w-[150px] border rounded"
                />
              </td>
              <td class="px-4 py-2 border text-center">
                
                <button @click="addedQuantities[item.item] += 1" class="px-6 py-3 bg-green-500 text-white rounded ml-2">+</button>
              </td>
            </tr>
          </tbody>
        </table>

        <div class="flex justify-end mt-4">
          <button @click="emit('close')" class="px-4 py-2 bg-white-500 text-black rounded hover:bg-gray-600">Cancel</button>
          <button @click="logOutput" class="ml-2 px-4 py-2 bg-black text-white rounded hover:pointer">
            Log Output
          </button>
        </div>
      </div>
    </div>
  </div>
</template>