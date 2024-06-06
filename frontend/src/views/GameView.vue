<script setup>
import { ref, onMounted } from 'vue'
import ButtonComp from '../components/ButtonComp.vue'
import { store } from '@/store/store'
import GameComp from '../components/GameComp.vue'
import { fetchWithJWTJson } from '@/utils/utils';

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
  // const response = await fetch(`${window.location.protocol}//${import.meta.env.VITE_APP_API_URL}/my-games/`, {
  //   method: 'POST',
  //   headers: {
  //     'Content-Type': 'application/json',
  //     Authorization: `Bearer ${localStorage.getItem('access')}`,
  //   },
  //   body: JSON.stringify({
  //     player1: player1,
  //     player2: player2,
  //     score1: score1,
  //     score2: score2,
  //     winner: score1 > score2 ? player1 : player2,
  //   }),
  // })
  const response = await fetchWithJWTJson(`${window.location.protocol}//${import.meta.env.VITE_APP_API_URL}/my-games/`, 'POST', {
      player1: player1,
      player2: player2,
      score1: score1,
      score2: score2,
      winner: score1 > score2 ? player1 : player2,
  })

  const data = await response.json()
  console.log(data)
  if (!response.ok) {
    console.log('error: ' + data.detail)
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
      :player2="store.userAuthorised ? 'opponent' : 'player2'"
    />
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

/* test */
.test-form {
  border-bottom: 1px solid #f58562;
  border-top: 1px solid #f58562;
}
</style>
