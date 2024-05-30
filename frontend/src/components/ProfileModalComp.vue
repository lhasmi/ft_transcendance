<script setup>
import { ref, onMounted } from 'vue'
import ButtonComp from './ButtonComp.vue'
import { store } from '../store/store.js'
import { getText } from '../language/language.js'
import { fetchWithJWT, fetchWithJWTJson } from '../utils/utils.js'

// test data
let data = {
  username: '',
  email: '',
  picture: '',
  gamesHistory: [],
}

// variables
const editProfile = ref(false)
const gamesHistory = ref(false)
const title = ref('profile')
const loader = ref(true)
const newUsername = ref('')
const newEmail = ref('')
const newPicture = ref(null)
const newPassword = ref('')
const newPassword2 = ref('')
const errorMsg = ref('')
const otpCode = ref('')

// functions
const loadData = async () => {
  loader.value = true
  try {
    console.log('fetch profile')
    const response = await fetchWithJWT('/api/update-profile/')
    const newData = await response.json()
    console.log(newData)
    if (!response.ok) {
      errorMsg.value = `${response.status}: ${response.statusText}`
    } else {
      data.username = newData.user.username
      data.email = newData.user.email
      data.picture = '/api' + newData.profile_picture
      errorMsg.value = ''
    }
  } catch {
    console.log('fetch error')
    errorMsg.value = 'fetch request failed'
  }
  // fetch games history
  // if (errorMsg.value != '') {
  //   console.log('CLEAR')
  //   loader.value = false
  //   store.userAuthorised = false
  //   store.username = ''
  //   store.email = ''
  //   store.picture = ''
  //   store.lang = 'en'
  //   localStorage.removeItem('access')
  //   localStorage.removeItem('refresh')
  //   return
  // }

  try {
    console.log('fetch games history')
    const response = await fetchWithJWT(
      '/api/my-matches-history/'
    )
    const newData = await response.json()
    if (!response.ok) {
      console.log('fetch games history error: ' + newData.error)
      errorMsg.value = newData.error
    } else {
      console.log(newData)
      data.gamesHistory = newData
    }
  } catch {
    console.log('fetch error')
    errorMsg.value = 'fetch request failed'
  }
  loader.value = false
}

const saveChanges = async (e) => {
  e.preventDefault()
  const formData = new FormData()

  if (
    !newUsername.value &&
    !newEmail.value &&
    !newPassword.value &&
    !newPicture.value
  ) {
    errorMsg.value = 'no changes'
    return
  }

  if (newUsername.value && newUsername.value === data.username) {
    errorMsg.value = 'new username is same as old'
    return
  }
  if (newEmail.value && newEmail.value === data.email) {
    errorMsg.value = 'new email is same as old'
    return
  }
  if (newPassword.value && newPassword.value !== newPassword2.value) {
    errorMsg.value = "passwords don't match"
    return
  }

  if (newUsername.value) formData.append('username', newUsername.value)
  if (newEmail.value) formData.append('email', newEmail.value)
  if (newPassword.value) formData.append('password', newPassword.value)
  if (newPicture.value)
    formData.append('profile_picture', newPicture.value, newPicture.value.name)

  errorMsg.value = ''

  try {
    const response = await fetchWithJWT(
      '/api/update-profile/',
      'PUT',
      formData
    )
    const newData = await response.json()
    console.log(newData)
    if (!response.ok) {
      errorMsg.value = newData.error
      console.log(newData.error + '!!!')
      return
    } else {
      console.log('profile updated')
    }
  } catch {
    console.log('fetch request failed')
    errorMsg.value = 'fetch request failed'
  }
  loadData()
  backProfileModal()
}

const resetInput = () => {
  newUsername.value = ''
  newEmail.value = ''
  newPassword.value = ''
  newPassword2.value = ''
  newPicture.value = null
  errorMsg.value = null
}

const toEditProfile = () => {
  editProfile.value = true
  title.value = 'editProfile'
}

const toGamesHistory = () => {
  gamesHistory.value = true
  title.value = 'gamesHistory'
}

