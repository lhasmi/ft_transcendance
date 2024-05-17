<script setup>
import { onMounted } from 'vue'
import { RouterView } from 'vue-router'
import HeaderComp from './components/HeaderComp.vue'
import { store } from './store/store.js'
import { fetchWithJWT } from './utils/utils.js'

onMounted(async () => {
	try {
		const response = await fetch('https://api.intra.42.fr/oauth/token?grant_type=authorization_code&code=814e7d160785257630580087a8627541a333c64a138e1c2a41be41689325ffb9&redirect_uri=http://127.0.0.1:8000/oauth/callback/&client_id=u-s4t2ud-5d66c931fc39d767149776c9efda2aa711a4167224361348d78cad3781c36d69&client_secret=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', {
			method: 'POST'
		})
		if (!response.ok) {
			console.log(response.error)	
		}
		const data = await response.json()
		console.log(data)
	} catch(error) {
		console.log(error)
	}

	try {
		if (localStorage.getItem('access') && localStorage.getItem('refresh')) {
			console.log('try to login')
			const response = await fetchWithJWT('http://127.0.0.1:8000/update-profile/')
			if (!response.ok) {
				console.log('can\'t login with existing JWT')
				return
			}
			const data = await response.json()
			store.userAuthorised = true
			store.username = data.user.username
			store.email = data.user.email
			store.picture = 'http://127.0.0.1:8000' + data.profile_picture
			console.log(store.username)
		}
	} catch(error) {
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
