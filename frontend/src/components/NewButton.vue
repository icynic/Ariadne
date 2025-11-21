<template>
    <v-btn class="mt-5" fixed block color="primary" variant="tonal" @click="$emit('click', $event)">
        <slot></slot>
    </v-btn>
</template>

<script setup>
const emit = defineEmits(['click'])
</script>