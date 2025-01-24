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
        <div class="w-[70%] pt-2 flex flex-col">
            <h1 class="text-xl font-bold">Order Details</h1>
            <!-- Action Buttons -->
            <div class="pt-2 flex flex-row-reverse space-x-4 space-x-reverse">
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
            </div>
            
            <!-- Order Number & Status Section -->
            <div class="pt-4 flex flex-row justify-between">
                <div class="flex flex-col">
                    <label class="text-sm text-gray-800">Order Number</label>
                    <p v-if="orderdetails.doc.name" class="mt-1 text-m font-bold"> {{ orderdetails.doc.name }} </p>
                </div>
                <div class="flex flex-col">
                    <label class="text-sm text-gray-800">Status</label>
                    <p v-if="orderStatus" class="mt-1 text-m font-bold"> {{ orderdetails.doc.status }} </p>
                </div>
            </div>
            
            <!-- Operation Section -->
            <div class="mt-4">
            <label class="mt-1 text-sm text-gray-800">Operation</label>
            <p class="mt-1 text-m font-bold"> {{ orderdetails.doc.operation }} </p>
            </div>
            
            <!-- Instructions Section -->
            <div class="mt-4">
                <label class="text-sm text-gray-800">Instructions</label>
                <p v-for="(line, index) in instructions" :key="index" class="mt-1 text-m font-bold">
                    {{ line }}
                </p>
            </div>

            <!-- Input Material List Section -->
            <div class="mt-4">
                <label class="text-sm text-gray-800">Input Material List</label>
                    <ListView
                        v-if="orderdetails.doc.planned_input"
                        class="mt-4"
                        :columns="[{ label: 'Items', key: 'item', width:1 },]"
                        :rows="orderdetails.doc.planned_input"
                        :options="{ 
                            selectable: false, 
                            resizeColumn: true, 
                            emptyState: { title: 'No Input Material Found' }}"
                    />
            </div>

            <!-- Output Material List Section -->
            
    </div>

    <!-- Column 2: 30% width -->
        <div class="w-[30%] bg-slate-200 p-4">
        <h1 class="text-xl font-bold">Column 2 (30%)</h1>
        <p>This column takes 30% of the screen width.</p>
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