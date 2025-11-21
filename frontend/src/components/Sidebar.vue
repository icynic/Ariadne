<template>
    <v-navigation-drawer app permanent :rail="railDrawer" color="transparent" width="180">
        <v-list>
            <v-list-item v-for="(item, index) in navItems" :prepend-icon="item.icon" :key="index" :to="item.route"
                router exact>
                <v-list-item-title>{{ item.title }}</v-list-item-title>
            </v-list-item>
        </v-list>
        <template v-slot:append>
            <v-btn rounded="0" @click="railDrawer = !railDrawer" variant="plain" class="mb-2 pl-1" :ripple="false">
                <v-icon>{{ railDrawer ? 'mdi-arrow-expand-right' : 'mdi-arrow-collapse-left' }} </v-icon>
            </v-btn>
        </template>
    </v-navigation-drawer>
</template>

<script setup>
import { ref } from 'vue'
const railDrawer = ref(true)
const navItems = ref([
    { title: 'Quests', icon: 'mdi-bulletin-board', route: '/' },
    // { title: 'Note', icon: 'mdi-note-outline', route: '/note' },
    { title: 'Timeline', icon: 'mdi-timeline-clock-outline', route: '/timeline' },
    { title: 'Settings', icon: 'mdi-cog', route: '/settings' },
])
</script>