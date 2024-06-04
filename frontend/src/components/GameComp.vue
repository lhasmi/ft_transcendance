<script setup>
import { ref, onMounted } from 'vue'
import router from '@/router'
import { store } from '@/store/store'
import { getText } from '../language/language.js'
import HelpModalComp from './HelpModalComp.vue'
import ButtonComp from './ButtonComp.vue'

const props = defineProps({
  isTournament: Boolean,
  player1: String,
  player2: String,
})

const score = ref({
  player1: 0,
  player2: 0,
})

const gameStop = ref(false)
const gameStart = ref(true)

const emit = defineEmits(['winner', 'results'])

const emitResults = (player1, player2, score1, score2) => {
  emit('results', player1, player2, score1, score2)
}

const setWinner = (winner, loser) => {
  emit('winner', winner, loser)
}

// GAME
let canvas
let ctx
let player1, player2, game, ball
const playerWidth = 4
const playerHeight = 80
const playerSpeed = 3
const ballSpeed = 2
const maxScore = 3

class Player {
  constructor(x = 0, y = 0) {
    this.posX = x
    this.posY = y
    // movement velocity
    this.vy = 0
    // button released
    this.upKeyPressed = false
    this.downKeyPressed = false
    // color
    this.color = '#F58562'
  }
  draw() {
    ctx.fillStyle = this.color
    ctx.fillRect(this.posX, this.posY, playerWidth, playerHeight)
  }
  update() {
    if (this.upKeyPressed && this.downKeyPressed) this.vy = 0
    else if (this.upKeyPressed) this.vy = -playerSpeed
    else if (this.downKeyPressed) this.vy = playerSpeed
    else if (!this.upKeyPressed && !this.downKeyPressed) this.vy = 0
    // boundaries check
    if (this.posY <= 0 && this.vy < 0) this.vy = 0
    if (this.posY >= canvas.height - playerHeight && this.vy > 0) this.vy = 0
    this.posY += this.vy
    this.draw()
  }
}

class Ball {
  constructor(x = 0, y = 0, player1, player2) {
    this.posX = x
    this.posY = y
    this.player1 = player1
    this.player2 = player2
    this.radius = 10
    // direction
    this.dirX = 1
    this.dirY = 2
    // velocity
    this.v = ballSpeed
  }
  draw() {
    ctx.beginPath()
    ctx.arc(this.posX, this.posY, this.radius, 0, 2 * Math.PI)
    ctx.fillStyle = 'white'
    ctx.fill()
  }
  #checkCircleRectCollision(player) {
    let pointX = this.posX
    let pointY = this.posY
    if (this.posX < player.posX) pointX = player.posX
    else if (this.posX > player.posX + playerWidth)
      pointX = player.posX + playerWidth
    if (this.posY < player.posY) pointY = player.posY
    else if (this.posY > player.posY + playerHeight)
      pointY = player.posY + playerHeight
    let distX = this.posX - pointX
    let distY = this.posY - pointY
    let distance = Math.sqrt(distX * distX + distY * distY)
    if (distance <= this.radius) return true
    return false
  }
  #checkPlayer1Collision() {
    if (this.posX - this.radius >= this.player1.posX + playerWidth) return false
    if (this.#checkCircleRectCollision(this.player1)) return true
    return false
  }
  #checkPlayer2Collision() {
    if (this.posX + this.radius <= this.player2.posX) return false
    if (this.#checkCircleRectCollision(this.player2)) return true
    return false
  }
  #checkBoundariesCollision() {
    if (
      this.posY - this.radius <= 0 ||
      this.posY + this.radius >= canvas.height
    )
      return true
    return false
  }
  #checkGoal() {
    if (this.posX - this.radius >= canvas.width + 100) return 1
    if (this.posX + this.radius <= -100) return 2
    return 0
  }
  update() {
    // check collisions
    if (this.#checkPlayer1Collision()) {
      if (this.posX <= this.player1.posX + playerWidth) {
        if (this.posY < this.player1.posY + playerHeight / 2) this.dirY = -2
        else this.dirY = 2
      } else this.dirX = 1
    }
    if (this.#checkPlayer2Collision()) {
      if (this.posX >= this.player2.posX) {
        if (this.posY < this.player2.posY + playerHeight / 2) this.dirY = -2
        else this.dirY = 2
      } else this.dirX = -1
    }
    if (this.#checkBoundariesCollision()) this.dirY *= -1
    let goalScorer
    if ((goalScorer = this.#checkGoal())) {
      goalScorer == 1 ? score.value.player1++ : score.value.player2++
      this.posX = canvas.width / 2
      this.posY = canvas.height / 2
    }
    // modify position
    this.posX += this.dirX * this.v
    this.posY += this.dirY * this.v
    this.draw()
  }
}

class Game {
  constructor(ctx, player1, player2, ball) {
    this.ctx = ctx
    this.player1 = player1
    this.player2 = player2
    this.ball = ball
    this.startGame = false
  }
  #draw() {
    ctx.beginPath()
    ctx.moveTo(canvas.width / 2, 0)
    ctx.lineTo(canvas.width / 2, canvas.height)
    ctx.lineWidth = 2
    ctx.strokeStyle = '#F58562'
    ctx.stroke()
  }
  animate() {
    if (!gameStop.value) {
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      this.#draw()
      if (score.value.player1 == maxScore || score.value.player2 == maxScore) {
        gameStop.value = true
        if (props.isTournament == true) {
          if (score.value.player1 == maxScore)
            setWinner(props.player1, props.player2)
          if (score.value.player2 == maxScore)
            setWinner(props.player2, props.player1)
        } else {
          // 1 vs 1 game => send results to backend
          emitResults(
            props.player1,
            props.player2,
            score.value.player1,
            score.value.player2
          )
        }
      }
      if (gameStart.value == false) {
        this.player1.update()
        this.player2.update()
        this.ball.update()
      } else {
        this.player1.draw()
        this.player2.draw()
        this.ball.draw()
      }
    }
    requestAnimationFrame(this.animate.bind(this))
  }
}

