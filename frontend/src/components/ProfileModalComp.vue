<script setup>
import { ref, watch } from 'vue'
import ButtonComp from './ButtonComp.vue'

// test data
const data = {
  username: 'pvznuzda',
  email: 'pashavznuzdajev@gmail.com',
  password: '12345',
  rating: 425,
  gameHistory: [1, 0, 1, 1, 0, 1, 1, 0, 0, 1]
}

// variables
const editProfileMode = ref(false)
const gameHistoryMode = ref(false)

// functions
const shortEmail = (email) => {
  const atSignPos = email.search('@')
  let first
  if (atSignPos >= 10) {
    first = email.substring(0, 8) + '...'
  }
  return first + email.substring(atSignPos)
}

const changePicture = (e) => {
  console.log(e.target.files[0])
  console.log(URL.createObjectURL(e.target.files[0]))
  document.getElementById('profile_img').src = URL.createObjectURL(e.target.files[0])
}
</script>

<template>
  <!-- Modal -->
  <div
    class="modal fade"
    id="exampleModal"
    tabindex="-1"
    aria-labelledby="exampleModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered">
      <div class="profile-modal modal-content myshadow border-0 rounded-4">
        <div class="modal-header border-0 d-flex flex-column m-0 p-0">
          <div class="d-flex position-relative w-100">
            <h1
              class="profile-modal-title modal-title fs-3 my-2 mx-auto roboto-bold"
              id="exampleModalLabel"
            >
              profile
            </h1>
            <button
              @click="editProfileMode = gameHistoryMode = false"
              type="button"
              class="icon-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            >
              <span class="material-symbols-outlined fs-2"> close </span>
            </button>
          </div>
          <hr class="splitter col-9 mx-auto m-0 mb-2" />
        </div>
        <!-- EDIT PROFILE -->
        <div v-if="editProfileMode" class="modal-body p-0 d-flex flex-column">
          <div class="d-flex mb-2">
            <img
              src="../assets/profile_img.png"
              alt="profile image"
              id="profile_img"
              class="profile-img my-2 mx-auto rounded-4"
            />
          </div>
          <form action="">
            <div class="d-flex col-9 col-md-7 mx-auto align-items-center mb-2 mb-md-3">
              <label for="picture" class="roboto-bold text-white fs-6">picture:</label>
              <input
                @change="changePicture"
                class="picture-input text-white roboto-regular fs-6 ms-2"
                type="file"
                id="picture"
                accept="image/*"
              />
            </div>
            <div class="d-flex col-9 col-md-7 mx-auto align-items-center mb-2 mb-md-3">
              <label for="username" class="roboto-bold text-white fs-6">username:</label>
              <input
                class="text-input text-white roboto-regular fs-6 ms-2"
                type="text"
                id="username"
                :placeholder="data.username"
              />
            </div>
            <div class="d-flex col-9 col-md-7 mx-auto align-items-center mb-2 mb-md-3">
              <label for="email" class="roboto-bold text-white fs-6">email:</label>
              <input
                class="text-input text-white roboto-regular fs-6 ms-2"
                type="email"
                id="email"
                :placeholder="data.email"
              />
            </div>
            <div class="d-flex col-9 col-md-7 mx-auto align-items-center mb-2 mb-md-3">
              <label for="password" class="roboto-bold text-white fs-6">password:</label>
              <input
                class="text-input text-white roboto-regular fs-6 ms-2"
                type="password"
                id="password"
                :placeholder="data.password.replace(/[ -~]/g, '*')"
              />
            </div>
            <div class="d-flex col-9 col-md-7 mx-auto align-items-center mb-3 mb-md-4">
              <label for="passwordRepeat" class="roboto-bold text-white fs-6">password:</label>
              <input
                class="text-input text-white roboto-regular fs-6 ms-2"
                type="password"
                id="passwordRepeat"
                :placeholder="data.password.replace(/[ -~]/g, '*')"
              />
            </div>
          </form>
          <div class="d-flex col-9 col-md-7 mx-auto justify-content-around mb-4">
            <ButtonComp @click="editProfileMode = false" class="save-btn fs-6">
              save changes
            </ButtonComp>
            <ButtonComp @click="editProfileMode = false" class="cancel-btn fs-6">
              cancel
            </ButtonComp>
          </div>
        </div>

        <!-- GAME HISTORY -->
        <div v-else-if="gameHistoryMode" class="modal-body p-0 d-flex flex-column">history</div>

        <!-- PROFILE -->
        <div v-else class="modal-body p-0 d-flex flex-column">
          <div class="d-flex">
            <img
              src="../assets/profile_img.png"
              alt="profile image"
              class="profile-img my-2 mx-auto rounded-4"
            />
          </div>
          <p class="col-9 col-md-7 mx-auto roboto-bold mb-2 mb-md-3 text-white fs-6">
            username: <span class="fs-6 ms-1">{{ data.username }}</span>
          </p>
          <p class="col-9 col-md-7 mx-auto roboto-bold mb-2 mb-md-3 text-white fs-6">
            e-mail:
            <span class="fs-6 ms-1">{{ shortEmail(data.email) }}</span>
          </p>
          <ButtonComp @click="editProfileMode = true" class="fs-6 col-9 col-md-7 mx-auto mb-4">
            edit profile
          </ButtonComp>
          <hr class="splitter col-9 mx-auto m-0" />
          <h2 class="profile-modal-title fs-3 my-3 mx-auto roboto-bold">last games</h2>
          <div class="last_games_circles d-flex col-9 col-md-7 mx-auto justify-content-around mb-3">
            <div class="circle" style="background-color: #66bf6a"></div>
            <div class="circle" style="background-color: #da4834"></div>
            <div class="circle" style="background-color: #66bf6a"></div>
            <div class="circle" style="background-color: #66bf6a"></div>
            <div class="circle" style="background-color: #da4834"></div>
          </div>
          <ButtonComp @click="gameHistoryMode = true" class="fs-6 col-9 col-md-7 mx-auto mb-4">
            view full history
          </ButtonComp>
        </div>
      </div>
    </div>
  </div>
  <!-- !Modal -->
