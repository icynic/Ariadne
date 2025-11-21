<template>
    <Tabs :tabs="['apps', 'websites']">
        <template #0>
            <TimeLine v-model="appTime" :updateFunction="getTimeData" formatName></TimeLine>
        </template>
        <template #1>
            <template v-if="!browser">Please choose a browser in the settings</template>
        
            <template v-if="browser">
                <TimeLine v-model="websiteTime"></TimeLine>
            </template>
        </template>
    </Tabs>
</template>

<script setup>
import { ref} from "vue";
import axios from "axios"

const appTime=ref({})
const websiteTime=ref({})

let browser
axios.get("/api/settings/browser").then(response => { browser = response.data; })

function getTimeData() {
    axios.get("/api/time-data").then((response) => {
        appTime.value = response.data[0]
        websiteTime.value = response.data[1]
    })
}


</script>