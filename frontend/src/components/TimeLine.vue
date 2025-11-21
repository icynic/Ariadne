<template>
    <!-- The legends -->
    <v-list rounded class="legend-container">
        <v-list-item v-for="item in timeDataLegend" :title="item.exe" :subtitle="formatTime(item.totalTime)">
            <template #prepend>
                <v-avatar :color="stringToColor(item.exe)" :size="timeToSize(item.totalTime)" class="mr-2"></v-avatar>
            </template>
        </v-list-item>
    </v-list>
    <!-- The timeline -->
    <v-timeline side="end" truncate-line="start" class="timeline">
        <v-timeline-item v-for="item in timeDataSorted" :dot-color="stringToColor(item.exe)"
            :size="timeToSize(item.time[1] - item.time[0])">
            <v-chip>{{ item.exe }}</v-chip>
            <template #opposite>
                <span>{{ formatTime(item.time[1] - item.time[0]) }}</span>
            </template>
        </v-timeline-item>
    </v-timeline>

</template>

<script setup>
import { ref, computed, onUnmounted } from "vue";

const timeData = defineModel()

const props = defineProps({
    updateFunction: {
        type: Function,
        default: () => { }
    },
    formatName:{
        type:Boolean,
        default:false
    }
})

const timeDataSorted = computed(() => {
    return Object.entries(timeData.value)
        .flatMap(([exe, times]) => {
            exe = pathToName(exe)
            return times.map(time => ({ exe, time }))
        })
        .sort((a, b) => a.time[0] - b.time[0])
})

const timeDataLegend = computed(() => {
    return Object.entries(timeData.value)
        .map(([exe, times]) => ({
            exe: pathToName(exe),
            totalTime: getTotalTime(times)
        }))
        .sort((a, b) => b.totalTime - a.totalTime);
})
let updateInterval


function formatTime(time) {
    const hours = Math.floor(time / 3600)
    const minutes = Math.floor((time % 3600) / 60)
    const seconds = Math.floor(time % 60)
    if (hours > 0) {
        return `${hours}h ${minutes}m ${seconds}s`
    }
    if (minutes > 0) {
        return `${minutes}m ${seconds}s`
    }
    return `${seconds}s`
}


function stringToColor(str) {
    if (!str) { return 'white' }
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        hash = str.charCodeAt(i) + ((hash << 5) - hash);
    }
    let color = '#';
    for (let i = 0; i < 3; i++) {
        const value = (hash >> (i * 8)) & 0xFF;
        color += value.toString(16).padStart(2, '0');
    }
    return color;
}

function timeToSize(time) {
    if (time < 60) { return 'x-small'; }
    else if (time < 600) { return 'small'; }
    else if (time < 1800) { return undefined; }
    else if (time < 3600) { return 'large'; }
    else { return 'x-large'; }
}

function getTotalTime(times) {
    let total = 0
    times.forEach(time => total += time[1] - time[0]);
    return total
}

function pathToName(path) {
    let name
    if (props.formatName){
        name= path.split('\\').pop().split('.')[0]    
    }else{
        name= path
    }
    if (name.length>35){
        name=name.slice(0,35)+"..."
    }
    return name
}


props.updateFunction()
updateInterval = setInterval(() => {
    props.updateFunction()
}, 5000);


onUnmounted(() => {
    clearInterval(updateInterval);
});

</script>
<style scoped>
.legend-container {
    position: fixed;
    right: 2%;
    overflow: auto;
    max-height: 80%;
    transform: scale(0.9);
    transform-origin: top right;
    z-index: 1000;
}
.timeline{
    padding-right: 20%;
}
</style>