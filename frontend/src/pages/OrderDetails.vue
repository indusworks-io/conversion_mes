<template>
    
    <!-- Top Navigation Section -->
                <div class="flex items-center justify-between mt-1">
                    <h1 class="font-black text-xl text-gray-600"> {{ workstationId }}</h1>
                    <Button
                        :variant="'outline'"
                        :ref_for="true"
                        theme="gray"
                        size="sm"
                        label="Button"
                        :loading="false"
                        :loadingText="null"
                        :disabled="false"
                        :link="null"
                        @click="goToWorkstationDetails"
                    >
                        View Orders
                    </Button>
                </div>
    <!-- Main Section -->
    <div class="flex w-full">
        <!-- Order Details Section -->
        <div class="w-[70%] pt-2 p-2 flex flex-col">
            <h1 class="text-xl font-bold">Order Details</h1>
            <!-- Action Buttons -->
            <div class="p-6">
                <ButtonsDynamic :workstationId="workstationId" @update-status="updateStatus" :currentStatus="currentStatus" :orderId="orderId"/>
            </div>            
            <!-- Order Number & Status Section -->

            <div v-if="orderdetails.doc" class="w-full mx-auto p-6 bg-white text-black shadow-xl rounded-lg">
                <!-- Order Header -->
                <div class="mb-6">
                <h2 class="text-2xl font-bold">Manufacturing Order</h2>
                <div class="mt-4">
                    <p><span class="font-semibold">Order Number:</span> {{ orderdetails.doc.name }}</p>
                    <p><span class="font-semibold">Status:</span> {{ orderdetails.doc.status }}</p>
                </div>
                </div>

                <!-- Input Materials -->
                <div class="mb-6">
                <h3 class="text-xl font-semibold">Input Materials</h3>
                <div class="overflow-x-auto mt-2">
                    {{ orderdetails.doc.planned_input_item }}
                </div>
                </div>

                 <!-- Batch Serial number -->
                 <!-- Batch Serial Number Section -->
                <div class="mb-6">
                <h3 class="text-xl font-semibold">Batch/Serial Number</h3>
                <div class="overflow-x-auto mt-2">
                    <ul>
                    <li v-for="(log, index) in orderdetails?.doc?.batch_serial_logs" :key="index">
                        {{ log.batch_serial_number }}
                    </li>
                    </ul>
                </div>
                </div>


                <!-- Operation Section -->
                <div class="mb-6">
                <h3 class="text-xl font-semibold">Formula</h3>
                <p class="mt-2">{{ orderdetails.doc.formula }}</p>
                </div>

                <!-- Instructions Section -->
                <div class="mb-6">
                <h3 class="text-xl font-semibold">Instructions</h3>
                <p class="mt-2">{{ orderdetails.doc.instructions }}</p>
                </div>

                <!-- Output Materials -->
                <div>
                <h3 class="text-xl font-semibold">Output Materials</h3>
                <div class="overflow-x-auto mt-2">
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
                </div>
                </div>
            </div>


            <!-- Loading and Error States -->
            <div v-if="orderdetails.loading" class="text-center py-4">Loading...</div>
            <div v-if="errorMessage" class="text-red-500 text-center py-4">{{ errorMessage }}</div>
            <!-- Output Material List Section -->
            
    </div>

    <!-- Column 2: 30% width -->
        
        <div class="w-[30%] bg-slate-200 p-12">
            <DowntimeCard  :workstationId="workstationId" />
            
        </div>
    </div>
        
</template>

<script setup>
import { ref , computed, watch} from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { createDocumentResource } from 'frappe-ui'
import { ListView } from 'frappe-ui';

const route = useRoute();
const router = useRouter();
const workstationId = route.params.id;
const orderId = route.params.orderid;
import DowntimeCard from '../components/DowntimeCard.vue'
import ActionButton from '../components/AcitonButton.vue'
import ButtonsDynamic from '../components/ButtonsDynamic.vue';


import ManufacturingOrder from '../components/ManufacturingOrder.vue';


const goToWorkstationDetails = () => {
    router.push({ name: 'WorkstationDetails', params: { id: workstationId } }).catch(err => {
        console.error('Navigation error:', err);
    });
};

const orderdetails = createDocumentResource({
        doctype: 'Manufacturing Order',
        name: orderId,
        auto: true,
})

console.log(orderdetails);

const currentStatus = computed(() => orderdetails.doc?.status || '');
// Function to update the status (for demonstration purposes)
const updateStatus = () => {
  orderdetails.reload();

};
// Reactive variables to store completed and scraped quantities
let itemCompleted = 0;
let itemsScraped = 0;

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

// // Watch for changes in orderdetails.doc and update quantities
// watch(
//   () => orderdetails.doc,
//   (newDoc) => {
//     if (newDoc) {
//       itemCompleted = getCompletedQty();
//       itemsScraped = getScrapedQty();
//     }
//   },
//   { immediate: true } // Trigger the watcher immediately on component mount
// );

</script>