<template>
  <v-app>

    <Sidebar></Sidebar>
    <Topbar></Topbar>

    <v-main>
      <v-container class="pt-0">
        <router-view />
      </v-container>
    </v-main>

  </v-app>
</template>

<script setup>
// import { useRouter } from 'vue-router';
// const router = useRouter();
// router.push('/')
</script>
