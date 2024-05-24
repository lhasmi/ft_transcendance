<script setup>
import { ref, onMounted } from 'vue'
import { store } from '../store/store.js'
import { getText, getError } from '../language/language.js'
import router from '@/router'
import ButtonComp from '../components/ButtonComp.vue'
import { fetchWithJWT } from '@/utils/utils'

const testData = {
  username: 'pvznuzda',
  password: '12345',
}

// variables
const username = ref('')
const password = ref('')
const errorMsg = ref('')

// functions
const redirectTo42 = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/oauth/login/')
    if (!response.ok) {
      console.log(response)
      console.log('redirectTo42: bad response')
    }
    const data = await response.json()

    console.log(data)
    window.location.href = data.link // replace url
  } catch (error) {
    console.log(error)
  }
}

const submit = async (e) => {
  e.preventDefault()
  if (
    username.value == testData.username &&
    password.value == testData.password
  ) {
    // test
    store.userAuthorised = true
    router.push('/')
  }

  if (!username.value) {
    errorMsg.value = getError('usernameEmpty', store.lang)
    return
  }
  if (!password.value) {
    errorMsg.value = getError('passwordEmpty', store.lang)
    return
  }
  errorMsg.value = ''

  try {
    const response = await fetch('http://127.0.0.1:8000/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: username.value,
        password: password.value,
      }),
    })
    const data = await response.json()
    console.log(data)
    if (!response.ok) {
      errorMsg.value = data.error
    } else {
      localStorage.setItem('access', data.access)
      localStorage.setItem('refresh', data.refresh)
      store.userAuthorised = true
      router.push('/')
    }
  } catch {
    errorMsg.value = 'fetch request failed'
  }
  try {
    const response = await fetchWithJWT('http://127.0.0.1:8000/update-profile/')
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
  } catch (error) {
    console.log('catch: ' + error)
  }
}

onMounted(async () => {
  const query = window.location.search
  console.log('query:' + query)
  if (query) {
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/oauth/callback/${query}`
      )
      const data = await response.json()
      console.log(data)
      localStorage.setItem('access', data.access)
      localStorage.setItem('refresh', data.refresh)
      store.userAuthorised = true
      router.push('/')
    } catch (error) {
      console.log('catch: ' + error)
    }
    try {
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
    } catch (error) {
      console.log('catch: ' + error)
    }
  }
})
</script>

<template>
  <section
    class="container-md flex-grow-1 d-flex flex-column justify-content-center align-items-center"
  >
    <div
      class="col-11 col-md-8 col-lg-5 col-xl-4 bg-white bg-opacity-10 rounded-4 myshadow d-flex flex-column"
    >
      <div class="d-flex justify-content-center position-relative">
        <RouterLink to="/">
          <span
            class="icon-back material-symbols-outlined"
            style="font-size: 2.6rem"
          >
            keyboard_backspace
          </span>
        </RouterLink>
        <h2 class="text-center roboto-bold my-2">
          {{ getText('login', store.lang) }}
        </h2>
      </div>
      <hr class="splitter col-12 mx-auto m-0 mb-2" />
      <form class="d-flex flex-column">
        <div
          class="input-container col-8 mx-auto mt-4 mb-2 d-flex justify-content-around align-items-center"
        >
          <input
            v-model="username"
            type="text"
            id="username"
            :placeholder="getText('username', store.lang)"
            required
          />
          <span
            class="icon material-symbols-outlined"
            style="font-size: 24px; color: white"
          >
            person
          </span>
        </div>
        <div
          class="input-container col-8 mx-auto mt-4 mb-2 d-flex justify-content-around align-items-center"
        >
          <input
            v-model="password"
            type="password"
            id="password"
            :placeholder="getText('password', store.lang)"
            required
          />
          <span
            class="icon material-symbols-outlined"
            style="font-size: 24px; color: white"
          >
            lock
          </span>
        </div>
        <div
          v-if="errorMsg"
          class="my-1 fs-6 roboto-bold text-center"
          style="color: #da4834"
        >
          {{ errorMsg }}
        </div>
        <ButtonComp @click="submit" class="btn-lg fs-5 col-7 mx-auto mt-4">{{
          getText('login', store.lang)
        }}</ButtonComp>
      </form>
      <p class="text-center fs-4 roboto-bold my-2" style="color: #f58562">or</p>
      <ButtonComp @click="redirectTo42" class="btn-lg fs-5 col-7 mx-auto">
        {{ getText('loginWith42', store.lang) }}
      </ButtonComp>
      <div
        class="register col-8 mx-auto text-white roboto-regular my-4 text-center fs-6"
      >
        {{ getText('dontHaveAcc', store.lang) }}
        <RouterLink class="register-link roboto-bold" to="/register">{{
          getText('register', store.lang)
        }}</RouterLink>
      </div>
    </div>
  </section>
</template>

<style scoped>
.myshadow {
  box-shadow: -6px 6px 6px 0px rgba(0, 0, 0, 0.25);
}

.icon-back {
  position: absolute;
  top: 0.5rem;
  left: 1rem;
  color: white;
  transition: all 0.2s ease;
}
.icon-back:hover {
  color: #f58562;
}

h2 {
  color: #f58562;
}

.splitter {
  color: transparent;
  border-bottom: 3px solid #f58562;
  opacity: 1;
}

.input-container {
  border-bottom: 2px solid white;
}

input {
  width: 100%;
  padding-left: 0.4rem;
  background: none;
  border: none;
  color: white;
}
input::placeholder {
  color: white;
  font-family: 'Roboto';
}
input:focus {
  outline: none;
}
input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus {
  -webkit-text-fill-color: white;
  transition: background-color 5000s ease-in-out 0s;
}

.register {
  font-size: 0.8rem;
}

.register-link {
  color: #f58562;
  text-decoration: none;
}
</style>
