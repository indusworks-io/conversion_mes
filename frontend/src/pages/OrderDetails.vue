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
        <div class="w-[70%] bg-slate-200 p-2 flex flex-col">
            <!-- Action Buttons -->
            <div class="">
                <ButtonsDynamic :workstationId="workstationId" @update-status="updateStatus" :currentStatus="currentStatus" :orderId="orderId"/>
            </div>            
            <!-- Order Number & Status Section -->

            <div v-if="orderdetails.doc" class="w-full mx-auto p-2 bg-white text-black shadow-xl rounded-lg">
                <!-- Order Header -->
                <div class="mb-6">
                <div class="pr-2 flex flex-row justify-between">
                    <p><span class="text-sm font-semibold text-gray-600">Order Number:</span> {{ orderdetails.doc.name }}</p>
                    <p><span class="text-sm font-semibold text-gray-600">Status:</span> {{ orderdetails.doc.status }}</p>
                </div>
                </div>

                <!-- Input Materials -->
                <div class="mb-6">
                <h3 class="text-sm font-semibold text-gray-600">Input:</h3>
                <div class="overflow-x-auto mt-2">
                    {{ orderdetails.doc.planned_input_item }}
                </div>
                </div>

                 <!-- Batch Serial number -->
                 <!-- Batch Serial Number Section -->
                <div class="mb-6">
                <h3 class="text-sm font-semibold text-gray-600">Batch/Serial Numbers:</h3>
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
                <h3 class="text-sm font-semibold text-gray-600">Formula:</h3>
                <p class="mt-2">{{ orderdetails.doc.formula }}</p>
                </div>

                <!-- Instructions Section -->
                <div class="mb-6">
                <h3 class="text-sm font-semibold text-gray-600">Instructions:</h3>
                <div class="mt-2" v-html="orderdetails.doc.instructions" style="white-space: pre-wrap;"></div>
                <!-- <pre class="mt-2" v-html="orderdetails.doc.instructions"></pre> -->
                <!-- <p class="mt-2">{{ orderdetails.doc.instructions }}</p> -->
                </div>

                <!-- Output Materials -->
                <div>
                <h3 class="text-sm font-semibold text-gray-600">Output:</h3>
                <div class="overflow-x-auto mt-2">
                    <table class="min-w-full border border-black text-black">
                        <thead class="bg-gray-100">
                        <tr>
                            <th class="px-4 py-2 border text-gray-600">#</th>
                            <th class="px-4 py-2 border text-gray-600">Item Code</th>
                            <th class="px-4 py-2 border text-gray-600">UOM</th>
                            <th class="px-4 py-2 border text-gray-600">Planned</th>
                            <th class="px-4 py-2 border text-gray-600">Completed</th>
                            <th class="px-4 py-2 border text-gray-600">Scrapped</th>
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
        
        <div class="w-[30%] bg-slate-200 p-2">
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