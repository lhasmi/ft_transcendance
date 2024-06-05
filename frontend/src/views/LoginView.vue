<script setup>
import { ref, onMounted } from 'vue'
import { store } from '../store/store.js'
import { getText, getError } from '../language/language.js'
import router from '@/router'
import ButtonComp from '../components/ButtonComp.vue'
import { fetchWithJWT, connectWithSocket, logout } from '@/utils/utils'

// variables
const username = ref('')
const password = ref('')
const errorMsg = ref('')
const renderOtpPrompt = ref(false) // should be false
const otpCode = ref('')
const canFetchProfile = ref(false)

// functions
const redirectTo42 = async () => {
  try {
    const response = await fetch(
      `${window.location.protocol}//${import.meta.env.VITE_APP_API_URL}/oauth/login/`
    )
    if (!response.ok) {
      console.log(response)
      console.log('redirectTo42: bad response')
    } else {
      const data = await response.json()
      console.log(data)
      window.location.href = data.link
    }
  } catch (error) {
    console.log(error)
  }
}

const submit = async (e) => {
  e.preventDefault()
  canFetchProfile.value = false

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
    const response = await fetch(
      `${window.location.protocol}//${import.meta.env.VITE_APP_API_URL}/login/`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: username.value,
          password: password.value,
        }),
      }
    )
    if (!response.ok) {
      console.log('/login/ response not ok: ' + response.status)
      const data = await response.json()
      errorMsg.value = data.error
    } else {
      const data = await response.json()
      console.log(data)
      if (
        data.message ==
        'OTP sent to your email. Please verify to complete login.'
      ) {
        renderOtpPrompt.value = true
        console.log('NEED TO PROMPT OTP CODE')
      } else {
        localStorage.setItem('access', data.access)
        localStorage.setItem('refresh', data.refresh)
        canFetchProfile.value = true
      }
    }
  } catch {
    errorMsg.value = 'fetch request failed'
  }
  if (renderOtpPrompt.value) return
  if (!canFetchProfile.value) return
  try {
    const response = await fetchWithJWT(
      `${window.location.protocol}//${import.meta.env.VITE_APP_API_URL}/update-profile/`
    )
    if (!response.ok) {
      console.log("can't login with existing JWT")
    } else {
      const data = await response.json()
      store.userAuthorised = true
      store.username = data.user.username
      store.email = data.user.email
      store.picture =
        `${window.location.protocol}//${import.meta.env.VITE_APP_API_URL}` +
        data.profile_picture
      console.log('logged in as ' + store.username)
      router.push('/')
      connectWithSocket()
    }
  } catch (error) {
    console.log('catch: ' + error)
  }
}

const sendOTP = async () => {
  console.log('verify-otp')
  console.log('username: ' + username.value)
  console.log('otp code: ' + otpCode.value)

  canFetchProfile.value = false
  try {
    const response = await fetch(
      `${window.location.protocol}//${import.meta.env.VITE_APP_API_URL}/verify-login-otp/`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: username.value,
          otp: otpCode.value,
        }),
      }
    )
    if (!response.ok) {
      console.log('verify-otp error: ')
      console.log(response)
      const data = await response.json()
      console.log(data)
      errorMsg.value = data.error
    } else {
      const data = await response.json()
      console.log('verify-otp success: ')
      console.log(data)
      localStorage.setItem('access', data.access)
      localStorage.setItem('refresh', data.refresh)
      canFetchProfile.value = true
    }
  } catch (error) {
    console.log('verify-otp fetch error: ' + error)
  }
  if (!canFetchProfile.value) return
  try {
    const response = await fetchWithJWT(
      `${window.location.protocol}//${import.meta.env.VITE_APP_API_URL}/update-profile/`
    )
    if (!response.ok) {
      console.log("can't login with existing JWT")
    } else {
      const data = await response.json()
      store.userAuthorised = true
      store.username = data.user.username
      store.email = data.user.email
      store.picture =
        `${window.location.protocol}//${import.meta.env.VITE_APP_API_URL}` +
        data.profile_picture
      console.log('logged in as ' + store.username)
      router.push('/')
      connectWithSocket()
    }
  } catch (error) {
    console.log('catch: ' + error)
  }
}

const backFromOTP = () => {
  renderOtpPrompt.value = false
  errorMsg.value = ''
  otpCode.value = ''
}