const handleKeydown = (e) => {
  if (e.key == 'w') {
    player1.upKeyPressed = true
  } else if (e.key == 's') {
    player1.downKeyPressed = true
  } else if (e.key == 'ArrowUp') {
    e.preventDefault()
    player2.upKeyPressed = true
  } else if (e.key == 'ArrowDown') {
    e.preventDefault()
    player2.downKeyPressed = true
  }
}

const handleKeyup = (e) => {
  if (e.key == 'w') {
    player1.upKeyPressed = false
  } else if (e.key == 's') {
    player1.downKeyPressed = false
  } else if (e.key == 'ArrowUp') {
    player2.upKeyPressed = false
  } else if (e.key == 'ArrowDown') {
    player2.downKeyPressed = false
  }
  // else if (e.key == ' ') {
  //   game.startGame = !game.startGame
  // }
}

const restartGame = () => {
  score.value.player1 = 0
  score.value.player2 = 0
  gameStop.value = false
}

onMounted(() => {
  // if (store.userAuthorised) {
  //   player1.value = store.username
  //   player2.value = 'opponent'
  // }
  canvas = document.getElementById('canvasId')
  ctx = canvas.getContext('2d')
  canvas.width = 700
  canvas.height = 416
  player1 = new Player(32, canvas.height / 2 - playerHeight / 2)
  player2 = new Player(
    canvas.width - playerWidth - 32,
    canvas.height / 2 - playerHeight / 2
  )
  ball = new Ball(canvas.width / 2, canvas.height / 2, player1, player2)
  game = new Game(ctx, player1, player2, ball)
  game.animate()
  addEventListener('keydown', (e) => handleKeydown(e, player1, player2))
  addEventListener('keyup', (e) => {
    handleKeyup(e, player1, player2, game)
  })
  if (props.isTournament) gameStart.value = false

  const player1UpElement = document.getElementById('player1Up')
  player1UpElement.addEventListener('touchstart', (e) => {
    e.preventDefault()
    player1.upKeyPressed = true
  })
  player1UpElement.addEventListener('touchend', (e) => {
    e.preventDefault()
    player1.upKeyPressed = false
  })
  const player1DownElement = document.getElementById('player1Down')
  player1DownElement.addEventListener('touchstart', (e) => {
    e.preventDefault()
    player1.downKeyPressed = true
  })
  player1DownElement.addEventListener('touchend', (e) => {
    e.preventDefault()
    player1.downKeyPressed = false
  })
  const player2UpElement = document.getElementById('player2Up')
  player2UpElement.addEventListener('touchstart', (e) => {
    e.preventDefault()
    player2.upKeyPressed = true
  })
  player2UpElement.addEventListener('touchend', (e) => {
    e.preventDefault()
    player2.upKeyPressed = false
  })
  const player2DownElement = document.getElementById('player2Down')
  player2DownElement.addEventListener('touchstart', (e) => {
    e.preventDefault()
    player2.downKeyPressed = true
  })
  player2DownElement.addEventListener('touchend', (e) => {
    e.preventDefault()
    player2.downKeyPressed = false
  })
})
</script>

