<script setup lang="ts">
import { onMounted, onUnmounted, ref, watchEffect } from 'vue';
import { createListResource } from 'frappe-ui';
import UpdateReasonModal from './UpdateReasonModal.vue';

const showModal = ref(false);
const selectedDowntimeId = ref<string | null>(null);

// Define props
const props = defineProps<{
   workstationId: string;
}>();

const openModal = (id: string) => {
  selectedDowntimeId.value = id;
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

interface DowntimeInfo {
  id: string;
  start: string;
  end: string;
  reason?: string;
}

// Fetch downtime logs from Frappe
const DowntimeLogs = createListResource({
  doctype: 'Downtime Log', // Ensure the doctype is correct
  fields: ['name', 'start_date_time', 'end_date_time', 'reason'],
  filters: [
    ['reason', '=', ''],
    ['workstation', '=', props.workstationId], // Filter for logs where reason is empty
  ],
  auto: true, // Automatically fetch data
});

const downtimeLogs = ref<DowntimeInfo[]>([]);

// Function to reload downtime logs
const reloadDowntimeLogs = () => {
  DowntimeLogs.reload();
};

// Set up periodic fetching

onMounted(() => {
  // Fetch immediately when the component is mounted
  reloadDowntimeLogs();

  // Set up an interval to fetch every 2 minutes (120,000 milliseconds)
  setInterval(() => {
    DowntimeLogs.reload();
    console.log('Reloading downtime logs...');
  }, 120000); // 2 minutes
});

onUnmounted(() => {
  
});

watchEffect(() => {
  if (DowntimeLogs.data) {
    downtimeLogs.value = DowntimeLogs.data.map((log) => ({
      id: log.name,
      start: log.start_date_time,
      end: log.end_date_time,
      reason: log.reason,
    }));
  }
});
</script>

<template>
  <div v-if="downtimeLogs.length === 0" class="text-center text-gray-500 py-6">
    No Downtime Logs
  </div>
  
  <div v-for="downtime in downtimeLogs" :key="downtime.id" class="p-2">
    <div class="w-full max-w-md bg-white rounded-lg shadow-md">
      <div class="p-2">
        <!-- Downtime ID -->
        <div class="mb-2 bg-gray-50 border border-gray-200 rounded-md p-3">
          <label class="block mb-2 text-sm font-medium text-gray-700">Downtime ID:</label>
          <input
            type="text"
            :value="downtime.id"
            readonly
            class="w-full px-3 py-2 bg-white border border-gray-300 rounded-md text-sm"
          />
        </div>

        <!-- Start Time -->
        <div class="mb-2 bg-gray-50 border border-gray-200 rounded-md p-3">
          <label class="block mb-2 text-sm font-medium text-gray-700">Start:</label>
          <input
            type="text"
            :value="downtime.start"
            readonly
            class="w-full px-3 py-2 bg-white border border-gray-300 rounded-md text-sm"
          />
        </div>

        <!-- End Time -->
        <div class="mb-2 bg-gray-50 border border-gray-200 rounded-md p-3">
          <label class="block mb-2 text-sm font-medium text-gray-700">End:</label>
          <input
            type="text"
            :value="downtime.end"
            readonly
            class="w-full px-3 py-2 bg-white border border-gray-300 rounded-md text-sm"
          />
        </div>

        <!-- Reason -->
        <!-- <div class="mb-2 bg-gray-50 border border-gray-200 rounded-md p-3">
          <label class="block mb-2 text-sm font-medium text-gray-700">Reason:</label>
          <input
            type="text"
            :value="downtime.reason"
            readonly
            class="w-full px-3 py-2 bg-white border border-gray-300 rounded-md text-sm"
          />
        </div> -->

        <!-- Update Reason Button -->
        <button
          @click="openModal(downtime.id)"
          class="w-full py-3 bg-black hover:bg-gray-800 text-white font-bold rounded-md transition-colors"
        >
          Update Reason
        </button>

        <!-- Update Reason Modal -->
        <UpdateReasonModal
          :show="showModal"
          :downtimeId="selectedDowntimeId ?? ''"
          @close="closeModal"
          @updated="() => DowntimeLogs.reload()"
        />
      </div>
    </div>
  </div>
</template>