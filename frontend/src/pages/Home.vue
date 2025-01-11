<template>
  <div class="pl-4 min-w-full py-4 mx-auto">
    <h2 class="font-bold text-lg text-gray-600 mb-4">
      Welcome {{ session.user }}!
    </h2>

    <Button theme="gray" variant="solid" icon-left="code" @click="ping.fetch" :loading="ping.loading">
      Click to send 'ping' request
    </Button>
    <div>
      {{ ping.data }}
    </div>
    <pre>{{ ping }}</pre>

    <div class="flex flex-row space-x-2 mt-4">
      <Button @click="showDialog = true">Open Dialog</Button>
      <Button @click="session.logout.submit()">Logout</Button>
    </div>

    <!-- Create List Of Workstations -->
    <div class="mt-8">
      <h3 class="font-bold text-lg text-gray-600 mb-4">Workstations</h3>
      <div v-if="workstations.loading">Loading...</div>
      <div v-else>
        <div v-for="workstation in workstations.data" :key="workstation.name">
          <div>{{ workstation.name }}</div>
          <div>{{ workstation.site }}</div>
        </div>
    </div>
    <!-- Dialog -->
    <Dialog title="Title" v-model="showDialog"> Dialog content </Dialog>
  </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Dialog } from 'frappe-ui'
import { createResource } from 'frappe-ui'
import { createListResource } from 'frappe-ui'
import { session } from '../data/session'

const ping = createResource({
  url: 'ping',
  auto: true,
})

let workstations = createListResource({
  doctype: 'Workstation',
  fields: ['name', 'site'],
})

workstations.fetch()

const showDialog = ref(false)
</script>
