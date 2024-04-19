<script setup>
import { ref } from 'vue'
import { store } from '../store/store.js'
import { getText } from '../language/language.js'
import router from '@/router'
import ButtonComp from '../components/ButtonComp.vue'

const username = ref('')
const password = ref('')

const testData = {
  username: 'pvznuzda',
  password: '12345'
}

const submit = (e) => {
	e.preventDefault()
  if (username.value == testData.username && password.value == testData.password) {
		store.userAuthorised = true
    router.push('/')
  }
}
</script>

<template>
  <section
    class="container-xxl flex-grow-1 d-flex flex-column justify-content-center align-items-center"
    style="height: 100%"
  >
    <div
      class="col-8 col-md-6 col-lg-4 col-xl-4 bg-white bg-opacity-10 rounded-4 myshadow d-flex flex-column"
    >
      <div class="d-flex justify-content-center position-relative">
        <RouterLink to="/">
          <span class="icon-back material-symbols-outlined" style="font-size: 2.6rem">
            keyboard_backspace
          </span>
        </RouterLink>
        <h2 class="text-center roboto-bold my-2">{{ getText('login', store.lang) }}</h2>
      </div>
      <hr class="splitter col-9 mx-auto m-0 mb-2" />
			<form class="d-flex flex-column" action="">
				<div
					class="input-container col-8 mx-auto mt-4 mb-2 d-flex justify-content-around align-items-center"
				>
					<input v-model="username" type="text" id="username" :placeholder="getText('username', store.lang)" required />
					<span class="icon material-symbols-outlined" style="font-size: 24px; color: white">
						person
					</span>
				</div>
				<div
					class="input-container col-8 mx-auto mt-4 mb-4 d-flex justify-content-around align-items-center"
				>
					<input v-model="password" type="password" id="password" :placeholder="getText('password', store.lang)" required />
					<span class="icon material-symbols-outlined" style="font-size: 24px; color: white">
						lock
					</span>
				</div>
				<ButtonComp @click="submit" class="btn-lg fs-5 col-6 mx-auto mt-4">{{ getText('login', store.lang) }}</ButtonComp>
			</form>
      <div class="register col-8 mx-auto text-white roboto-regular my-4 text-center fs-6">
        {{ getText('dontHaveAcc', store.lang) }}
        <RouterLink class="register-link roboto-bold" to="/register">{{ getText('register', store.lang) }}</RouterLink>
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