<template>
  <section class="">
    <div class="scoreboard col-10 col-md-6 mx-auto">
      <div class="row d-flex align-items-center">
        <p class="text-white text-center fs-4 mb-0 roboto-medium col-4">
          {{ props.player1 }}
        </p>
        <p
          class="text-white text-center fs-2 mb-0 roboto-bold col-4"
          aria-live="polite"
        >
          {{ score.player1 }} : {{ score.player2 }}
        </p>
        <p class="text-white text-center fs-4 mb-0 roboto-medium col-4">
          {{ props.player2 }}
        </p>
      </div>
    </div>
    <div class="canvas-wrapper">
      <canvas class="canvas mx-auto" id="canvasId"></canvas>
      <div id="player1Up" class="player1-touch-up"></div>
      <div id="player1Down" class="player1-touch-down"></div>
      <div id="player2Up" class="player2-touch-up"></div>
      <div id="player2Down" class="player2-touch-down"></div>
      <div
        v-if="gameStart && !props.isTournament"
        class="gamestop d-flex flex-column justify-content-center align-items-center rounded-4 myshadow friends-modal"
      >
        <ButtonComp
          @click="gameStart = false"
          class="mb-2 btn-lg"
          style="width: 120px"
          aria-label="start button"
        >
          {{ getText('start', store.lang) }}
        </ButtonComp>
      </div>
      <div
        v-else-if="gameStop && !props.isTournament"
        class="gamestop d-flex flex-column justify-content-center align-items-center rounded-4 myshadow friends-modal"
      >
        <ButtonComp
          @click="restartGame"
          class="mb-2 btn-lg"
          style="width: 120px"
          aria-label="restart button"
        >
          {{ getText('restart', store.lang) }}
        </ButtonComp>
        <ButtonComp
          @click="router.push('/')"
          class="btn-lg"
          style="width: 120px"
          aria-label="back button"
          >{{ getText('back', store.lang) }}</ButtonComp
        >
      </div>
    </div>

    <button
      class="btn btn-primary rounded-5 mt-3 d-flex justify-content-center align-items-center fs-1 mx-auto controls-btn"
      style="width: 64px; height: 64px"
      data-bs-toggle="modal"
      data-bs-target="#helpModal"
      aria-label="open controls modal button"
    >
      ?
    </button>

    <HelpModalComp />
  </section>
</template>

<style scoped>
.myshadow {
  box-shadow: -6px 6px 6px 0px rgba(0, 0, 0, 0.25);
}

.controls-btn:focus {
  color: #f58562;
}

.friends-modal {
  background: linear-gradient(
    145deg,
    rgba(60, 26, 153, 0.97) 23%,
    55%,
    rgba(92, 42, 132, 0.97) 85%
  );
  backdrop-filter: blur(2px);
}

.gamestop {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 220px;
  height: 140px;
  border: 2px solid #f58562;
}

.canvas-wrapper {
  position: relative;
}

.player1-touch-up {
  position: absolute;
  top: 0;
  left: 0;
  height: 50%;
  width: 10%;
}
.player1-touch-down {
  position: absolute;
  top: 50%;
  left: 0;
  height: 50%;
  width: 10%;
}
.player2-touch-up {
  position: absolute;
  top: 0;
  right: 0;
  height: 50%;
  width: 10%;
}
.player2-touch-down {
  position: absolute;
  top: 50%;
  right: 0;
  height: 50%;
  width: 10%;
}

.canvas {
  @media screen and (max-width: 600px) {
    border: 2px solid #f58562;
    border-left: none;
    border-right: none;
  }
  width: 100%;
  border: 5px solid #f58562;
  border-right: none;
  border-left: none;
}

.btn-primary {
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
}
</style>
