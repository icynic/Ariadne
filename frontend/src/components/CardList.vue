<template>
    <v-card v-for="(item, index) of items" class="mb-2" link @dragstart="handleDrag(index)" @drop="handleDrop(index)"
        draggable="true" @dragover.prevent @mouseenter="handleMouseEnter(index)" @mouseleave="handleMouseLeave"
        :color="isHighlighted(index)">
        <!-- When an item is an index of props.original. -->
        <template v-if="props.original">
            <v-card-subtitle class="float-right pt-2" v-if="props.showTimes && props.original[item].completeTimes > 1">
                x{{ props.original[item].completeTimes }}
        </v-card-subtitle>
            <v-card-title class="text-capitalize">{{ props.original[item].title }}</v-card-title>

            <v-card-text>{{ props.original[item].text }}</v-card-text>
            

        </template>
        <!-- When an item is itself -->
        <template v-if="!props.original">
            <v-card-title>{{ item.title }}</v-card-title>
            <v-card-text>{{ item.text }}</v-card-text>
        </template>



        <v-expand-transition :color="isHighlighted(index)">
            <v-card v-if="revealedItem == index" elevation="0">
                <v-card-actions v-if="revealedItem == index" class="justify-end">
                    <v-btn v-for="b in Object.keys(props.buttons)" @click.stop="props.buttons[b](item, index)">{{ b
                        }}</v-btn>
                </v-card-actions>
            </v-card>
        </v-expand-transition>
    </v-card>
</template>

<script setup>
import { ref } from 'vue'
// An item should have: title, text, completeTimes
const items = defineModel()
const props = defineProps({
    buttons: {
        // {name:callback}
        type: Object,
        default: {}
    },
    original: {
        type: Array
    },
    showTimes: {
        type: Boolean,
        default: false
    },
    updateFunction: {
        type: Function,
        default: () => { }
    },
    highlighted:{
        type: Array,
        default:[]
    },
    highlightAll:{
        type: Boolean,
        default: false
    },
})

// Dragging
let draggedItemIndex = null

function handleDrag(index) {
    draggedItemIndex = index
}

function handleDrop(droppedItemIndex) {
    const draggedItem = items.value[draggedItemIndex]
    if (draggedItemIndex !== -1 && droppedItemIndex !== -1) {
        items.value.splice(draggedItemIndex, 1);
        items.value.splice(droppedItemIndex, 0, draggedItem);
        props.updateFunction()
    }
}

// Expand on hover
const revealedItem = ref(null)
let revealTimeout
let shirnkTimeout

function handleMouseEnter(index) {
    clearTimeout(shirnkTimeout)
    revealTimeout = setTimeout(() => { revealedItem.value = index }, 150)
}

function handleMouseLeave() {
    shirnkTimeout = setTimeout(() => { revealedItem.value = null }, 200)
    clearTimeout(revealTimeout)
}

function isHighlighted(index){
    if (props.highlightAll || props.highlighted.includes(index)){
        return "secondary"
    }
}
</script>