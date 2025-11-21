<template>
  <Tabs :tabs="['settings']">
    <template #0>

      <v-select v-model="browser" label="Browser" :items="['Chrome', 'Edge', 'Firefox']"
        @update:modelValue="handleBrowserSelect"></v-select>

      <v-switch label="Start with system" v-model="isStartup" @change="handleStartupSwitch" color="primary"></v-switch>

      Data Postion
      <v-file-input disabled :label="dataPath"></v-file-input>

    </template>
  </Tabs>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios"

const isStartup = ref(false)
const dataPath = ref("")
const browser = ref("")

axios.get("api/settings/startup").then(response => { isStartup.value = response.data })
axios.get("api/settings/data-path").then(response => { dataPath.value = response.data })
axios.get("api/settings/browser").then(response => { browser.value = response.data })

function handleStartupSwitch() {
  axios.post("api/settings/startup", { isStartup: isStartup.value })
}

function handleBrowserSelect() {
  axios.post("api/settings/browser", { browser: browser.value })
}

</script>