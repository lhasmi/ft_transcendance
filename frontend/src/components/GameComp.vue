<script setup>
import { ref, onMounted } from 'vue'
import { store } from '@/store/store'
import HelpModalComp from './HelpModalComp.vue'

const props = defineProps({
  isTournament: Boolean,
  player1: String,
  player2: String,
})

const score = ref({
  player1: 0,
  player2: 0,
})

const gameFinished = ref(false)

const emit = defineEmits(['winner', 'results'])

const emitResults = (player1, player2, score1, score2) => {
  emit('results', player1, player2, score1, score2)
}

const setWinner = (winner, loser) => {
  emit('winner', winner, loser)
}

// const sendGameResult = async () => {
//   const response = await fetch('http://127.0.0.1:8000/games/', {
//     method: 'POST',
//     headers: {
//       'Content-Type': 'application/json',
//       Authorization: `Bearer ${localStorage.getItem('access')}`,
//     },
//     body: JSON.stringify({
//       players: ['vpaul', 'admin'],
//       winner: 'vpaul',
//       played_on: '2023-05-20T14:28:23.382Z',
//       details: 'Match details here.',
//     }),
//   })

//   const data = await response.json()
//   console.log(data)
//   if (!response.ok) {
//     console.log('error: ' + data.error)
//   }
// }

// GAME
let canvas
let ctx
const playerWidth = 4
const playerHeight = 100
const playerSpeed = 3
const ballSpeed = 2

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
    if (gameFinished.value) return
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    this.#draw()
    if (score.value.player1 == 1 || score.value.player2 == 1) {
      gameFinished.value = true
      if (props.isTournament == true) {
        if (score.value.player1 == 1) setWinner(props.player1, props.player2)
        if (score.value.player2 == 1) setWinner(props.player2, props.player1)
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
    if (this.startGame) {
      this.player1.update()
      this.player2.update()
      this.ball.update()
    } else {
      this.player1.draw()
      this.player2.draw()
      this.ball.draw()
    }
    requestAnimationFrame(this.animate.bind(this))
  }
}

onMounted(() => {
  canvas = document.getElementById('canvasId')
  ctx = canvas.getContext('2d')
  canvas.width = 700
  canvas.height = 466
  const player1 = new Player(32, canvas.height / 2 - playerHeight / 2)
  const player2 = new Player(
    canvas.width - playerWidth - 32,
    canvas.height / 2 - playerHeight / 2
  )
  const ball = new Ball(canvas.width / 2, canvas.height / 2, player1, player2)
  const game = new Game(ctx, player1, player2, ball)
  game.animate()
  if (store.userAuthorised) {
    player1.value = store.username
    player2.value = 'opponent'
  }
  addEventListener('keydown', (e) => {
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
  })
  addEventListener('keyup', (e) => {
    if (e.key == 'w') {
      player1.upKeyPressed = false
    } else if (e.key == 's') {
      player1.downKeyPressed = false
    } else if (e.key == 'ArrowUp') {
      player2.upKeyPressed = false
    } else if (e.key == 'ArrowDown') {
      player2.downKeyPressed = false
    } else if (e.key == ' ') {
      game.startGame = !game.startGame
    }
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
        <p class="text-white text-center fs-2 mb-0 roboto-bold col-4">
          {{ score.player1 }} : {{ score.player2 }}
        </p>
        <p class="text-white text-center fs-4 mb-0 roboto-medium col-4">
          {{ props.player2 }}
        </p>
      </div>
    </div>
    <canvas class="canvas mx-auto" id="canvasId"></canvas>

    <button
      class="btn btn-primary rounded-5 mt-3 d-flex justify-content-center align-items-center fs-1 mx-auto"
      style="width: 64px; height: 64px"
      data-bs-toggle="modal"
      data-bs-target="#helpModal"
    >
      ?
    </button>

    <HelpModalComp />
  </section>
</template>

<style scoped>
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
