<script setup>
import { onMounted } from 'vue'
import { RouterView } from 'vue-router'
import HeaderComp from './components/HeaderComp.vue'
import { store } from './store/store.js'
import { getText } from './language/language.js'
import { fetchWithJWT, connectWithSocket } from './utils/utils.js'

onMounted(async () => {
  try {
    if (localStorage.getItem('access') && localStorage.getItem('refresh')) {
      console.log('try to login...')
      const response = await fetchWithJWT(
        `${window.location.protocol}//${import.meta.env.VITE_APP_API_URL}/update-profile/`
      )
      if (!response.ok) {
        console.log("can't login with existing JWT")
        return
      }
      const data = await response.json()
      store.userAuthorised = true
      store.username = data.user.username
      store.email = data.user.email
      store.picture = `${window.location.protocol}//${import.meta.env.VITE_APP_API_URL}` + data.profile_picture
      console.log('logged in as ' + store.username)
      connectWithSocket()
    }
  } catch (error) {
    console.log(error)
  }
})
</script>

<template>
  <main class="d-flex flex-column">
    <HeaderComp v-if="['login', 'register'].includes($route.name) == false" />

    <RouterView class="mb-2" />
    <footer class="px-4 py-1 text-white text-center fs-6 roboto-regular mx-auto footer-help rounded-top-4">{{ getText('needHelp', store.lang) }}? lhasmi@student.42heilbronn.de</footer>
  </main>
</template>

<style>
body {
  background: #3b1a99;
}

main {
  min-height: 100vh;
  max-width: 100vw;
  background: linear-gradient(145deg, #5c2a84 23%, 55%, #3b1a99 85%);
}

.footer-help {
  background: rgba(255, 255, 255, 0.1);
}
</style>
