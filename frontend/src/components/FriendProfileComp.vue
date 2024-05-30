<script setup>
import { store } from '../store/store.js'
import { getText } from '../language/language.js'
import { onMounted } from 'vue'

const props = defineProps({
  data: Object,
  games: Object,
})

const picture = `api${props.data.profile_picture}`

// variables

// functions
const getStatusColor = (status) => {
  if (status == true) return 'background: #66bf6a'
  else return 'background: rgba(255, 255, 255, 0.1)'
}

const getCircleColor = (index) => {
  if (index >= props.data.gamesHistory.length)
    return 'background: rgba(255, 255, 255, 0.1)'
  return props.data.gamesHistory[index].score1 >
    props.data.gamesHistory[index].score2
    ? 'background: #66bf6a'
    : 'background: #da4834'
}

// 2024-05-24T23:48:49.479760
const formatDateTime = (dateTime) => {
  let date = dateTime.slice(0, dateTime.indexOf('T'))
  let time = dateTime.slice(dateTime.indexOf('T') + 1, dateTime.indexOf('.'))
  return `${date} | ${time}`
}

const getWonAmount = () => {
  if (!props.games || props.games.length == 0) return 0
  let counter = 0
  for (let i in props.games) {
    if (props.games[i].winner == props.data.user.username) counter++
  }
  return counter
}

const getLostAmount = () => {
  if (!props.games || props.games.length == 0) return 0
  let counter = 0
  for (let i in props.games) {
    if (props.games[i].winner != props.data.user.username) counter++
  }
  return counter
}

onMounted(() => {
  console.log('PROPS:')
  console.log(props.data)
  console.log(props.games)
})
</script>

<template>
  <div class="modal-body p-0 d-flex flex-column" style="height: 396px">
    <div class="d-flex">
      <img
        :src="picture"
        alt="profile image"
        class="profile-img my-2 mx-auto rounded-4"
      />
    </div>
    <p class="col-9 col-md-7 mx-auto roboto-bold mb-2 mb-md-3 text-white fs-6">
      {{ getText('username', store.lang) }}:
      <span class="fs-6 ms-1">{{ props.data.user.username }}</span>
    </p>
    <div
      class="col-9 col-md-7 mx-auto roboto-bold mb-2 mb-md-3 text-white fs-6 d-flex"
    >
      {{ getText('status', store.lang) }}:
      <span class="fs-6 ms-1">{{
        getText(props.data.online_status ? 'online' : 'offline', store.lang)
      }}</span>
      <div
        class="friend-status ms-2 my-auto"
        :style="getStatusColor(props.data.online_status)"
      ></div>
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
        style="border-right: 1px solid #f58562; border-left: 2px solid #f58562"
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
    <hr class="splitter col-12 mx-auto m-0 mt-3" />
    <h2 class="fs-3 my-3 mx-auto roboto-bold" style="color: #f58562">
      {{ getText('gamesHistory', store.lang) }}
    </h2>
    <div
      v-if="!props.games || props.games.length == 0"
      class="text-center text-white roboto-regular mt-1 mb-4"
    >
      games history is empty...
    </div>
    <div
      class="col-9 col-md-7 mx-auto mb-1"
      v-for="item in props.games.slice().reverse()"
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
</template>

<style scoped>
.profile-img {
  border: solid 3px #f58562;
  height: 80px;
  width: 80px;
}

.friend-status {
  height: 16px;
  width: 16px;
  border-radius: 50%;
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
</style>
