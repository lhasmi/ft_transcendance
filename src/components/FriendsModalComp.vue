<script setup>
import { ref, onMounted } from 'vue'
import { store } from '../store/store.js'
import { getText } from '../language/language.js'
import ButtonComp from './ButtonComp.vue'
import FriendProfileComp from './FriendProfileComp.vue'

// test data
let data = {
  friends: [
    { id: 1, username: 'friend1', status: 'online' },
    { id: 2, username: 'friend2', status: 'online' },
    { id: 3, username: 'friend3', status: 'offline' },
    { id: 4, username: 'friend4', status: 'online' },
    { id: 5, username: 'friend5', status: 'offline' }
  ]
}

let friendData = {
	id: 1,
	username: 'friend1',
	status: 'online',
	picture: '',
	gamesHistory: [
		{
      id: 3,
      player1: 'friend1',
      player2: 'test2',
      score1: 6,
      score2: 7,
      date: '11.04.2024 14:35'
    },
		{
      id: 2,
      player1: 'friend1',
      player2: 'test1',
      score1: 7,
      score2: 2,
      date: '11.04.2024 14:35'
    },
		{
      id: 1,
      player1: 'friend1',
      player2: 'test3',
      score1: 3,
      score2: 7,
      date: '11.04.2024 14:35'
    }
	],
}


// variables
const loader = ref(true)
const friendToAdd = ref('')
const friendProfile = ref(false)
const title = ref('friends')
const errorMsg = ref('')

// funcions
const loadFriends = async () => {
	loader.value = true
	try {
		const response = await fetch('127.0.0.1:8000/friends')
		const data = await response.json()
		console.log(data)
		if (!response.ok) {
			errorMsg.value = data.error
		}
	} catch {
		errorMsg.value = 'fetch request failed'
	}
	setTimeout(() => { // test
		loader.value = false
	}, 1000);
}

const loadFriend = async (id) => {
	loader.value = true
	// try {
	// 	const response = await fetch(`127.0.0.1:8000/friend/${id}`)
	// 	const data = await response.json()
	// 	console.log(data)
	// 	if (!response.ok) {
	// 		errorMsg.value = data.error
	// 	}
	// } catch {
	// 	errorMsg.value = 'fetch request failed'
	// }
	// loader.value = false

	setTimeout(() => { // test
		loader.value = false
	}, 1000)
}

const addFriend = async () => {
	// send "post" request to try to add a new friend
	// on success fetch new friends list to rerender it
}

const getStatusColor = (status) => {
  if (status === 'online') return 'background: #66bf6a'
  else return 'background: rgba(255, 255, 255, 0.1)'
}

const toFriendProfile = (friendItem) => {
	loadFriend(friendItem.id)
  title.value = friendItem.username
	friendProfile.value = true

}

const backFriendsModal = () => {
  title.value = 'friends'
	friendProfile.value = false
}

onMounted(() => {
	const friendsModal = document.getElementById('friendsModal')
	friendsModal.addEventListener('show.bs.modal', e => {
		loadFriends()
	})
	friendsModal.addEventListener('hidden.bs.modal', e => {
		loader.value = true
		backFriendsModal()
		// abort fetch if its still ongoing
	})
})

</script>

<template>
  <div
    class="modal fade"
    id="friendsModal"
    tabindex="-1"
    aria-labelledby="friendsModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-scrollable modal-dialog-centered">
      <div class="friends-modal modal-content myshadow border-0 rounded-4">
        <div class="modal-header border-0 d-flex flex-column m-0 p-0">
          <div class="d-flex position-relative w-100">
						<button
              v-if="friendProfile"
              @click="backFriendsModal"
              type="button"
              class="icon-back"
            >
              <span class="material-symbols-outlined" style="font-size: 2.5rem">
                keyboard_backspace
              </span>
            </button>

            <h1
              class="friends-modal-title modal-title fs-3 my-2 mx-auto roboto-bold"
              id="friendsModalLabel"
            >
              {{ friendProfile ? title : getText('friends', store.lang) }}
            </h1>
            <button type="button" class="icon-close" data-bs-dismiss="modal" aria-label="Close">
              <span class="material-symbols-outlined" style="font-size: 2rem"> close </span>
            </button>
          </div>
          <hr class="splitter col-9 mx-auto m-0 mb-2" />
        </div>

				<!-- SPINNER -->
				<div v-if="loader" class="modal-body p-0 d-flex justify-content-center">
					<div class="spinner-border text-white my-5" role="status">
  					<span class="visually-hidden">Loading...</span>
					</div>
				</div>

				<!-- FRIEND PROFILE -->
				<FriendProfileComp v-else-if="friendProfile" :data="friendData"/>

				<!-- FRIENDS -->
        <div v-else class="modal-body p-0 d-flex flex-column" style="max-height: 396px">
					<div v-if="data.friends.length === 0" class="col-9 col-md-7 mx-auto text-white text-center roboto-regular my-4">
						{{ getText('friendsListEmpty', store.lang) }}
					</div>
          <button
						class="friend-item col-9 col-md-7 mx-auto d-flex justify-content-center my-2"
						v-for="item in data.friends"
						:key="item.id"
						@click="toFriendProfile(item)"
          >
            <p class="friend-item-name roboto-regular fs-5 mb-0">{{ item.username }}</p>
            <div class="friend-status ms-3 my-auto" :style="getStatusColor(item.status)"></div>
				</button>
        </div>
				<div v-if="!loader && !friendProfile" class="modal-footer">
					<hr class="splitter col-9 mx-auto m-0 mb-2" />	
					<div class="col-9 col-md-7 mx-auto d-flex flex-column">
						<label class="roboto-bold fs-5 text-center mb-1" style="color: #f58562" for="addFriend">{{ getText('addFriend', store.lang) }}</label>
						<input v-model="friendToAdd" class="text-input text-white roboto-regular fs-6 p-0 mb-3 text-center" type="text" id="addFriend" :placeholder="getText('username', store.lang)"/>
						<ButtonComp class="">{{ getText('add', store.lang) }}</ButtonComp>
					</div>
      	</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-body {
  scrollbar-color: rgba(255, 255, 255, 0.1) rgba(255, 255, 255, 0.1);
  scrollbar-width: thin;
}

.myshadow {
  box-shadow: -6px 6px 6px 0px rgba(0, 0, 0, 0.25);
}

.friends-modal {
  background: linear-gradient(145deg, rgba(60, 26, 153, 0.9) 23%, 55%, rgba(92, 42, 132, 0.9) 85%);
  backdrop-filter: blur(2px);
}

.friends-modal-title {
  color: #f58562;
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

.friend-item-name {
  color: white;
}

.friend-item {
	background: none;
	border: none;
  border-top: 2px solid white;
  border-bottom: 2px solid white;
  transition: all 0.2s ease;
}
.friend-item:hover {
  border-color: #f58562;
}
.friend-item:hover .friend-item-name {
  color: #f58562;
}

.friend-status {
  height: 16px;
  width: 16px;
  border-radius: 50%;
}

.modal-footer {
	border: none;
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
</style>
