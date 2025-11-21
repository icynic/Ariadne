<template>
    <!-- How to use this?
     1. pass in an array of strings call tabs as props
     2. use named slots to inject contents, which are named after the strings
     3. call .animateTab(tabName) to animate a tab -->

    <v-tabs v-model="displayedTab" class="mb-5">
        <v-tab v-for="(name, index) in props.tabs" :value="index" @animationend="animatedTab = null"
            :class="{ animated: name === animatedTab }">
            {{ name }}
        </v-tab>
        <slot name="append"></slot>
    </v-tabs>

    <v-tabs-window v-model="displayedTab">
        <v-tabs-window-item v-for="(name, index) in props.tabs" :value="index">
            <slot :name="index"></slot>
        </v-tabs-window-item>
    </v-tabs-window>
</template>


<script setup>
import { ref, watch } from "vue";
const props = defineProps({
    tabs: {
        type: Array,
        default: () => []
    }
})

const displayedTab = ref(0)

watch(() => props.tabs, (newTabs) => {
    if (newTabs.length > 0) {
        displayedTab.value = newTabs.length - 1
    }
})

const animatedTab = ref(null)
defineExpose({
    animateTab: (tabName) => {
        animatedTab.value = tabName
    }
})
</script>


<style>
.animated {
    animation: slide-in 0.5s forwards
}

@keyframes slide-in {
    50% {
        transform: scale(1.3);
    }
}
</style>