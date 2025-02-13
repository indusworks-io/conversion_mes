<template>
    <div class="flex items-center justify-between w-[100%]">
        <h2 class="font-black text-xl text-gray-600">
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
    <div class="flex w-full">
        <div class="mt-8 w-[70%] ">
            <h3 class="font-bold text-xl text-gray-600">
            Open Manufacturing Orders
            </h3>
            <div class="pt-6">
                <OrderCard
                    v-for="order in ManufacturingOrders.list.data"
                    :key="order.name"
                    :date="order.posting_date"
                    :orderNo="order.name"
                    :status="order.status"
                />
            </div>
        </div>
        <div class="w-[30%] bg-slate-200 p-12">
            <DowntimeCard />
        </div>
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

import OrderCard from '../components/OrderCard.vue'

import DowntimeCard from '../components/DowntimeCard.vue'


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
    fields: ['posting_date', 'name', 'status'],
    filters: [
        ['workstation', '=', workstationId],
        ['status', 'not in', ['Draft', 'Cancelled', 'Closed', 'Completed']]
    ],
    auto: true
});


</script>
