<script setup lang="ts">
interface DowntimeInfo {
  id: string;
  start: string;
  end: string;
}

defineProps<{
  downtimeInfo: DowntimeInfo;
}>();
</script>

<template>
  <div class="w-full max-w-md bg-white rounded-lg shadow-md">
    <div class="p-6">
      <div class="mb-4 bg-gray-50 border border-gray-200 rounded-md p-3">
        <label class="block mb-2 text-sm font-medium text-gray-700">Downtime ID:</label>
        <input 
          type="text" 
          :value="downtimeInfo.id" 
          readonly 
          class="w-full px-3 py-2 bg-white border border-gray-300 rounded-md text-sm"
        />
      </div>

      <div class="mb-4 bg-gray-50 border border-gray-200 rounded-md p-3">
        <label class="block mb-2 text-sm font-medium text-gray-700">Start:</label>
        <input 
          type="text" 
          :value="downtimeInfo.start" 
          readonly 
          class="w-full px-3 py-2 bg-white border border-gray-300 rounded-md text-sm"
        />
      </div>

      <div class="mb-4 bg-gray-50 border border-gray-200 rounded-md p-3">
        <label class="block mb-2 text-sm font-medium text-gray-700">End:</label>
        <input 
          type="text" 
          :value="downtimeInfo.end" 
          readonly 
          class="w-full px-3 py-2 bg-white border border-gray-300 rounded-md text-sm"
        />
      </div>

      <button class="w-full py-3 bg-[#000000] hover:pointer text-white font-bold rounded-md transition-colors">
        Update Reason
      </button>
    </div>
  </div>
</template>