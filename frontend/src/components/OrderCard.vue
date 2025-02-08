<script setup lang="ts">
import { useRouter } from 'vue-router';

defineProps<{
  date: string;
  orderNo: string;
  status: string;
}>();


const router = useRouter();

const navigateToOrder = (orderNo: string) => {
  router.push({ name: 'OrderDetails', params: { orderid: orderNo } });
};

</script>

<template>
  <div class="bg-gray-100 p-4 rounded-md mb-4">
    <div class="grid grid-cols-5 gap-4 items-center">
      <div>
        <div class="text-sm text-gray-600">Date:</div>
        <div class="bg-white p-2 rounded border border-gray-300">{{ date }}</div>
      </div>
      
      <div class="col-span-2">
        <div class="text-sm text-gray-600">Order No.:</div>
        <div class="bg-white p-2 rounded border border-gray-300">{{ orderNo }}</div>
      </div>
      
      <div class="">
        <div class="text-sm text-gray-600">Status:</div>
        <div class="bg-white p-2 rounded border border-gray-300">{{ status }}</div>
      </div>
      <div>
        <button
          class="w-full h-full bg-[#000000] text-white py-3 px-2 rounded hover:pointer transition-colors"
          @click="navigateToOrder(orderNo)"
        >
          View Order
        </button>
      </div>
    </div>
  </div>
</template>