</template>

<style scoped>
/* Modal */
.myshadow {
  box-shadow: -6px 6px 6px 0px rgba(0, 0, 0, 0.25);
}

.profile-modal {
  background: linear-gradient(145deg, rgba(60, 26, 153, 0.9) 23%, 55%, rgba(92, 42, 132, 0.9) 85%);
  backdrop-filter: blur(2px);
  /* height: 460px; */
}

.profile-modal-title {
  color: #f58562;
}

.profile-img {
  border: solid 3px #f58562;
  height: 80px;
  width: 80px;
  /* border-radius: 50%; */
}

.icon-close {
  position: absolute;
  background: none;
  border: none;
  top: 0.8rem;
  right: 0.8rem;
  color: white;
  transition: all 0.2s ease;
}
.icon-close:hover {
  color: #f58562;
}

.splitter {
  color: transparent;
  border-bottom: 3px solid #f58562;
  opacity: 1;
}

.circle {
  height: 2rem;
  width: 2rem;
  background: white;
  border-radius: 50%;
}
/* !Modal */

/* Edit profile */

.picture-input {
  color: white;
}
.picture-input::file-selector-button {
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid white;
  border-radius: 4px;
  color: white;
  transition: all 0.3s ease;
}
.picture-input::file-selector-button:hover {
  border-color: #f58562;
  cursor: pointer;
}

.save-btn:hover {
  color: #66bf6a;
}

.cancel-btn:hover {
  color: #da4834;
}

/* input */
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
/* !input */

.text-input {
  border-bottom: solid 2px white;
}

/* !Edit profile */
</style>
