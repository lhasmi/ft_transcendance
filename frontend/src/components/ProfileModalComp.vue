<script setup>
import { ref } from 'vue'
import ButtonComp from './ButtonComp.vue'

// test data
const data = {
  username: 'pvznuzda',
  email: 'pashavznuzdajev@gmail.com',
  password: '12345',
  gameHistory: [
    {
      id: 8,
      player1: 'pvznuzda',
      player2: 'test1',
      score1: 6,
      score2: 7,
      date: '11.04.2024 14:35'
    },
    {
      id: 7,
      player1: 'pvznuzda',
      player2: 'test2',
      score1: 7,
      score2: 5,
      date: '11.04.2024 14:35'
    },
    {
      id: 6,
      player1: 'pvznuzda',
      player2: 'test3',
      score1: 7,
      score2: 2,
      date: '11.04.2024 14:35'
    },
    {
      id: 5,
      player1: 'pvznuzda',
      player2: 'test1',
      score1: 4,
      score2: 7,
      date: '11.04.2024 14:35'
    },
    {
      id: 4,
      player1: 'pvznuzda',
      player2: 'test1',
      score1: 7,
      score2: 2,
      date: '11.04.2024 14:35'
    },
    {
      id: 3,
      player1: 'pvznuzda',
      player2: 'test3',
      score1: 2,
      score2: 7,
      date: '11.04.2024 14:35'
    },
    {
      id: 2,
      player1: 'pvznuzda',
      player2: 'test2',
      score1: 6,
      score2: 5,
      date: '11.04.2024 14:35'
    },
    { id: 1, player1: 'pvznuzda', player2: 'test2', score1: 7, score2: 5, date: '11.04.2024 14:35' }
  ]
}

// variables
const editProfile = ref(false)
const gameHistory = ref(false)
const title = ref('profile')

// functions
const toEditProfile = () => {
  editProfile.value = true
  title.value = 'edit profile'
}

const toGameHistory = () => {
  gameHistory.value = true
  title.value = 'game history'
}

const backProfileModal = () => {
  title.value = 'profile'
  editProfile.value = false
  gameHistory.value = false
}

const shortEmail = (email) => {
  const atSignPos = email.search('@')
  let first
  if (atSignPos >= 10) {
    first = email.substring(0, 8) + '...'
  }
  return first + email.substring(atSignPos)
}

const getCircleColor = (index) => {
  if (index >= data.gameHistory.length) return 'background: rgba(255, 255, 255, 0.1)'
  return data.gameHistory[index].score1 > data.gameHistory[index].score2
    ? 'background: #66bf6a'
    : 'background: #da4834'
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
    id="profileModal"
    tabindex="-1"
    aria-labelledby="profileModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-scrollable modal-dialog-centered">
      <div class="profile-modal modal-content myshadow border-0 rounded-4">
        <div class="modal-header border-0 d-flex flex-column m-0 p-0">
          <div class="d-flex position-relative w-100">
            <button
              v-if="editProfile || gameHistory"
              @click="backProfileModal"
              type="button"
              class="icon-back"
            >
              <span class="material-symbols-outlined" style="font-size: 2.5rem">
                keyboard_backspace
              </span>
            </button>

            <h1
              class="profile-modal-title modal-title fs-3 my-2 mx-auto roboto-bold"
              id="profileModalLabel"
            >
              {{ title }}
            </h1>
            <button
              @click="backProfileModal"
              type="button"
              class="icon-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            >
              <span class="material-symbols-outlined" style="font-size: 2rem"> close </span>
            </button>
          </div>
          <hr class="splitter col-9 mx-auto m-0 mb-2" />
        </div>
        <!-- EDIT PROFILE -->
        <div v-if="editProfile" class="modal-body p-0 d-flex flex-column">
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
            <ButtonComp @click="backProfileModal" class="save-btn fs-6"> save changes </ButtonComp>
            <ButtonComp @click="backProfileModal" class="cancel-btn fs-6"> cancel </ButtonComp>
          </div>
        </div>

        <!-- GAME HISTORY -->
        <div
          v-else-if="gameHistory"
          class="modal-body p-0 d-flex flex-column mb-3"
          style="height: 396px"
        >
          <div class="col-9 col-md-7 mx-auto mb-1" v-for="item in data.gameHistory" :key="item.id">
            <p class="game-date text-center text-white roboto-regular mb-1">{{ item.date }}</p>
            <div class="d-flex justify-content-center position-relative">
              <p class="player-left text-white roboto-regular fs-5">{{ item.player1 }}</p>
              <p class="text-white roboto-bold fs-5">
                <span
                  class="roboto-bold"
                  :style="item.score1 > item.score2 ? 'color: #f58562' : ''"
                  >{{ item.score1 }}</span
                >
                :
                <span
                  class="roboto-bold"
                  :style="item.score2 > item.score1 ? 'color: #f58562' : ''"
                  >{{ item.score2 }}</span
                >
              </p>
              <p class="player-right text-white roboto-regular fs-5">{{ item.player2 }}</p>
            </div>
          </div>
        </div>

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
          <ButtonComp @click="toEditProfile" class="fs-6 col-9 col-md-7 mx-auto mb-4">
            edit profile
          </ButtonComp>
          <hr class="splitter col-9 mx-auto m-0" />
          <h2 class="profile-modal-title fs-3 my-3 mx-auto roboto-bold">last games</h2>
          <div class="last_games_circles d-flex col-9 col-md-7 mx-auto justify-content-around mb-3">
            <div class="circle" :style="getCircleColor(4)"></div>
            <div class="circle" :style="getCircleColor(3)"></div>
            <div class="circle" :style="getCircleColor(2)"></div>
            <div class="circle" :style="getCircleColor(1)"></div>
            <div class="circle" :style="getCircleColor(0)"></div>
          </div>
          <ButtonComp @click="toGameHistory" class="fs-6 col-9 col-md-7 mx-auto mb-4">
            game history
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
  top: 0.7rem;
  right: 0.7rem;
  color: white;
  transition: all 0.2s ease;
}
.icon-close:hover {
  color: #f58562;
}

.icon-back {
  position: absolute;
  background: none;
  border: none;
  top: 0.5rem;
  left: 1rem;
  color: white;
  transition: all 0.2s ease;
}
.icon-back:hover {
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

/* Game History */
.player-left {
  position: absolute;
  left: 0;
}

.player-right {
  position: absolute;
  right: 0;
}

.game-date {
  border-bottom: 1px solid white;
}

.modal-body {
  scrollbar-color: rgba(255, 255, 255, 0.1) rgba(255, 255, 255, 0.1);
  scrollbar-width: thin;
}

/* !Game History */
</style>
