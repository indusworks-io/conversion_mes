<template>
    <div class="flex items-center justify-between">
        <h2 class="font-black text-2xl text-gray-600">
        {{ workstationId }} Dashboard
        </h2>
        <div class='flex items-center space-x-4'>
        <Button
            v-if="workstationId !== defaultWorkstation"
            :variant="'outline'"
            :ref_for="true"
            theme="gray"
            size="sm"
            label="Button"
            :loading="false"
            :loadingText="null"
            :disabled="false"
            :link="null"
            @click="setDefaultWorkstation(workstationId)"
        >
            Set Default
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
            @click="goToWorkstationList"
        >
            View Workstations
        </Button>
        </div>
    </div>
    <div class="mt-8">
        <h3 class="font-bold text-xl text-gray-600">
        Open Manufacturing Orders
        </h3>
        <ListView
            v-if="ManufacturingOrders.list.data"
            class="h-[500px] mt-4"
            :columns="[
                { label: 'Date', key: 'posting_date', width:1 },
                { label: 'Order Number', key: 'name', width:2 },
                { label: 'Operation', key: 'operation', width:2 },
                { label: 'Status', key: 'status', width:1 },
            ]"
            :rows="ManufacturingOrders.list.data"
            :options="{
                selectable: false,
                resizeColumn: true,
                emptyState: {
                    title: 'No Manufacturing Orders Found',
                },
            }"
            row-key="name"
        />
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { createListResource } from 'frappe-ui'
import { ListView } from 'frappe-ui';

const route = useRoute();
const router = useRouter();
const workstationId = route.params.id;
const defaultWorkstation = ref(localStorage.getItem('defaultWorkstation'));

const setDefaultWorkstation = (workstationId) => {
    localStorage.setItem('defaultWorkstation', workstationId);
    defaultWorkstation.value = workstationId;
    console.log('Default Workstation Set:', workstationId);
};

const goToWorkstationList = () => {
    router.push({ name: 'Workstations' }).catch(err => {
        console.error('Navigation error:', err);
    });
};

let ManufacturingOrders = createListResource({
    doctype: 'Manufacturing Order',
    fields: ['posting_date', 'name', 'operation', 'status'],
    filters: [['workstation', '=', workstationId]],
    auto: true
});


</script>