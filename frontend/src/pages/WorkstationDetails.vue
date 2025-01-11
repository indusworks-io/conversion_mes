<template>
    <div>
        <h2 class="font-black text-2xl text-gray-600">
        Workstation Details For {{ workstationId }}
        </h2>
    </div>
</template>

<script setup>
import { useRoute } from 'vue-router';

const route = useRoute();
const workstationId = route.params.id;

console.log('Workstation ID:', workstationId);
</script>