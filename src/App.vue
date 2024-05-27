<script setup>
import { onMounted } from 'vue'
import { RouterView } from 'vue-router'
import HeaderComp from './components/HeaderComp.vue'
import { store } from './store/store.js'
import { fetchWithJWT, connectWithSocket } from './utils/utils.js'

onMounted(async () => {
  try {
    if (localStorage.getItem('access') && localStorage.getItem('refresh')) {
      console.log('try to login...')
      const response = await fetchWithJWT(
        'http://127.0.0.1:8000/update-profile/'
      )
      if (!response.ok) {
        console.log("can't login with existing JWT")
        return
      }
      const data = await response.json()
      store.userAuthorised = true
      store.username = data.user.username
      store.email = data.user.email
      store.picture = 'http://127.0.0.1:8000' + data.profile_picture
      console.log('logged in as ' + store.username)
			connectWithSocket()
      // socket connection to track online status
      // store.socket = new WebSocket(
      //   `ws://localhost:8000/ws/status/?token=${localStorage.getItem('access')}`
      // )
      // store.socket.onopen = () => {
      //   console.log(
      //     'CONNECTED TO STATUS CONSUMER (my online status should be online now)'
      //   )
      // }
    }
  } catch (error) {
    console.log(error)
  }
})
</script>

<template>
  <main class="d-flex flex-column">
    <HeaderComp v-if="['login', 'register'].includes($route.name) == false" />

    <RouterView />
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
</style>