onMounted(async () => {
  if (store.userAuthorised) {
    logout()
  }
  const query = window.location.search
  query ? console.log('query:' + query) : null
  if (query && query.startsWith('?code=')) {
    // check if query starts with '?code=' ???
    try {
      const response = await fetch(
        `${window.location.protocol}//${import.meta.env.VITE_APP_API_URL}/oauth/callback/${query}`
      )
      if (!response.ok) {
        console.log('/oauth/callback/ response not ok: ' + response.status)
        const data = await response.json()
        console.log(data)
        errorMsg.value = data.error
      } else {
        const data = await response.json()
        console.log('callback')
        console.log(data)
        if (
          data.message ==
          'OTP sent to your email. Please verify to complete login.'
        ) {
          // NEED TO GET USERNAME IN CALLBACK RESPONSE
          renderOtpPrompt.value = true
          console.log('NEED TO PROMPT OTP CODE')
          username.value = data.username
        } else {
          localStorage.setItem('access', data.access)
          localStorage.setItem('refresh', data.refresh)
          canFetchProfile.value = true
        }
      }
    } catch (error) {
      console.log('catch: ' + error)
    }
    if (!canFetchProfile.value) return
    try {
      const response = await fetchWithJWT(
        `${window.location.protocol}//${import.meta.env.VITE_APP_API_URL}/update-profile/`
      )
      if (!response.ok) {
        console.log("can't login with existing JWT")
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
        <button v-if="renderOtpPrompt" class="router-link" style="background: none; border: none" @click="backFromOTP">
          <span
            class="icon-back material-symbols-outlined"
            style="font-size: 2.6rem"
            aria-label="back button"
          >
            keyboard_backspace
          </span>
        </button>
        <RouterLink v-else to="/" aria-label="back button" class="router-link">
          <span
            class="icon-back material-symbols-outlined"
            style="font-size: 2.6rem"
            aria-label="back button"
          >
            keyboard_backspace
          </span>
        </RouterLink>

        <h2 class="text-center roboto-bold my-2">
          {{ getText('login', store.lang) }}
        </h2>
      </div>
      <hr class="splitter col-12 mx-auto m-0 mb-2" />
      <div
        v-if="renderOtpPrompt"
        class="col-11 col-md-8 mx-auto d-flex flex-column"
      >
        <p class="m-0 mx-auto mb-3 text-center text-white roboto-regular fs-5">
          otp code has been sent to your email
        </p>
        <div class="col-9 mx-auto mb-3">
          <input
            v-model="otpCode"
            class="text-input text-white text-center roboto-regular fs-6"
            type="text"
            id="otpCode"
            placeholder="otp code"
            aria-label="input for otp code"
          />
        </div>
        <div
          v-if="errorMsg"
          class="my-1 fs-6 roboto-bold text-center"
          style="color: #da4834"
        >
          {{ errorMsg }}
        </div>
        <ButtonComp
          @click="sendOTP"
          class="fs-6 col-9 col-md-7 mx-auto mb-4"
          style="width: 120px"
          aria-label="send otp code button"
        >
          send OTP
        </ButtonComp>
      </div>
      <div v-else class="d-flex flex-column">
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
            class="input-container col-8 mx-auto mt-4 mb-2 d-flex justify-content-around align-items-center"
          >
            <input
              v-model="password"
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
            v-if="errorMsg"
            class="my-1 fs-6 roboto-bold text-center"
            style="color: #da4834"
          >
            {{ errorMsg }}
          </div>
          <ButtonComp
            @click="submit"
            class="btn-lg fs-5 col-7 mx-auto mt-4"
            aria-label="login button"
            >{{ getText('login', store.lang) }}</ButtonComp
          >
        </form>
        <p class="text-center fs-4 roboto-bold my-2" style="color: #f58562">
          or
        </p>
        <ButtonComp
          @click="redirectTo42"
          class="btn-lg fs-5 col-7 mx-auto"
          aria-label="login with 42"
        >
          {{ getText('loginWith42', store.lang) }}
        </ButtonComp>
        <div
          class="register col-8 mx-auto text-white roboto-regular my-4 text-center fs-6"
        >
          {{ getText('dontHaveAcc', store.lang) }}
          <RouterLink
            class="register-link roboto-bold"
            to="/register"
            aria-label="to registration page button"
            >{{ getText('register', store.lang) }}</RouterLink
          >
        </div>
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
/* .icon-back:focus {
  color: #f58562;
} */
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

.text-input {
  border-bottom: solid 2px white;
}

.register {
  font-size: 0.8rem;
}

.register-link {
  color: #f58562;
  text-decoration: none;
}
</style>
