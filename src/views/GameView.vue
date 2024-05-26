<script setup>
import { ref, onMounted } from 'vue'
import ButtonComp from '../components/ButtonComp.vue'
import { store } from '@/store/store'
import GameComp from '../components/GameComp.vue'

// variables
const test = ref(false)
const testMode = ref(false)
const player1 = ref('player1')
const player2 = ref('player2')
const score = ref({
  player1: 0,
  player2: 0,
})

// functions

const handleFinishedMatch = async (player1, player2, score1, score2) => {
  // stop the game and show the winner
  console.log('GAME FINISHED')
  console.log(`p1: ${player1}, p2: ${player2}, s1: ${score1}, s2: ${score2}`)
  // send results
  if (store.userAuthorised) await sendTestData(player1, player2, score1, score2)
}

const sendTestData = async (player1, player2, score1, score2) => {
  const response = await fetch('http://127.0.0.1:8000/my-games/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${localStorage.getItem('access')}`,
    },
    body: JSON.stringify({
      // players: [player1, player2],
      // winner: score1 > score2 ? player1 : player2,
      // // played_on: '2023-05-20T14:28:23.382Z',
      // // details: 'Match details here.',
      // user_score: score1,
      // opponent_score: score2,
      //
      player1: player1,
      player2: player2,
      score1: score1,
      score2: score2,
      winner: score1 > score2 ? player1 : player2,
    }),
  })

  const data = await response.json()
  console.log(data)
  if (!response.ok) {
    console.log('error: ' + data.error)
  }
}
</script>

<template>
  <section
    class="container flex-grow-1 d-flex flex-column justify-content-center align-items-center"
  >
    <!-- TEST -->
    <ButtonComp v-if="test" @click="testMode = !testMode" class="mb-3"
      >test mode</ButtonComp
    >
    <div v-if="testMode" class="row test-form py-2">
      <div class="col d-flex">
        <div
          class="d-flex flex-column justify-content-center align-items-center"
        >
          <label class="text-white roboto-regular fs-6" for="player1">{{
            player1
          }}</label>
          <input
            v-model="score.player1"
            class="text-center"
            type="text"
            id="player1"
            :placeholder="player1"
          />
        </div>
        <div
          class="d-flex flex-column justify-content-center align-items-center"
        >
          <label class="text-white roboto-regular fs-6" for="player2">{{
            player2
          }}</label>
          <input
            v-model="score.player2"
            class="ms-2 text-center"
            type="text"
            id="player2"
            :placeholder="player2"
          />
        </div>
        <ButtonComp @click="sendTestData" class="ms-2">send</ButtonComp>
      </div>
    </div>
    <GameComp
      @results="
        (player1, player2, score1, score2) =>
          handleFinishedMatch(player1, player2, score1, score2)
      "
      :isTournament="false"
      :player1="store.userAuthorised ? store.username : 'player1'"
      player2="player2"
    />
    <!-- <button
      class="btn btn-primary rounded-5 mt-3 d-flex justify-content-center align-items-center fs-1"
      style="width: 64px; height: 64px"
      data-bs-toggle="modal"
      data-bs-target="#helpModal"
    >
      ?
    </button> -->

    <!-- Modal -->
    <!-- <div
      class="modal fade"
      id="helpModal"
      tabindex="-1"
      aria-labelledby="helpModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="helpModalLabel">Modal title</h1>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">...</div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
              Close
            </button>
            <button type="button" class="btn btn-primary">Save changes</button>
          </div>
        </div>
      </div>
    </div> -->
  </section>
</template>

<style scoped>
.canvas {
  @media screen and (max-width: 600px) {
    border: 2px solid #f58562;
    border-left: none;
    border-right: none;
  }
  width: 80%;
  border: 5px solid #f58562;
  border-right: none;
  border-left: none;
}

/* .btn-primary {
  --bs-btn-active-color: #f58562;
  --bs-btn-active-bg: rgba(255, 255, 255, 0.1);
  background-color: var(--bs-btn-active-bg);
  border: none;
  box-shadow: -6px 6px 6px 0px rgba(0, 0, 0, 0.25);
  font-weight: 700;
  font-family: 'Roboto', sans-serif;
  transition: all 0.2s ease;
}
.btn-primary:hover,
.btn-primary:active {
  color: #f58562;
  background-color: rgba(255, 255, 255, 0.1);
  transform: translate(2px, -2px);
  box-shadow: -8px 8px 8px 0px rgba(0, 0, 0, 0.25);
}

.btn-primary:disabled {
  --bs-btn-active-color: rgba(255, 255, 255, 0.5);
  --bs-btn-active-bg: rgba(255, 255, 255, 0.07);
  position: relative;
  color: var(--bs-btn-active-color);
  background-color: var(--bs-btn-active-bg);
  pointer-events: all;
}
.btn-primary:hover:disabled {
  transform: none;
  box-shadow: -6px 6px 6px 0px rgba(0, 0, 0, 0.25);
} */

/* test */
.test-form {
  border-bottom: 1px solid #f58562;
  border-top: 1px solid #f58562;
}
</style>
