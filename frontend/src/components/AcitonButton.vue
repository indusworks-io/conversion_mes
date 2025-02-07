<template>
    <Button
        :variant="'outline'"
        :ref_for="true"
        theme="gray"
        size="sm"
        :loading="false"
        :loadingText="null"
        :disabled="false"
        :link="null"
        @click="handleClick"
    >
        {{ title }}
    </Button>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
    title: {
        type: String,
        required: true
    },
    onClick: {
        type: Function,
        
    }
});

const handleClick = () => {
    props.onClick();
};
</script>
