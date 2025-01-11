<template>
    <div>
        <h2 class="font-black text-2xl text-gray-600">
        Workstation List
        </h2>
    
        <!-- Create List Of Workstations -->
        <div class="mt-4">
        <ListView
            class="h-[500px]"
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
                onRowClick: (row) => handleRowClick(row)
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

const router = useRouter();
function handleRowClick(row) {
    router.push({ name: 'WorkstationDetails', params: { id: row.name } });
    // console.log('Row Clicked', row.name);
    }

</script>