<script setup>
import { ref, onMounted, watch } from 'vue'
import { store } from '../store/store.js'
import { getText } from '../language/language.js'
import ButtonComp from '../components/ButtonComp.vue'
import TournamentTestComp from '../components/TournamentTestComp.vue'
import GameComp from '@/components/GameComp.vue'

// variables
const players = ref([])
const playersAmount = ref(0)
const tournamentState = ref('')
const errorMsg = ref('')
const upcomingMatches = ref([])

const states = Object.freeze({
  registration: 'registrationState',
  table: 'tableState',
  game: 'gameState',
  end: 'endState',
})

// functions
const toRegistrationState = (number) => {
  playersAmount.value = number
  tournamentState.value = states.registration
}

const toTableState = () => {
  if (!validateInput()) return
  if (upcomingMatches.value.length === 0 && players.value.length > 1)
    generateUpcomingMatches()

  tournamentState.value = states.table
}

const toGameState = () => {
  tournamentState.value = states.game
}

const handleFinishedMatch = (winner, loser) => {
  console.log(winner + ' won')
  console.log(loser + ' lost')
  upcomingMatches.value.shift()
  players.value.splice(players.value.indexOf(loser), 1)
  playersAmount.value--

  if (playersAmount.value > 1) toTableState()
  else tournamentState.value = states.end
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
      errorMsg.value = `${i + 1} ${getText('isEmpty', store.lang)}`
      return false
    }
  }
  for (let i = 0; i < playersAmount.value - 1; i++) {
    for (let k = i + 1; k < playersAmount.value; k++) {
      if (players.value[i] === players.value[k]) {
        errorMsg.value = `${i + 1} ${getText('and', store.lang)} ${k + 1} ${getText('areSame', store.lang)}`
        return false
      }
    }
  }
  errorMsg.value = ''
  return true
}

watch(store, () => {
  players.value[0] = store.username
})

onMounted(() => {
  if (store.userAuthorised) players.value[0] = store.username
})
</script>

