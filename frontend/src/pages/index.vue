<template>

    <Tabs :tabs="['active', 'available', 'completed']" ref="tabsRef">
        <template #0>
            <CardList v-model="quests.active" :original="quests.entities" :updateFunction="updateQuests"
                :buttons="{ complete: handleComplete, abandon: handleAbandon }" highlightAll></CardList>
        </template>
        <template #1>
            <CardList v-model="quests.available" :original="quests.entities" :updateFunction="updateQuests"
                :buttons="{ accept: handleAccept, edit: handleEdit, drop: handleDrop }" :highlighted="highlighted">
            </CardList>
            <NewButton @click="handleAdd">Add a new quest</NewButton>
        </template>
        <template #2>
            <CardList v-model="quests.completed" :original="quests.entities" showTimes
                :buttons="{ delete: handleDelete }" :updateFunction="updateQuests">
            </CardList>
        </template>
    </Tabs>

    <QuestDialog ref="dialogRef" :updateFunction="updateQuests"></QuestDialog>

</template>

<script setup>
import { ref, computed } from 'vue'
import axios from "axios"

const tabsRef = ref(null)
const dialogRef = ref(null)
const quests = ref({})
// quests.entities: the actual quests
// quests.available, .active, .completed: index lists of quests
let questTemplate = {}

// Get quests form the backend
axios.get("/api/quests").then(response => { quests.value = response.data; })
axios.get("/api/quest-template").then(response => { questTemplate = response.data; })

const highlighted =computed(()=>{
    if (! quests.value.active){return}
    return quests.value.active.filter((i)=>{
        return quests.value.available.includes(i)
    })

})

function updateQuests() {
    axios.post("/api/quests", quests.value)
}

function handleComplete(entityIndex, referenceIndex) {
    tabsRef.value.animateTab('completed')
    if (!quests.value.completed.includes(entityIndex)) {
        quests.value.completed.push(entityIndex)
    }
    quests.value.entities[entityIndex].completeTimes += 1
    quests.value.active.splice(referenceIndex, 1)
    updateQuests()
}

function handleAbandon(entityIndex, referenceIndex) {
    quests.value.active.splice(referenceIndex, 1)
    updateQuests()
}

function handleAccept(entityIndex, referenceIndex) {
    tabsRef.value.animateTab('active')
    quests.value.active.push(entityIndex)
    updateQuests()
}

function handleEdit(entityIndex, referenceIndex) {
    dialogRef.value.show(quests.value.entities[entityIndex])
}

function handleDrop(entityIndex, referenceIndex) {
    quests.value.available.splice(referenceIndex, 1)
    //must check the existence first
    updateQuests()
}

function handleAdd() {
    dialogRef.value.show(Object.assign({}, questTemplate), addQuest)
    purge()
}

function addQuest(quest){
    quests.value.entities.push(quest)
    quests.value.available.push(quests.value.entities.length-1)
}

function handleDelete(entityIndex, referenceIndex) {
    quests.value.completed.splice(referenceIndex, 1)
    updateQuests()
}

// Delete quests in `entities` that are not referenced
function purge() {
    const indices = quests.value.active.concat(quests.value.available, quests.value.completed)

    quests.value.entities.forEach((entity, index) => {
        if (!indices.includes(index)) {
            quests.value.entities.splice(index, 1);
            ["active", "available", "completed"].forEach((list) => {
                quests.value[list].forEach((value, i) => {
                    if (value > index) {
                        quests.value[list][i] -= 1
                    }
                })
            })
        }
    })
    updateQuests()
}

</script>