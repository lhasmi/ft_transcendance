<script setup>
import { RouterView } from 'vue-router'
import HeaderComp from './components/HeaderComp.vue'
</script>

<template>
  <main class="d-flex flex-column">
    <HeaderComp v-if="['login', 'register'].includes($route.name) == false" />

    <RouterView />
  </main>
</template>

<style scoped>
main {
  min-height: 100vh;
  max-width: 100vw;
  background: linear-gradient(145deg, #5c2a84 23%, 55%, #3b1a99 85%);
}
</style>
