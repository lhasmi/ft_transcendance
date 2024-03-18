<script setup>
import { ref, onMounted } from 'vue'

let canvas
let ctx
const playerWidth = 4
const playerHeight = 116
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
    this.color = 'rgba(255, 166, 0, 0.8)'

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
  #draw() {
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
    else if (this.upKeyPressed) this.vy = -1.5
    else if (this.downKeyPressed) this.vy = 1.5
    else if (!this.upKeyPressed && !this.downKeyPressed) this.vy = 0

    // boundaries check
    if (this.posY <= 0 && this.vy < 0) this.vy = 0
    if (this.posY >= canvas.height - playerHeight && this.vy > 0) this.vy = 0

    this.posY += this.vy
    this.#draw()
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
    this.v = 1
  }
  #draw() {
    ctx.beginPath()
    ctx.arc(this.posX, this.posY, this.radius, 0, 2 * Math.PI)
    ctx.fillStyle = 'lightgrey'
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
    this.#draw()
  }
}

class Game {
  constructor(ctx, player1, player2, ball) {
    this.ctx = ctx
    this.player1 = player1
    this.player2 = player2
    this.ball = ball

    // time delta
    // this.lastTime = 0
    // this.interval = 1000 / 60
    // this.timer = 0
  }
  #draw() {
    ctx.moveTo(canvas.width / 2, 0)
    ctx.lineTo(canvas.width / 2, canvas.height)
    ctx.strokeStyle = 'rgba(255, 166, 0, 0.5)'
    ctx.stroke()
  }
  animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    this.#draw()
    this.player1.update()
    this.player2.update()
    this.ball.update()

    requestAnimationFrame(this.animate.bind(this))
  }
}

onMounted(() => {
  canvas = document.getElementById('canvasId')
  ctx = canvas.getContext('2d')
  canvas.width = 720
  canvas.height = 480

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
    }
  })
})
</script>

<template>
  <main>
    <div class="top_bar">
      <RouterLink class="btn" to="/">Back</RouterLink>
      <p class="nickname">Player1</p>
      <p class="score">{{ score.player1 + ' : ' + score.player2 }}</p>
      <p class="nickname">Player2</p>
    </div>
    <canvas class="canvas" id="canvasId"> Hello </canvas>
  </main>
</template>

<style scoped>
.canvas {
  border: 4px solid rgba(255, 166, 0, 0.5);
  border-right: none;
  border-left: none;
}

.top_bar {
  position: relative;
  width: 64%;
  display: flex;
  margin: 6px 0 22px 0;
  /* margin-bottom: 14px; */
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
  font-size: 26px;
  color: lightgrey;
}

.nickname:first-of-type {
  margin-left: 120px;
}
.nickname:last-of-type {
  margin-right: 120px;
}

.score {
  font-weight: bold;
  font-size: 40px;
}

.btn {
  left: 0;
  position: absolute;
  text-decoration: none;
  width: fit-content;
  padding: 5px 12px;
  margin-left: 20px;
  /* margin-bottom: 20px; */
  font-size: 22px;
  background-color: rgb(40, 40, 40);
  color: rgba(255, 166, 0, 0.8);
  cursor: pointer;
  background-color: rgb(40, 40, 40);
  border-radius: 16px;
  border: solid rgb(62, 62, 62);
  transition: all 0.1s ease-in-out;
}
.btn:hover {
  transform: scale(1.05);
  box-shadow: 4px 4px 6px rgb(8, 8, 8);
}
</style>
