<template>
  <div class="p-2 h-full overflow-hidden">
    <router-view />
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const redirectToDefaultWorkstation = () => {
  const defaultWorkstation = localStorage.getItem('defaultWorkstation');
  if (defaultWorkstation) {
    router.replace({ name: 'WorkstationDetails', params: { id: defaultWorkstation } });
  }
};

// Redirect on app load
redirectToDefaultWorkstation();
</script>