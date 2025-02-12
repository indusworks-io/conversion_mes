<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { createResource } from 'frappe-ui'; // Import createResource from frappe-ui

const props = defineProps<{
  workstationID: string; // Define workstationID as a prop
}>();

const emit = defineEmits(['close', 'start-order']);

const operators = ref<string[]>([]);
const selectedOperator = ref<string | null>(null);
const loading = ref(false);
const workstation = props.workstationID;

// Use createResource to fetch operators
const operatorsResource = createResource({
  method: 'GET',
  url: 'conversion_mes.api.get_operators',
  params: {
    workstation, // Pass workstationID as a parameter
  },
  onSuccess: (response) => {
    console.log('API Response:', response); // Debugging: Log the response
    if (response && Array.isArray(response)) {
      operators.value = response; // Set the operators list
    } else {
      console.error('Unexpected API response format:', response);
    }
  },
  onError: (error) => {
    console.error('Error fetching operators:', error);
  },
  auto: true,
});

console.log(operatorsResource);

// Fetch operators when the component is mounted
onMounted(() => {
  operatorsResource.fetch();
});

// Start order with the selected operator
const startOrder = () => {
  if (selectedOperator.value) {
    emit('start-order', selectedOperator.value);
    emit('close');
  }
};
</script>

<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
    <div class="bg-white p-6 rounded-lg shadow-lg w-96">
      <h2 class="text-lg font-semibold mb-4">Select Operator</h2>
      <div v-if="operatorsResource.loading" class="text-center">Loading...</div>
      <div v-else>
        <select v-model="selectedOperator" class="w-full p-2 border border-gray-300 rounded mb-4">
          <option v-for="operator in operators" :key="operator" :value="operator">{{ operator }}</option>
        </select>
        <div class="flex justify-end">
          <button @click="emit('close')" class="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600">Cancel</button>
          <button @click="startOrder" class="ml-2 px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600">Start Order</button>
        </div>
      </div>
    </div>
  </div>
</template>