<template>
  <div
    class="container d-flex flex-grow-1 justify-content-center align-items-center"
  >
    <!-- TOURNAMENT REGISTRATION -->
    <div
      v-if="tournamentState === states.registration"
      class="myshadow bg-white bg-opacity-10 col-11 col-sm-10 col-md-8 col-lg-6 rounded-4"
    >
      <p
        class="m-0 mt-3 mb-2 fs-3 roboto-bold text-center"
        style="color: #f58562"
      >
        {{ getText('tournamentRegistration', store.lang) }}
      </p>
      <hr class="splitter col-12 mx-auto m-0 mb-4" />
      <div v-for="n in playersAmount / 2" :key="n" class="row">
        <div class="col-sm-6 text-center">
          <span class="roboto-bold fs-5" style="color: #f58562"
            >{{ n + (n - 1) }}.</span
          >
          <input
            v-model="players[n + (n - 1) - 1]"
            class="text-input text-white roboto-regular fs-6 p-0 mb-3 text-center"
            type="text"
            :id="n + (n - 1)"
          />
        </div>
        <div class="col-sm-6 text-center">
          <span class="roboto-bold fs-5" style="color: #f58562"
            >{{ n + (n - 1) + 1 }}.</span
          >
          <input
            v-model="players[n + (n - 1)]"
            class="text-input text-white roboto-regular fs-6 p-0 mb-3 text-center"
            type="text"
            :id="n + (n - 1) + 1"
          />
        </div>
      </div>
      <div
        v-if="errorMsg"
        class="error-msg my-1 fs-6 roboto-bold text-center"
        style="color: #da4834"
      >
        {{ errorMsg }}
      </div>
      <ButtonComp
        @click="toTableState"
        class="btn-lg mt-3 mb-4 fs-5 d-flex justify-content-center mx-auto col-6 col-lg-4"
        >{{ getText('ready', store.lang) }}</ButtonComp
      >
    </div>
    <!-- TOURNAMENT TABLE -->
    <div
      v-else-if="tournamentState === states.table"
      class="myshadow bg-white bg-opacity-10 col-11 col-sm-8 col-md-6 col-lg-4 rounded-4"
    >
      <p
        class="m-0 mt-3 mb-2 fs-3 roboto-bold text-center"
        style="color: #f58562"
      >
        {{ getText('upcomingMatches', store.lang) }}
      </p>
      <hr class="splitter col-12 mx-auto m-0 mb-4" />
      <div
        v-for="match in upcomingMatches"
        :key="match[0]"
        class="match-item col-11 col-sm-9 mx-auto"
      >
        <div class="row">
          <div
            class="col text-end roboto-bold fs-4 text-white my-2 text-break align-self-center"
          >
            {{ match[0] }}
          </div>
          <div
            class="col-2 text-center roboto-bold fs-4 my-2 align-self-center"
            style="color: #f58562"
          >
            vs
          </div>
          <div
            class="col text-start roboto-bold fs-4 text-white my-2 text-break align-self-center"
          >
            {{ match[1] }}
          </div>
        </div>
        <!-- <p class="fs-4 m-0 my-2 text-white text-center roboto-bold">{{ match[0] }} <span style="color: #f58562;">vs</span> {{ match[1] }}</p> -->
      </div>
      <ButtonComp
        @click="toGameState"
        class="btn-lg mt-3 mb-4 fs-5 d-flex justify-content-center mx-auto col-7 col-lg-5"
        >{{ getText('start', store.lang) }}</ButtonComp
      >
    </div>

    <!-- TOURNAMENT GAME -->
    <div v-else-if="tournamentState === states.game">
      <!-- <TournamentTestComp @winner="(winner, loser) => handleFinishedMatch(winner, loser)" :match="upcomingMatches[0]"/> -->
      <GameComp
        :is-tournament="true"
        @winner="(winner, loser) => handleFinishedMatch(winner, loser)"
        :player1="upcomingMatches[0][0]"
        :player2="upcomingMatches[0][1]"
      />
    </div>

    <div
      v-else-if="tournamentState === states.end"
      class="myshadow bg-white bg-opacity-10 col-11 col-sm-8 col-md-6 col-lg-4 rounded-4"
    >
      <p
        class="m-0 mt-3 mb-2 fs-3 roboto-bold text-center"
        style="color: #f58562"
      >
        {{ getText('tournamentFinished', store.lang) }}
      </p>
      <hr class="splitter col-12 mx-auto m-0 mb-4" />
      <p class="m-0 mb-4 roboto-bold fs-4 text-white text-center text-break">
        <span class="roboto-bold" style="color: #f58562">{{ players[0] }}</span>
        {{ getText('isWinner', store.lang) }}
      </p>
    </div>

    <!-- CHOOSE AMOUNT OF PLAYERS -->
    <div
      v-else
      class="myshadow bg-white bg-opacity-10 col-11 col-sm-9 col-md-7 col-lg-5 col-xl-4 rounded-4 d-flex flex-column align-items-center"
    >
      <p
        class="fs-3 m-0 mt-3 mb-2 roboto-bold text-center"
        style="color: #f58562"
      >
        {{ getText('chooseAmountPlayers', store.lang) }}
      </p>
      <hr class="splitter col-12 mx-auto m-0 mb-4" />
      <div class="mb-4 d-flex">
        <ButtonComp
          @click="toRegistrationState(4)"
          class="btn-lg fs-3 me-4"
          style="width: 100px"
          >4</ButtonComp
        >
        <ButtonComp
          @click="toRegistrationState(8)"
          class="btn-lg fs-3 ms-4"
          style="width: 100px"
          >8</ButtonComp
        >
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

.match-item {
  border-bottom: 2px solid white;
}
.match-item:last-of-type {
  border: none;
}
</style>
