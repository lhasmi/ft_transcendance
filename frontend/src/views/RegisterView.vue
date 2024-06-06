<script setup>
import { onMounted, ref } from 'vue'
import { store } from '../store/store.js'
import { getText, getError } from '../language/language.js'
import router from '@/router'
import ButtonComp from '../components/ButtonComp.vue'
import { fetchWithJWT, connectWithSocket, logout } from '@/utils/utils.js'

// variables
const username = ref('')
const email = ref('')
const password = ref('')
const password2 = ref('')
const errorMsg = ref('')

// funcions
const submit = async (e) => {
  e.preventDefault()
  if (store.userAuthorised) {
    logout()
  }

  // client side validation
  if (!username.value) {
    errorMsg.value = getError('usernameEmpty', store.lang)
    return
  }
  if (!email.value) {
    errorMsg.value = getError('emailEmpty', store.lang)
    return
  }
  if (!validateEmail(email.value)) {
    errorMsg.value = getError('emailInvalid', store.lang)
    return
  }
  if (!password.value) {
    errorMsg.value = getError('passwordEmpty', store.lang)
    return
  }
  if (password.value != password2.value) {
    errorMsg.value = getError('passwordsDontMatch', store.lang)
    return
  }
  errorMsg.value = ''

  try {
    const response = await fetch(
      `${window.location.protocol}//${import.meta.env.VITE_APP_API_URL}/register/`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: username.value,
          password: password.value,
          email: email.value,
        }),
      }
    )
    const data = await response.json()
    console.log(data)
    if (!response.ok) {
      if (data.password_error) errorMsg.value = data.password_error[0][1][0]
      else errorMsg.value = data.error
    } else {
      localStorage.setItem('access', data.access)
      localStorage.setItem('refresh', data.refresh)
    }
  } catch {
    errorMsg.value = 'fetch request failed'
  }
  if (errorMsg.value != '') return
  try {
    const response = await fetchWithJWT(
      `${window.location.protocol}//${import.meta.env.VITE_APP_API_URL}/update-profile/`
    )
    if (!response.ok) {
      console.log("couldn't fetch profile data")
      errorMsg.value = 'JWT invalid'
      return
    }
    const data = await response.json()
    store.userAuthorised = true
    store.username = data.user.username
    store.email = data.user.email
    store.picture =
      `${window.location.protocol}//${import.meta.env.VITE_APP_API_URL}` +
      data.profile_picture
    console.log('logged in as ' + store.username)
    connectWithSocket()
    router.push('/')
  } catch (error) {
    console.log('catch: ' + error)
  }
}

const validateEmail = (str) => {
  const validEmailRegex =
    /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/
  if (str.match(validEmailRegex)) return true
  return false
}

onMounted(() => {
  if (store.userAuthorised) {
    logout()
  }
})
</script>

<template>
  <section
    class="container-xxl flex-grow-1 d-flex flex-column justify-content-center align-items-center"
    style="height: 100%"
  >
    <div
      class="col-9 col-md-6 col-xl-4 bg-white bg-opacity-10 rounded-4 myshadow d-flex flex-column"
    >
      <div class="d-flex justify-content-center position-relative">
        <RouterLink to="/" aria-label="back button" class="router-link">
          <span
            class="icon-back material-symbols-outlined"
            style="font-size: 2.6rem"
          >
            keyboard_backspace
          </span>
        </RouterLink>
        <h2 class="text-center roboto-bold my-2">
          {{ getText('register', store.lang) }}
        </h2>
      </div>
      <hr class="splitter col-12 mx-auto m-0 mb-2" />
      <form class="col-9 col-md-8 mx-auto">
        <div
          class="input-container mt-4 mb-2 d-flex justify-content-around align-items-center"
        >
          <input
            v-model="username"
            autocomplete="off"
            type="text"
            id="username"
            :placeholder="getText('username', store.lang)"
            required
            aria-label="input for username"
          />
          <span
            class="icon material-symbols-outlined"
            style="font-size: 24px; color: white"
          >
            person
          </span>
        </div>
        <div
          class="input-container mt-4 mb-2 d-flex justify-content-around align-items-center"
        >
          <input
            v-model="email"
            autocomplete="off"
            type="email"
            id="email"
            :placeholder="getText('email', store.lang)"
            required
            aria-label="input for email"
          />
          <span
            class="icon material-symbols-outlined"
            style="font-size: 22px; color: white; margin-right: 1px"
          >
            mail
          </span>
        </div>
        <div
          class="input-container mt-4 mb-2 d-flex justify-content-around align-items-center"
        >
          <input
            v-model="password"
            autocomplete="off"
            type="password"
            id="password"
            :placeholder="getText('password', store.lang)"
            required
            aria-label="input for password"
          />
          <span
            class="icon material-symbols-outlined"
            style="font-size: 24px; color: white"
          >
            lock
          </span>
        </div>
        <div
          class="input-container mt-4 mb-4 d-flex justify-content-around align-items-center"
        >
          <input
            v-model="password2"
            autocomplete="off"
            type="password"
            id="password2"
            :placeholder="getText('password', store.lang)"
            required
            aria-label="input for password"
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
        <ButtonComp
          @click="submit"
          class="btn-lg mt-4 fs-5 d-flex mx-auto"
          aria-label="register button"
          >{{ getText('register', store.lang) }}</ButtonComp
        >
      </form>
      <div
        class="login col-8 mx-auto text-white roboto-regular my-4 text-center fs-6"
      >
        {{ getText('alreadyHaveAcc', store.lang) }}
        <RouterLink
          class="login-link roboto-bold"
          to="/login"
          aria-label="to login page button"
          >{{ getText('login', store.lang) }}</RouterLink
        >
      </div>
    </div>
  </section>
</template>

<style scoped>
.myshadow {
  box-shadow: -6px 6px 6px 0px rgba(0, 0, 0, 0.25);
}

.router-link {
  position: absolute;
  top: 0.5rem;
  left: 1rem;
  color: white;
  transition: all 0.2s ease;
}
.router-link:hover {
  color: #f58562;
}
.router-link:focus {
  color: #f58562;
}

.icon-back {
  color: white;
  transition: all 0.2s ease;
}
.icon-back:hover,
.icon-back:focus {
  color: #f58562;
}
.router-link:focus .icon-back {
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

.login {
  font-size: 0.8rem;
}

.login-link {
  color: #f58562;
  text-decoration: none;
}
</style>
