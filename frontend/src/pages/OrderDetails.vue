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

            <!-- <div class="pt-2 flex flex-row-reverse space-x-4 space-x-reverse">
            <div class="pt-2 flex flex-row-reverse space-x-4 space-x-reverse">
            <!-- <div>
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
                    >
                        Start Order
                    </Button>
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
                    >
                        Stop Order
                    </Button>
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
                    >
                        Complete Order
                    </Button>
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
                    >
                        Log Scrap
                    </Button>
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
                    >
                        Log Output
                    </Button>
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
                    >
                        Batch/Serial
                    </Button>
            </div> -->
                   
                    <ActionButton title=" Batch/Serial"/>
                    <ActionButton title=" Log Output"/>
                    <ActionButton title=" Log Scrap"/>
                    <ActionButton title=" Complete Order"/>
                    <ActionButton title=" Stop Order"/>
                    <ActionButton title=" Start Order"/>

            </div> -->
            <div class="p-6">
                <ButtonsDynamic :orderId="orderId"/>
            </div>
            <div>
                <ButtonsDynamic/>

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

                <!-- Operation Section -->
                <div class="mb-6">
                <h3 class="text-xl font-semibold">Operation</h3>
                <p class="mt-2">{{ orderdetails.doc.operation }}</p>
                </div>

                <!-- Instructions Section -->
                <div class="mb-6">
                <h3 class="text-xl font-semibold">Instructions</h3>
                <p class="mt-2">{{ orderdetails.doc.instructions }}</p>
                </div>

                <!-- Input Materials -->
                <div class="mb-6">
                <h3 class="text-xl font-semibold">Input Materials</h3>
                <div class="overflow-x-auto mt-2">
                    <table class="min-w-full border border-black text-black">
                    <thead class="bg-gray-100">
                        <tr>
                        <th class="px-4 py-2 border">S. No.</th>
                        <th class="px-4 py-2 border">Item Code</th>
                        <th class="px-4 py-2 border">UOM</th>
                        <th class="px-4 py-2 border">Planed Qty</th>
                        <th class="px-4 py-2 border">Conversion Factor</th>
                        <th class="px-4 py-2 border">Alternate UMO</th>
                        <th class="px-4 py-2 border">Alternate Quantity</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(item, index) in orderdetails.doc.planned_input" :key="index">
                        <td class="px-4 py-2 border text-center">{{ index + 1 }}</td>
                        <td class="px-4 py-2 border">{{ item.item }}</td>
                        <td class="px-4 py-2 border text-center">{{ item.uom }}</td>
                        <td class="px-4 py-2 border text-center">{{ item.quantity }}</td>
                        <td class="px-4 py-2 border text-center">{{ item.conversion_factor }}</td>
                        <td class="px-4 py-2 border text-center">{{ item.alternate_uom }}</td>
                        <td class="px-4 py-2 border text-center">{{ item.alternate_quantity }}</td>
                        </tr>
                    </tbody>
                    </table>
                </div>
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
                        <th class="px-4 py-2 border">Conversion Factor</th>
                        <th class="px-4 py-2 border">Alternate UMO</th>
                        <th class="px-4 py-2 border">Alternate Quantity</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(item, index) in orderdetails.doc.planned_output" :key="index">
                        <td class="px-4 py-2 border text-center">{{ index + 1 }}</td>
                        <td class="px-4 py-2 border">{{ item.item }}</td>
                        <td class="px-4 py-2 border text-center">{{ item.uom }}</td>
                        <td class="px-4 py-2 border text-center">{{ item.quantity }}</td>
                        <td class="px-4 py-2 border text-center">{{ item.conversion_factor }}</td>
                        <td class="px-4 py-2 border text-center">{{ item.alternate_uom }}</td>
                        <td class="px-4 py-2 border text-center">{{ item.alternate_quantity }}</td>
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
            <div class="">
                <ManufacturingOrder :order="orderData"/>
            </div>
    </div>

    <!-- Column 2: 30% width -->
        
        <div class="w-[30%] bg-slate-200 p-12">
            <DowntimeCard />
            <DowntimeCard :downtime-info="downtimeInfo" />
        </div>
    </div>
        
</template>

<script setup>
import { ref } from 'vue';
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

const orderData = {
  orderNumber: 'MO-241221-178',
  instructions: 'Backprint',
  inputMaterials: [
    {
      serialNo: 1,
      itemCode: 'E10038 S-RACE@ Dynamic, Matt, 38g/m2 124cm x 20000mtr',
      uom: 'Reel',
      plan: 1,
      actual: 0
    }
  ],
  outputMaterials: [
    {
      serialNo: 1,
      itemCode: 'E10038 S-RACE@ Dynamic, Matt, 38g/m2 122cm x 600mtr x 3"',
      uom: 'Roll',
      plan: 30,
      actual: 0
    }
  ]
};
const downtimeInfo = {
  id: 'DT-241220-02',
  start: '20 December, 3:00 PM',
  end: '20 December, 3:30 PM'
}

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

console.log('Order Details:', orderdetails);

// const rawinstructions = orderdetails.doc.instructions;
// const instructions = ref(rawinstructions.split('\n'));

</script>