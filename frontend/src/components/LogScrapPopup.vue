<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { createDocumentResource } from 'frappe-ui';

const props = defineProps<{
  orderId: string;
  operator: string;
}>();

const emit = defineEmits(['close', 'update-status']);

// Fetch Manufacturing Order details using createDocumentResource
const orderdetails = createDocumentResource({
  doctype: 'Manufacturing Order',
  name: props.orderId,
  auto: true,
});

// Reactive object to track added scrap quantities for each item
const addedScrapQuantities = reactive({});

// Initialize added scrap quantities for each item in planned_output
orderdetails.doc.planned_output?.forEach(item => {
  addedScrapQuantities[item.item] = 0;
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

// Log Scrap Function
const logScrap = async () => {
  try {
    // Filter items with addedQuantities > 0
    const itemsToUpdate = orderdetails.doc.planned_output.filter(
      item => addedScrapQuantities[item.item] > 0
    );

    // If no items need to be updated, close the popup
    if (itemsToUpdate.length === 0) {
      console.log('No items to update.');
      emit('close');
      return;
    }

    // Iterate over filtered items and send requests
    for (const item of itemsToUpdate) {
      const response = await fetch('/api/method/conversion_mes.api.log_scrap', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          order_name: props.orderId,
          operator: props.operator,
          item: item.item,
          quantity: addedScrapQuantities[item.item], // Send the added scrap quantity
        }),
      });

      const data = await response.json();

      if (data) {
        console.log('Scrap logged successfully for item:', item.item, data);
        emit('update-status'); // Emit event to update status
      } else {
        console.error('Failed to log scrap for item:', item.item, data.message);
      }
    }

    emit('close'); // Close the popup after successful logging
  } catch (error) {
    console.error('Error logging scrap:', error);
  }
};
</script>

<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
    <div class="bg-white p-6 rounded-lg shadow-lg w-auto max-h-[80vh] overflow-y-auto">
      <h2 class="text-lg font-semibold mb-4">Log Scrap</h2>

      <div>
        <table class="min-w-full border border-black text-black">
          <thead class="bg-gray-100">
            <tr>
              <th class="px-4 py-2 border">S. No.</th>
              <th class="px-4 py-2 border">Item Code</th>
              <th class="px-4 py-2 border">UOM</th>
              <th class="px-4 py-2 border">Planned Qty</th>
              <th class="px-4 py-2 border">Scraped Qty</th>
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
              <td class="px-4 py-2 border text-center">{{ getScrapedQty(item.item) }}</td>
              <td class="px-4 py-2 border text-center">
                <button 
                  @click="addedScrapQuantities[item.item] -= 1" 
                  :disabled="addedScrapQuantities[item.item] <= 0" 
                  class="px-6 py-3 bg-red-500 text-white rounded"
                >
                  −
                </button>
              </td>
              <td class="px-4 py-2 border text-center">
                <input 
                  type="number" 
                  v-model="addedScrapQuantities[item.item]" 
                  min="0" 
                  class="text-center p-2 w-[150px] border rounded"
                />
              </td>
              <td class="px-4 py-2 border text-center">
                
                <button 
                  @click="addedScrapQuantities[item.item] += 1" 
                  class="px-6 py-3 bg-green-500 text-white rounded ml-2"
                >
                  +
                </button>
              </td>
            </tr>
          </tbody>
        </table>

        <div class="flex justify-end mt-4">
          <button @click="emit('close')" class="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600">
            Cancel
          </button>
          <button @click="logScrap" class="ml-2 px-4 py-2 bg-black text-white rounded hover:pointer">
            Log Scrap
          </button>
        </div>
      </div>
    </div>
  </div>
</template>