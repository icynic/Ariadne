<template>
<v-app-bar height="" floating flat style="width: 50%; right: 0px; left:auto" 
color="transparent" density="compact" >
<template #append>
    <v-btn rounded="0" class="pywebview-drag-region cursor-move" variant="plain" :ripple="false"><v-icon>mdi-cursor-move</v-icon></v-btn>
    <v-btn rounded="0" @click="close"><v-icon>mdi-window-close</v-icon></v-btn>
    <v-btn rounded="0" @click="hide" ><v-icon>mdi-window-minimize</v-icon></v-btn>
</template>
</v-app-bar>
</template>
<script setup>

function hide(){
    pywebview.api.hide()
}
function close(){
    pywebview.api.close()
}


</script>