const backProfileModal = () => {
  title.value = 'profile'
  editProfile.value = false
  gamesHistory.value = false
  resetInput()
}

const shortEmail = (email) => {
  const atSignPos = email.search('@')
  let first
  if (atSignPos >= 10) {
    first = email.substring(0, 8) + '...'
  } else {
    return email
  }
  return first + email.substring(atSignPos)
}

const getCircleColor = (index) => { // TO BE REMOVED?
  if (index >= data.gamesHistory.length)
    return 'background: rgba(255, 255, 255, 0.1)'
  return data.gamesHistory[index].score1 > data.gamesHistory[index].score2
    ? 'background: #66bf6a'
    : 'background: #da4834'
}

const changePicture = (e) => {
  console.log(e.target.files[0])
  console.log(URL.createObjectURL(e.target.files[0]))
  document.getElementById('profile_img').src = URL.createObjectURL(
    e.target.files[0]
  )
  newPicture.value = e.target.files[0]
}

// 2024-05-24T23:48:49.479760
const formatDateTime = (dateTime) => {
  let date = dateTime.slice(0, dateTime.indexOf('T'))
  let time = dateTime.slice(dateTime.indexOf('T') + 1, dateTime.indexOf('.'))
  return `${date} | ${time}`
}

const getWonAmount = () => {
  if (data.gamesHistory.length == 0) return 0
  let counter = 0
  for (let i in data.gamesHistory) {
    if (data.gamesHistory[i].winner == data.username) counter++
  }
  return counter
}

const getLostAmount = () => {
  if (data.gamesHistory.length == 0) return 0
  let counter = 0
  for (let i in data.gamesHistory) {
    if (data.gamesHistory[i].winner != data.username) counter++
  }
  return counter
}

const enable2FA = async () => {
  console.log('enable2FA')
  try {
    const response = await fetchWithJWT('/api/enable-2fa/', 'POST')
    if (!response.ok) {
      console.log('enable 2FA error: ')
      console.log(response)
    } else {
      const data = await response.json()
      console.log('enable 2FA success: ')
      console.log(data)
    }
  } catch (error) {
    console.log('enable 2FA fetch error: ' + error)
  }
}

const verifyOTP = async () => {
  console.log('verify-otp')
	console.log("username: " + store.username)
	console.log("otp code: " + otpCode.value)
  try {
    const response = await fetchWithJWTJson('/api/verify-otp/', 'POST', {
			username: store.username,
			otp: otpCode.value
		})
    if (!response.ok) {
      console.log('verify-otp error: ')
      console.log(response)
    } else {
      const data = await response.json()
      console.log('verify-otp success: ')
      console.log(data)
    }
  } catch (error) {
    console.log('verify-otp fetch error: ' + error)
  }
}

