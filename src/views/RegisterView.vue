<script setup>
import {ref} from 'vue'
import { store } from '../store/store.js'
import { getText } from '../language/language.js'
import ButtonComp from '../components/ButtonComp.vue'

// variables
const username = ref('')
const email = ref('')
const password = ref('')
const password2 = ref('')

// funcions
const submit = async () => {
	const response = await fetch('http://127.0.0.1:8000/register/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
				username: username.value,
        password: password.value,
        email: email.value
    })
	})
	const data = await response.json()
	console.log(data)
}

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
        <RouterLink to="/">
          <span class="icon-back material-symbols-outlined" style="font-size: 2.6rem">
            keyboard_backspace
          </span>
        </RouterLink>
        <h2 class="text-center roboto-bold my-2">{{ getText('register', store.lang) }}</h2>
      </div>
      <hr class="splitter col-9 mx-auto m-0 mb-2" />
      <div
        class="input-container col-8 mx-auto mt-4 mb-2 d-flex justify-content-around align-items-center"
      >
        <input v-model="username" autocomplete="off" type="text" id="username" :placeholder="getText('username', store.lang)" />
        <span class="icon material-symbols-outlined" style="font-size: 24px; color: white">
				person
        </span>
      </div>
      <div
        class="input-container col-8 mx-auto mt-4 mb-2 d-flex justify-content-around align-items-center"
      >
        <input v-model="email" autocomplete="off" type="email" id="email" :placeholder="getText('email', store.lang)" />
        <span
          class="icon material-symbols-outlined"
          style="font-size: 22px; color: white; margin-right: 1px"
        >
          mail
        </span>
      </div>
      <div
        class="input-container col-8 mx-auto mt-4 mb-2 d-flex justify-content-around align-items-center"
      >
        <input v-model="password" autocomplete="off" type="password" id="password" :placeholder="getText('password', store.lang)" />
        <span class="icon material-symbols-outlined" style="font-size: 24px; color: white">
          lock
        </span>
      </div>
      <div
        class="input-container col-8 mx-auto mt-4 mb-4 d-flex justify-content-around align-items-center"
      >
        <input
				v-model="password2"
          autocomplete="off"
          type="password"
          id="password2"
          :placeholder="getText('password', store.lang)"
        />
        <span class="icon material-symbols-outlined" style="font-size: 24px; color: white">
          lock
        </span>
      </div>
      <ButtonComp @click="submit" class="btn-lg fs-5 col-6 mx-auto mt-4">{{ getText('register', store.lang) }}</ButtonComp>
      <div class="login col-8 mx-auto text-white roboto-regular my-4 text-center fs-6">
        {{ getText('alreadyHaveAcc', store.lang) }}
        <RouterLink class="login-link	roboto-bold" to="/login">{{ getText('login', store.lang) }}</RouterLink>
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

.login {
  font-size: 0.8rem;
}

.login-link {
  color: #f58562;
  text-decoration: none;
}
</style>
