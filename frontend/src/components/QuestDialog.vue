<template>
  <v-dialog v-model="showDialog" width="auto" min-width="70vw">
    <v-card>
      <v-card-title>Quest</v-card-title>
      <v-card-text>
        <v-text-field label="Title" v-model="newQuest.title"></v-text-field>
        <v-textarea label="Content" v-model="newQuest.text" rows="1" auto-grow></v-textarea>
      </v-card-text>

      <v-card-actions class="pr-5 pb-3">
        <v-btn text="Close" variant="plain" @click="showDialog = false"></v-btn>
        <v-btn text="Save" variant="tonal" color="primary" @click="handleSave"></v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script setup>
import { ref } from 'vue'

const showDialog = ref(false)
const newQuest = ref({ title: undefined, text: undefined })
let originalQuest
let addFunction

const props = defineProps({
  updateFunction: {
    type: Function,
    default: () => { }
  },
})

function handleSave() {
  Object.assign(originalQuest, newQuest.value)
  if (addFunction) { addFunction(originalQuest) }
  props.updateFunction()
  showDialog.value = false
}

defineExpose({
  show: (q, add) => {
    Object.assign(newQuest.value, q)
    originalQuest = q
    if (add) { addFunction = add }
    else { addFunction = undefined }
    showDialog.value = true
  },
})
</script>