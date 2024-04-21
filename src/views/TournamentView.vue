<script setup>
import { ref } from 'vue'
import ButtonComp from '../components/ButtonComp.vue'

// variables
const players = ref([])
const playersAmount = ref(0)
const tournamentRegistrationState = ref(false)
const tournamentGameState = ref(false)
const tournamentTableState = ref(false)
const errorMsg = ref('')
const upcomingMatches = ref([])

// functions
const toRegistrationState = (number) => {
	playersAmount.value = number
	tournamentRegistrationState.value = true
}

const toTableState = () => {
	if (!validateInput()) return
	tournamentTableState.value = true
	tournamentGameState.value = false
	tournamentRegistrationState.value = false

	generateUpcomingMatches()
}

const generateUpcomingMatches = () => {
	const playersCopy = players.value.slice(0)
	let randomPick
	while (playersCopy.length) {
		let pair = []
		randomPick = Math.floor(Math.random() * playersCopy.length)
		pair[0] = playersCopy[randomPick]
		playersCopy.splice(randomPick, 1)
		randomPick = Math.floor(Math.random() * playersCopy.length)
		pair[1] = playersCopy[randomPick]
		playersCopy.splice(randomPick, 1)
		upcomingMatches.value.push(pair)
	}
	console.log(upcomingMatches.value)
}

const validateInput = () => {
	for (let i = 0; i < playersAmount.value; i++) {
		if (!players.value[i]) {
			errorMsg.value = `${i + 1} is empty`
			return false
		}
	}
	for (let i = 0; i < playersAmount.value - 1; i++) {
		for (let k = i + 1; k < playersAmount.value; k++) {
			if (players.value[i] === players.value[k]) {
				errorMsg.value = `${i + 1} and ${k + 1} are the same`
				return false
			}
		}
	}
	errorMsg.value = ''
	return true
}

</script>

<template>
	<div class="container d-flex flex-grow-1 justify-content-center align-items-center ">
		<!-- TOURNAMENT REGISTRATION -->
		<div v-if="tournamentRegistrationState" class="myshadow bg-white bg-opacity-10 col-11 col-sm-10 col-md-8 col-lg-6 rounded-4">
			<p class="m-0 mt-3 mb-2 fs-3 roboto-bold text-center" style="color:#f58562">tournament registration</p>
			<hr class="splitter col-12 mx-auto m-0 mb-4" />
			<div v-for="n in playersAmount / 2" :key="n" class="row">
				<div class="col-sm-6 text-center">
					<span class="roboto-bold fs-5" style="color: #f58562;">{{ n+(n-1) }}.</span>
					<input v-model="players[n+(n-1)-1]" class="text-input text-white roboto-regular fs-6 p-0 mb-3 text-center" type="text" :id="n+(n-1)"/>
				</div>
				<div class="col-sm-6 text-center">
					<span class="roboto-bold fs-5" style="color: #f58562;">{{ n+(n-1)+1 }}.</span>
					<input v-model="players[n+(n-1)]" class="text-input text-white roboto-regular fs-6 p-0 mb-3 text-center" type="text" :id="n+(n-1)+1"/>
				</div>
			</div>
			<div v-if="errorMsg" class="error-msg my-1 fs-6 roboto-bold text-center" style="color: #da4834;">{{ errorMsg }}</div>
			<ButtonComp @click="toTableState" class="btn-lg mt-3 mb-4 fs-5 d-flex justify-content-center mx-auto col-6 col-lg-4">ready</ButtonComp>
		</div>
		<!-- TOURNAMENT TABLE -->
		<div class="myshadow bg-white bg-opacity-10 col-11 col-sm-8 col-md-6 col-lg-4 rounded-4" v-else-if="tournamentTableState">
			<p class="m-0 mt-3 mb-2 fs-3 roboto-bold text-center" style="color:#f58562">upcoming matches</p>
			<hr class="splitter col-12 mx-auto m-0 mb-4" />
			<div v-for="match in upcomingMatches" :key="match[0]">
				<p class="fs-4 text-white text-center roboto-bold">{{ match[0] }} <span style="color: #f58562;">vs</span> {{ match[1] }}</p>
			</div>
			<ButtonComp class="btn-lg mt-3 mb-4 fs-5 d-flex justify-content-center mx-auto col-7 col-lg-5">start</ButtonComp>
		</div>

		<!-- TOURNAMENT GAME -->
		<div v-else-if="tournamentGameState">tournament game</div>

		<!-- CHOOSE AMOUNT OF PLAYERS -->
		<div v-else class="myshadow bg-white bg-opacity-10 col-11 col-sm-9 col-md-7 col-lg-5 col-xl-4 rounded-4 d-flex flex-column align-items-center">
			<p class="fs-3 m-0 mt-3 mb-2 roboto-bold text-center" style="color: #f58562;">choose amount of players</p>
			<hr class="splitter col-12 mx-auto m-0 mb-4" />
			<div class="mb-4 d-flex">
				<ButtonComp @click="toRegistrationState(4)" class="btn-lg fs-3 me-4">4 players</ButtonComp>
				<ButtonComp @click="toRegistrationState(8)" class="btn-lg fs-3 ms-4">8 players</ButtonComp>
			</div>
		</div>
	</div>

</template>

<style scoped>
.myshadow {
  box-shadow: -6px 6px 6px 0px rgba(0, 0, 0, 0.25);
}

.prompt-container {
	background: rgba(255, 255, 255, 0.1);
}

.splitter {
  color: transparent;
  border-bottom: 3px solid #f58562;
  opacity: 1;
}

input {
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

.numeric {
  border-bottom: solid 2px #f58562;
}

</style>