onMounted(() => {
  const profileModal = document.getElementById('profileModal')
  profileModal.addEventListener('show.bs.modal', (e) => {
    loadData()
  })
  profileModal.addEventListener('hidden.bs.modal', (e) => {
    loader.value = true
    backProfileModal()
    // abort fetch if its still ongoing
  })
})
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
              v-if="editProfile || gamesHistory"
              @click="backProfileModal"
              type="button"
              class="icon-back"
            >
              <span class="material-symbols-outlined" style="font-size: 2.5rem">
                keyboard_backspace
              </span>
            </button>

            <h1
              class="modal-title fs-3 my-2 mx-auto roboto-bold"
              style="color: #f58562"
              id="profileModalLabel"
            >
              {{ getText(title, store.lang) }}
            </h1>
            <button
              @click="backProfileModal"
              type="button"
              class="icon-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            >
              <span class="material-symbols-outlined" style="font-size: 2rem">
                close
              </span>
            </button>
          </div>
          <hr class="splitter col-12 mx-auto m-0 mb-2" />
        </div>

        <!-- SPINNER -->
        <div v-if="loader" class="modal-body p-0 d-flex justify-content-center">
          <div class="spinner-border text-white my-5" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
        <!-- EDIT PROFILE -->
        <div v-else-if="editProfile" class="modal-body p-0 d-flex flex-column">
          <div class="d-flex mb-2">
            <img
              :src="data.picture"
              alt="profile image"
              id="profile_img"
              class="profile-img my-2 mx-auto rounded-4"
            />
            <!--             
						<img
              src="../assets/profile_img.png"
              alt="profile image"
              id="profile_img"
              class="profile-img my-2 mx-auto rounded-4"
            />
						 -->
          </div>
          <form action="">
            <div
              class="d-flex col-9 col-md-7 mx-auto align-items-center mb-2 mb-md-3"
            >
              <label for="picture" class="roboto-bold text-white fs-6"
                >{{ getText('picture', store.lang) }}:</label
              >
              <input
                @change="changePicture"
                class="picture-input text-white roboto-regular fs-6 ms-2"
                type="file"
                id="picture"
                accept="image/*"
              />
            </div>
            <div
              class="d-flex col-9 col-md-7 mx-auto align-items-center mb-2 mb-md-3"
            >
              <label for="username" class="roboto-bold text-white fs-6"
                >{{ getText('username', store.lang) }}:</label
              >
              <input
                v-model="newUsername"
                class="text-input text-white roboto-regular fs-6 ms-2"
                type="text"
                id="username"
                :placeholder="data.username"
              />
            </div>
            <div
              class="d-flex col-9 col-md-7 mx-auto align-items-center mb-2 mb-md-3"
            >
              <label for="email" class="roboto-bold text-white fs-6"
                >{{ getText('email', store.lang) }}:</label
              >
              <input
                v-model="newEmail"
                class="text-input text-white roboto-regular fs-6 ms-2"
                type="email"
                id="email"
                :placeholder="data.email"
              />
            </div>
            <div
              class="d-flex col-9 col-md-7 mx-auto align-items-center mb-2 mb-md-3"
            >
              <label for="password" class="roboto-bold text-white fs-6"
                >{{ getText('password', store.lang) }}:</label
              >
              <input
                v-model="newPassword"
                class="text-input text-white roboto-regular fs-6 ms-2"
                type="password"
                id="password"
              />
            </div>
            <div
              class="d-flex col-9 col-md-7 mx-auto align-items-center mb-3 mb-md-4"
            >
              <label for="passwordRepeat" class="roboto-bold text-white fs-6"
                >{{ getText('password', store.lang) }}:</label
              >
              <input
                v-model="newPassword2"
                class="text-input text-white roboto-regular fs-6 ms-2"
                type="password"
                id="passwordRepeat"
              />
            </div>
            <div
              v-if="errorMsg"
              class="my-1 fs-6 roboto-bold text-center"
              style="color: #da4834"
            >
              {{ errorMsg }}
            </div>
            <div
              class="d-flex col-9 col-md-7 mx-auto justify-content-around my-4"
            >
              <ButtonComp @click="saveChanges" class="save-btn fs-6">{{
                getText('saveChanges', store.lang)
              }}</ButtonComp>
              <!-- <ButtonComp @click="backProfileModal" class="cancel-btn fs-6">{{ getText('cancel', store.lang) }}</ButtonComp> -->
            </div>
          </form>
        </div>

        <!-- GAME HISTORY -->
        <div
          v-else-if="gamesHistory"
          class="modal-body p-0 d-flex flex-column mb-3"
          style="height: 396px"
        >
          <div
            v-if="data.gamesHistory.length == 0"
            class="text-center text-white roboto-regular mt-4"
          >
            games history is empty...
          </div>
          <div
            class="col-9 col-md-7 mx-auto mb-1"
            v-for="item in data.gamesHistory.slice().reverse()"
            :key="item.played_on"
          >
            <p class="game-date text-center text-white roboto-regular mb-1">
              {{ formatDateTime(item.played_on) }}
            </p>
            <div class="d-flex justify-content-center position-relative">
              <p class="player-left text-white roboto-regular fs-5">
                {{ item.player1 }}
              </p>
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
              <p class="player-right text-white roboto-regular fs-5">
                {{ item.player2 }}
              </p>
            </div>
          </div>
        </div>

        <!-- PROFILE -->
        <div v-else class="modal-body p-0 d-flex flex-column">
          <div class="d-flex">
            <img
              v-if="!data.picture"
              src="../assets/profile_img.png"
              alt="profile image"
              class="profile-img my-2 mx-auto rounded-4"
            />
            <img
              v-else
              :src="data.picture"
              alt="profile image"
              class="profile-img my-2 mx-auto rounded-4"
            />
          </div>
          <p
            class="col-9 col-md-7 mx-auto roboto-bold mb-2 mb-md-3 text-white fs-6"
          >
            {{ getText('username', store.lang) }}:
            <span class="fs-6 ms-1">{{ data.username }}</span>
          </p>
          <p
            class="col-9 col-md-7 mx-auto roboto-bold mb-2 mb-md-3 text-white fs-6"
          >
            {{ getText('email', store.lang) }}:
            <span class="fs-6 ms-1">{{ shortEmail(data.email) }}</span>
          </p>
          <ButtonComp
            @click="toEditProfile"
            class="fs-6 col-9 col-md-7 mx-auto mb-3"
          >
            {{ getText('editProfile', store.lang) }}
          </ButtonComp>
          <ButtonComp
            @click="enable2FA"
            class="fs-6 col-9 col-md-7 mx-auto mb-3"
          >
            enable 2FA
          </ButtonComp>
					<div class="col-9 col-md-7 mx-auto d-flex mb-3">
						<input
									v-model="otpCode"
									class="text-input text-white text-center roboto-regular fs-6 me-3"
									type="text"
									id="otpCode"
									placeholder="otp code"
								/>
						<ButtonComp
							@click="verifyOTP"
							class="fs-6 col-9 col-md-7 mx-auto"
							style="width: 120px;"
						>
							send OTP
						</ButtonComp>
					</div>
          <hr class="splitter col-12 mx-auto m-0" />
          <div
            class="col-9 col-md-7 d-flex justify-content-around my-3 mx-auto roboto-bold mb-2 mb-md-3 text-white"
          >
            <div class="fs-4 roboto-bold" style="color: #f58562">
              won
              <p class="text-center text-white m-0">{{ getWonAmount() }}</p>
            </div>
            <div
              style="
                border-right: 1px solid #f58562;
                border-left: 2px solid #f58562;
              "
            ></div>
            <div class="fs-4 roboto-bold" style="color: #f58562">
              lost
              <p class="text-center text-white m-0">{{ getLostAmount() }}</p>
            </div>
          </div>

          <!-- <h2 class="fs-3 my-3 mx-auto roboto-bold" style="color: #f58562">
            {{ getText('lastGames', store.lang) }}
          </h2> -->
          <!-- <div
            class="last_games_circles d-flex col-9 col-md-7 mx-auto justify-content-around mb-3"
          >
            <div class="circle" :style="getCircleColor(4)"></div>
            <div class="circle" :style="getCircleColor(3)"></div>
            <div class="circle" :style="getCircleColor(2)"></div>
            <div class="circle" :style="getCircleColor(1)"></div>
            <div class="circle" :style="getCircleColor(0)"></div>
          </div> -->
          <ButtonComp
            @click="toGamesHistory"
            class="fs-6 col-9 col-md-7 mx-auto mb-4"
          >
            {{ getText('gamesHistory', store.lang) }}
          </ButtonComp>
          <div
            v-if="errorMsg"
            class="mt-1 mb-3 fs-6 roboto-bold text-center"
            style="color: #da4834"
          >
            {{ errorMsg }}
          </div>
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
  background: linear-gradient(
    145deg,
    rgba(60, 26, 153, 0.9) 23%,
    55%,
    rgba(92, 42, 132, 0.9) 85%
  );
  backdrop-filter: blur(2px);
}

.profile-img {
  border: solid 3px #f58562;
  height: 80px;
  width: 80px;
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
