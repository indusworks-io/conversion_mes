<template>
  <div class="bg-gray-100 p-8">
    <div class="max-w-4xl mx-auto">
      <div class="grid grid-cols-4 gap-8">
        <!-- Left side - State Display -->
        <div class="col-span-1 bg-white p-6 rounded-lg shadow-md">
          <h2 class="text-lg font-semibold mb-4">Current State</h2>
          <div :class="{
            'text-sm font-medium': true,
            'text-orange-500': currentState === 'Not Started',
            'text-blue-500': currentState === 'In Progress',
            'text-green-500': currentState === 'Complete'
          }">
            {{ currentState }}
          </div>
        </div>

        <!-- Right side - Buttons -->
        <div class="col-span-3 space-y-4">
          <template v-if="!isStarted">
            <button
              @click="handleStart"
              class="flex items-center gap-2 bg-green-500 text-white px-6 py-3 rounded-md hover:bg-green-600 transition-colors"
            >
              <Play class="w-5 h-5" />
              START
            </button>
          </template>
          <template v-else>
            <div class="space-y-4">
              <div class="flex gap-4">
                <button
                  @click="handleStepComplete('BATCH/SERIAL')"
                  :class="{
                    'flex items-center gap-2 px-6 py-3 rounded-md transition-colors': true,
                    'bg-blue-500 text-white hover:bg-blue-600': true
                  }"
                >
                  <FileSpreadsheet class="w-5 h-5" />
                  BATCH/SERIAL
                </button>

                <button
                  @click="handleStepComplete('LOG OUTPUT')"
                  :class="{
                    'flex items-center gap-2 px-6 py-3 rounded-md transition-colors': true,
                    'bg-blue-500 text-white hover:bg-blue-600': true
                  }"
                >
                  <FileOutput class="w-5 h-5" />
                  LOG OUTPUT
                </button>

                <button
                  @click="handleStepComplete('LOG SCRAP')"
                  :class="{
                    'flex items-center gap-2 px-6 py-3 rounded-md transition-colors': true,
                    'bg-blue-500 text-white hover:bg-blue-600': true
                  }"
                >
                  <FileWarning class="w-5 h-5" />
                  LOG SCRAP
                </button>
              </div>

              <div class="flex gap-4">
                <button
                  @click="handleComplete"
                  :disabled="completedSteps.length < 3"
                  :class="{
                    'flex items-center gap-2 px-6 py-3 rounded-md transition-colors': true,
                    'bg-gray-300 cursor-not-allowed': completedSteps.length < 3,
                    'bg-green-500 text-white hover:bg-green-600': completedSteps.length === 3
                  }"
                >
                  <CheckCircle class="w-5 h-5" />
                  COMPLETE
                </button>

                <button
                  @click="handleStopResume"
                  :class="{
                    'flex items-center gap-2 px-6 py-3 rounded-md transition-colors': true,
                    'bg-red-500 text-white hover:bg-red-600': !isPaused,
                    'bg-blue-500 text-white hover:bg-blue-600': isPaused
                  }"
                >
                  <StopCircle v-if="!isPaused" class="w-5 h-5" />
                  <Play v-else class="w-5 h-5" />
                  {{ isPaused ? 'RESUME' : 'STOP' }}
                </button>
              </div>
            </div>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { Play, FileSpreadsheet, FileOutput, FileWarning, CheckCircle, StopCircle } from 'lucide-vue-next';

const isStarted = ref(false);
const isPaused = ref(false);
const currentState = ref('Not Started');
const completedSteps = ref<string[]>([]);

const handleStart = () => {
  isStarted.value = true;
  currentState.value = 'In Progress';
};

const handleStepComplete = (step: string) => {
  if (!completedSteps.value.includes(step)) {
    completedSteps.value.push(step);
  }

  if (completedSteps.value.length === 3) {
    currentState.value = 'Complete';
  }
};

const handleComplete = () => {
  if (completedSteps.value.length === 3) {
    currentState.value = 'Complete';
  }
};

const handleStopResume = () => {
  isPaused.value = !isPaused.value;
  if (isPaused.value) {
    currentState.value = 'Paused';
  } else {
    currentState.value = 'In Progress';
  }
};
</script>