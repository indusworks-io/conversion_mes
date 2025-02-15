<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { createListResource } from 'frappe-ui'; // Assuming you're using Frappe UI

interface Reason {
  text: string;
}

const props = defineProps<{ downtimeId: string; show: boolean }>();
const emit = defineEmits(['close', 'updated']);

const selectedReason = ref<string>('');
const loading = ref(false);
const errorMessage = ref<string | null>(null);

// Fetch downtime reasons using createListResource
const downtimeReasons = createListResource({
  doctype: 'Downtime Reason', // Replace with the correct doctype
  fields: ['name'], // Fetch the fields you need
  filters: [['show_to_operator', '=', true]],
  auto: true, // Automatically fetch data when the component is mounted
  transform(data: any[]) {
    // Transform the data into the desired format
    return data.map((item) => ({ text: item.name }));
  },
  onError(error: any) {
    console.error('Error fetching reasons:', error);
    errorMessage.value = 'Failed to fetch reasons';
  },
});

// Update downtime reason
const updateReason = async () => {
  if (!selectedReason.value) return;

  loading.value = true;
  errorMessage.value = null;

  try {
    const response = await fetch('/api/method/conversion_mes.api.update_downtime_reason', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        downtime_name: props.downtimeId, // Pass the downtime ID
        downtime_reason: selectedReason.value, // Pass the selected reason
      }),
    });

    const data = await response.json();

    if (data.message.status) {
      // Emit events to notify the parent component
      emit('updated', selectedReason.value);
      emit('close');
    } else {
      // Handle error
      errorMessage.value = data.message.message || 'Update failed';
    }
  } catch (error) {
    console.error('Error updating reason:', error);
    errorMessage.value = 'Server error';
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div v-if="show" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
    <div class="bg-white border border-black p-6 rounded-lg shadow-lg w-96">
      <h2 class="text-lg font-bold mb-4">Update Downtime Reason</h2>

      <div v-if="errorMessage" class="text-red-500 text-sm mb-3">{{ errorMessage }}</div>

      <label class="block mb-2 text-sm font-medium text-black">Select a Reason:</label>
      <select 
        v-model="selectedReason" 
        class="w-full border border-black rounded-md px-3 py-2 text-black bg-white"
      >
        <option value="" disabled>Select a reason</option>
        <option 
          v-for="reason in downtimeReasons.data" 
          :key="reason.text" 
          :value="reason.text" 
          class="text-black"
        >
          {{ reason.text }}
        </option>
      </select>

      <div class="mt-4 flex justify-between">
        <button 
          @click="emit('close')" 
          class="px-4 py-2 border border-black text-black rounded-md bg-white hover:bg-gray-100"
        >
          Cancel
        </button>
        <button 
          @click="updateReason" 
          :disabled="loading"
          class="px-4 py-2 bg-black text-white rounded-md hover:bg-gray-800 disabled:opacity-50"
        >
          {{ loading ? 'Updating...' : 'Update' }}
        </button>
      </div>
    </div>
  </div>
</template>