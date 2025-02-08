<script setup lang="ts">
interface Material {
  serialNo: number;
  itemCode: string;
  uom: string;
  plan: number;
  actual: number;
  batchNumber?: string;
}

interface ManufacturingOrder {
  orderNumber: string;
  instructions: string;
  inputMaterials: Material[];
  outputMaterials: Material[];
}

const props = defineProps<{ order: ManufacturingOrder }>();
</script>

<template>
  <div class="max-w-8xl mx-auto p-6 bg-white text-black shadow-lg rounded-lg">
    <!-- Order Header -->
    <div class="mb-6">
      <h2 class="text-2xl font-bold">Manufacturing Order</h2>
      <div class="mt-4">
        <p><span class="font-semibold">Order Number:</span> {{ order.orderNumber }}</p>
        <p><span class="font-semibold">Instructions:</span> {{ order.instructions }}</p>
      </div>
    </div>

    <!-- Input Materials -->
    <div class="mb-6">
      <h3 class="text-xl font-semibold">Input Materials</h3>
      <div class="overflow-x-auto mt-2">
        <table class="min-w-full border border-black text-black">
          <thead class="bg-gray-100">
            <tr>
              <th class="px-4 py-2 border">S. No.</th>
              <th class="px-4 py-2 border">Item Code</th>
              <th class="px-4 py-2 border">UOM</th>
              <th class="px-4 py-2 border">Plan</th>
              <th class="px-4 py-2 border">Actual</th>
              <th class="px-4 py-2 border">Batch Number</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in order.inputMaterials" :key="item.serialNo">
              <td class="px-4 py-2 border text-center">{{ item.serialNo }}</td>
              <td class="px-4 py-2 border">{{ item.itemCode }}</td>
              <td class="px-4 py-2 border text-center">{{ item.uom }}</td>
              <td class="px-4 py-2 border text-center">{{ item.plan }}</td>
              <td class="px-4 py-2 border text-center">{{ item.actual }}</td>
              <td class="px-4 py-2 border text-center">{{ item.batchNumber || '-' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Output Materials -->
    <div>
      <h3 class="text-xl font-semibold">Output Materials</h3>
      <div class="overflow-x-auto mt-2">
        <table class="min-w-full border border-black text-black">
          <thead class="bg-gray-100">
            <tr>
              <th class="px-4 py-2 border">S. No.</th>
              <th class="px-4 py-2 border">Item Code</th>
              <th class="px-4 py-2 border">UOM</th>
              <th class="px-4 py-2 border">Plan</th>
              <th class="px-4 py-2 border">Actual</th>
              <th class="px-4 py-2 border">Batch Number</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in order.outputMaterials" :key="item.serialNo">
              <td class="px-4 py-2 border text-center">{{ item.serialNo }}</td>
              <td class="px-4 py-2 border">{{ item.itemCode }}</td>
              <td class="px-4 py-2 border text-center">{{ item.uom }}</td>
              <td class="px-4 py-2 border text-center">{{ item.plan }}</td>
              <td class="px-4 py-2 border text-center">{{ item.actual }}</td>
              <td class="px-4 py-2 border text-center">{{ item.batchNumber || '-' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
