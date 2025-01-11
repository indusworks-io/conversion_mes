<template>
    <div class="flex items-center justify-between">
        
        <h2 class="font-black text-2xl text-gray-600">
        {{ workstationId }} Dashboard
        </h2>
        <div class='flex items-center space-x-4'>
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
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();
const workstationId = route.params.id;

const goToWorkstationList = () => {
    router.push({ name: 'Workstations' }).catch(err => {
        console.error('Navigation error:', err);
    });
};

const setDefaultWorkstation = (workstationId) => {
      localStorage.setItem('defaultWorkstation', workstationId);
        console.log('Default Workstation Set:', workstationId);
    };

</script>