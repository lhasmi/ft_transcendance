<script setup>
import { ref, onMounted } from 'vue'

let canvas
let ctx
const playerWidth = 4
const playerHeight = 100
const playerSpeed = 1.5


const score = ref({
  player1: 0,
  player2: 0
})

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

    //
    // addEventListener('keydown', (e) => {
    //   // DYNAMIC SPEED
    //   // if (e.key == 'ArrowUp' || e.key == 'w') {
    //   //   this.keyPressed = true
    //   //   if (this.vy > -2) this.vy -= 0.1
    //   // } else if (e.key == 'ArrowDown' || e.key == 's') {
    //   //   this.keyPressed = true
    //   //   if (this.vy < 2) this.vy += 0.1
    //   // }
    //   // STATIC SPEED
    //   if (e.key == 'ArrowUp' || e.key == 'w') {
    //     this.keyPressed = true
    //     if (this.vy > -2) this.vy = -1.5
    //   } else if (e.key == 'ArrowDown' || e.key == 's') {
    //     this.keyPressed = true
    //     if (this.vy < 2) this.vy = 1.5
    //   }
    // })

    // addEventListener('keyup', (e) => {
    //   if (e.key == 'ArrowUp' || e.key == 'w') {
    //     this.keyPressed = false
    //   } else if (e.key == 'ArrowDown' || e.key == 's') {
    //     this.keyPressed = false
    //   }
    // })
  }
  draw() {
    ctx.fillStyle = this.color
    ctx.fillRect(this.posX, this.posY, playerWidth, playerHeight)
  }
  update() {
    // movement key is not pressed
    // DYNAMIC SPEED
    // if (this.vy >= -0.02 && this.vy <= 0.02 && !this.keyPressed) this.vy = 0
    // if (this.vy < -0.02 && !this.keyPressed) this.vy += 0.02
    // if (this.vy > 0.02 && !this.keyPressed) this.vy -= 0.02
    // STATIC SPEED
    // if (!this.upKeyPressed && !this.downKeyPressed) this.vy = 0
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
    this.v = 2
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
    else if (this.posX > player.posX + playerWidth) pointX = player.posX + playerWidth

    if (this.posY < player.posY) pointY = player.posY
    else if (this.posY > player.posY + playerHeight) pointY = player.posY + playerHeight

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
    if (this.posY - this.radius <= 0 || this.posY + this.radius >= canvas.height) return true
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

    // time delta
    this.lastTime = 0
    // this.interval = 1000 / 60
    // this.timer = 0
  }
  #draw() {
    ctx.beginPath()
    ctx.moveTo(canvas.width / 2, 0)
    ctx.lineTo(canvas.width / 2, canvas.height)
    ctx.lineWidth = 2
    ctx.strokeStyle = '#F58562'
    ctx.stroke()
  }
  animate(timeStamp) {
	const timeDelta = timeStamp - this.lastTime
	this.lastTime = timeStamp
	console.log(timeDelta)
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    this.#draw()
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
  const player2 = new Player(canvas.width - playerWidth - 32, canvas.height / 2 - playerHeight / 2)
  const ball = new Ball(canvas.width / 2, canvas.height / 2, player1, player2)

  const game = new Game(ctx, player1, player2, ball)
  game.animate()

  // addEventListener('keydown', (e) => {
  //   if (e.key == 'ArrowUp' || e.key == 'w') {
  //     player1.keyPressed = true
  //     if (player1.vy > -2) player1.vy -= 0.05
  //   } else if (e.key == 'ArrowDown' || e.key == 's') {
  //     player1.keyPressed = true
  //     if (player1.vy < 2) player1.vy += 0.05
  //   }
  // })

  // addEventListener('keyup', (e) => {
  //   if (e.key == 'ArrowUp' || e.key == 'w') {
  //     player1.keyPressed = false
  //   } else if (e.key == 'ArrowDown' || e.key == 's') {
  //     player1.keyPressed = false
  //   }
  // })

  addEventListener('keydown', (e) => {
    // DYNAMIC SPEED
    // if (e.key == 'ArrowUp' || e.key == 'w') {
    //   this.keyPressed = true
    //   if (this.vy > -2) this.vy -= 0.1
    // } else if (e.key == 'ArrowDown' || e.key == 's') {
    //   this.keyPressed = true
    //   if (this.vy < 2) this.vy += 0.1
    // }
    // STATIC SPEED
    if (e.key == 'w') {
      player1.upKeyPressed = true
    } else if (e.key == 's') {
      player1.downKeyPressed = true
    } else if (e.key == 'ArrowUp') {
      player2.upKeyPressed = true
    } else if (e.key == 'ArrowDown') {
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
  <section
    class="container flex-grow-1 d-flex flex-column justify-content-center align-items-center"
  >
    <div class="scoreboard col-6 mx-auto d-flex justify-content-around align-items-center">
      <p class="text-white fs-4 mb-0 roboto-medium">pvznuzda</p>
      <p class="text-white fs-2 mb-0 roboto-bold">{{ score.player1 }} : {{ score.player2 }}</p>
      <p class="text-white fs-4 mb-0 roboto-medium">opponent</p>
    </div>
    <canvas class="canvas" id="canvasId"></canvas>
    <button
      class="btn btn-primary rounded-5 mt-3 d-flex justify-content-center align-items-center fs-1"
      style="width: 64px; height: 64px"
    >
      ?
    </button>
  </section>
</template>

<style scoped>
.canvas {
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
