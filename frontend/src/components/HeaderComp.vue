<script setup>
import { ref } from 'vue'
import ProfileModalComp from './ProfileModalComp.vue'
import FriendsModalComp from './FriendsModalComp.vue'
import { store } from '../store/store.js'

// variables

// functions
const logout = () => {
  store.userAuthorised = false
}

// const profileOpen = async () => {
//     console.log('opened')
//     const response = await fetch('http://127.0.0.1:8000/players/')
//     const user = await response.json()
//     console.log(user)
// }
</script>

<template>
  <!-- Header -->
  <header class="container mt-2">
    <nav class="navbar navbar-expand-md bg-white bg-opacity-10 m-auto myshadow rounded-4 py-1">
      <RouterLink class="navbar-brand ms-5 fs-3 roboto-medium" to="/">ft_transcendence</RouterLink>
      <button
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
            <RouterLink class="nav-link mx-4 fs-5 roboto-medium align-self-center" to="/register"
              >register</RouterLink
            >
            <RouterLink class="nav-link mx-4 fs-5 roboto-regular align-self-center" to="/login"
              >login</RouterLink
            >
          </div>
          <div v-else class="d-flex">
            <button
              class="nav-link mx-4 fs-5 roboto-regular align-self-center"
              data-bs-toggle="modal"
              data-bs-target="#profileModal"
            >
              profile
            </button>
            <button
              class="nav-link mx-4 fs-5 roboto-regular align-self-center"
              data-bs-toggle="modal"
              data-bs-target="#friendsModal"
            >
              friends
            </button>
            <button @click="logout" class="nav-link mx-4 fs-5 roboto-regular align-self-center">
              logout
            </button>
          </div>
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

.myshadow {
  box-shadow: -6px 6px 6px 0px rgba(0, 0, 0, 0.25);
}
/* !Header */
</style>
