<template>
    <div>
        <h2 class="font-black text-xl text-gray-600">
        Workstation List
        </h2>
    
        <!-- Create List Of Workstations -->
        <div class="mt-4">
        <ListView
            v-if="workstations.list.data"
            :columns="[
                { label: 'Workstation Name', key: 'name' },
                { label: 'Site', key: 'site'},
            ]"
            :rows="workstations.list.data"
            :options="{
                selectable: false,
                resizeColumn: true,
                emptyState: {
                    title: 'No Workstations Found',
                },
                getRowRoute: (row) => ({ name: 'WorkstationDetails', params: { id: row.name } })
            }"
            row-key="name"
        />
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { createListResource } from 'frappe-ui'
import { ListView } from 'frappe-ui';
import { useRouter } from 'vue-router';

// Fetch All Workstations
let workstations = createListResource({
  doctype: 'Workstation',
  fields: ['name', 'site'],
  auto: true
})
</script>