<script setup>
import { ref, onMounted } from 'vue'
import ProfileModalComp from './ProfileModalComp.vue'
import FriendsModalComp from './FriendsModalComp.vue'
import ButtonComp from './ButtonComp.vue'
import { store } from '../store/store.js'
import { logout } from '../utils/utils.js'
import { getText } from '../language/language.js'

// variables
const language = ref('')

// functions
const toggleLanguage = () => {
  const languages = ['en', 'de', 'ru']
  const index = languages.indexOf(language.value)

  language.value =
    index !== languages.length - 1 ? languages[index + 1] : languages[0]
  store.lang = language.value
  localStorage.setItem('lang', language.value)
}

onMounted(() => {
  language.value = localStorage.getItem('lang') || 'en'
  store.lang = language.value
  localStorage.setItem('lang', language.value)
})
</script>

<template>
  <!-- Header -->
  <header class="container-md mt-2">
    <nav
      class="navbar navbar-expand-lg bg-white bg-opacity-10 m-auto myshadow rounded-4 py-2"
      style="width: 100%"
    >
      <RouterLink
				tabindex="0"
        class="navbar-brand ms-5 fs-2 roboto-bold"
        to="/"
        aria-label="to home page button"
      >
        ft_transcendence
      </RouterLink>
      <button
				tabindex="0"
        class="navbar-toggler me-3"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNavAltMarkup"
        aria-controls="navbarNavAltMarkup"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
        <div class="navbar-nav ms-auto">
          <div v-if="!store.userAuthorised" class="d-flex">
            <RouterLink
							tabindex="0"
              class="nav-link mx-4 fs-4 roboto-medium align-self-center"
              to="/register"
              aria-label="to registration page button"
              >{{ getText('register', language) }}</RouterLink
            >
            <RouterLink
							tabindex="0"
              class="nav-link mx-4 fs-4 roboto-medium align-self-center"
              to="/login"
              aria-label="to login page button"
              >{{ getText('login', language) }}</RouterLink
            >
          </div>
          <div v-else class="d-flex">
            <button
							tabindex="0"
              class="nav-link mx-4 fs-4 roboto-medium align-self-center"
              data-bs-toggle="modal"
              data-bs-target="#profileModal"
              aria-label="open profile modal button"
            >
              {{ getText('profile', language) }}
            </button>
            <button
							tabindex="0"
              class="nav-link mx-4 fs-4 roboto-medium align-self-center"
              data-bs-toggle="modal"
              data-bs-target="#friendsModal"
              aria-label="open friends modal button"
            >
              {{ getText('friends', language) }}
            </button>
            <button
							tabindex="0"
              @click="logout"
              class="nav-link mx-4 fs-4 roboto-medium align-self-center"
              aria-label="logout button"
            >
              {{ getText('logout', language) }}
            </button>
          </div>
          <ButtonComp
						tabindex="0"
            @click="toggleLanguage"
            class="mx-4"
            style="width: 40px"
            aria-label="change language button"
            >{{ language }}</ButtonComp
          >
        </div>
      </div>
    </nav>

    <ProfileModalComp />
    <FriendsModalComp />
  </header>
  <!-- !Header -->
</template>

<style scoped>
/* Header */
@media (min-width: 1200px) {
  .navbar {
    width: 900px;
  }
}

.navbar-brand,
.navbar-brand:hover,
.navbar-brand:focus {
  color: #f58562;
}

.navbar-nav .nav-link {
  color: #e8e8e8;
}
.navbar-nav .nav-link:hover {
  text-decoration: underline;
  text-decoration-color: #f58562;
}
.navbar-nav .nav-link:focus {
  text-decoration: underline;
  text-decoration-color: #f58562;
}

.myshadow {
  box-shadow: -6px 6px 6px 0px rgba(0, 0, 0, 0.25);
}

.language {
  border: none;
  background: none;
}
/* !Header */
</style>
