<script setup>
import { RouterView } from 'vue-router'
import { ref } from 'vue'
import HeaderComp from './components/HeaderComp.vue'

// const authorised = ref(false)
</script>

<template>
  <div class="container">
    <HeaderComp />

    <!-- <RouterView :userAuthorised="authorised" /> -->
    <RouterView />
  </div>
</template>

<style scoped>
.container {
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

main {
  display: flex;
  flex-grow: 1;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>
