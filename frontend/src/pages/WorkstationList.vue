<template>
    <div class="p-3 bg-gray-50 min-h-screen">
        <!-- Header -->
        <h2 class="font-black text-2xl text-gray-600 mb-6">
            Workstation List
        </h2>

        <!-- Workstation List -->
        <div class="bg-white rounded-lg shadow-sm overflow-hidden">
            <ListView
                v-if="workstations.list.data"
                :columns="[
                    { label: '', key: 'actions', width: '10%' }, // Button column
                    { label: 'Workstation Name', key: 'name', width: '45%' },
                    { label: 'Site', key: 'site', width: '45%' },
                ]"
                :rows="workstations.list.data"
                :options="{
                    selectable: false,
                    resizeColumn: true,
                    emptyState: {
                        title: 'No Workstations Found',
                        description: 'Add a new workstation to get started.',
                        icon: 'folder',
                    },
                    rowClass: 'hover:bg-gray-50 transition duration-200',
                    getRowRoute: (row) => ({ name: 'WorkstationDetails', params: { id: row.name } })
                }"
                row-key="name"
            >
                <!-- Custom Row Template -->
                <template #row="{ row }">
                    <!-- Action Button -->
                    <div class="p-3 flex items-center justify-center">
                        <button
                            class="bg-gray-800 text-white px-3 py-1 rounded-lg hover:bg-gray-700 transition duration-200"
                            @click="navigateToWorkstation(row.name)"
                        >
                            View
                        </button>
                    </div>

                    <!-- Workstation Name -->
                    <div class="p-3">
                        <span class="font-semibold text-gray-800">
                            {{ row.name }}
                        </span>
                    </div>

                    <!-- Site -->
                    <div class="p-3">
                        <span class="text-gray-600">
                            {{ row.site }}
                        </span>
                    </div>
                </template>
            </ListView>
        </div>
    </div>
</template>

<script setup>
import { createListResource } from 'frappe-ui';
import { ListView } from 'frappe-ui';
import { useRouter } from 'vue-router';

const router = useRouter();

// Fetch All Workstations
const workstations = createListResource({
    doctype: 'Workstation',
    fields: ['name', 'site'],
    auto: true,
});

// Navigate to Workstation Details
function navigateToWorkstation(workstationName) {
    router.push({ name: 'WorkstationDetails', params: { id: workstationName } });
}
</script>