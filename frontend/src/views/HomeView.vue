<script setup>
import { store } from '../store/store.js'
</script>

<template>
  <main>
    <div class="options">
      <RouterLink class="btn roboto-regular" to="/game">Play</RouterLink>
      <RouterLink class="btn roboto-regular" to="/game">Tournament</RouterLink>
      <p class="mode roboto-regular">Offline</p>
    </div>
    <div v-if="store.userAuthorised" class="options">
      <p class="mode roboto-regular">Online</p>
      <RouterLink class="btn roboto-regular" to="/game">Play</RouterLink>
      <RouterLink class="btn roboto-regular" to="/game">Tournament</RouterLink>
    </div>
    <div v-else class="options options-unauthorised">
      <p class="mode roboto-regular">Online</p>
      <button class="btn-unauthorised roboto-regular" to="/game">
        Play
        <span class="tooltip roboto-regular">Log in to play online</span>
      </button>
      <button class="btn-unauthorised roboto-regular" to="/game">
        Tournament
        <span class="tooltip roboto-regular">Log in to play online</span>
      </button>
    </div>
  </main>
</template>

<style scoped>
.options {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-content: center;
}
.options:first-of-type {
  border-bottom: 2px solid rgba(255, 166, 0, 0.8);
}
.options-unauthorised {
  position: relative;
}

.info {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.info-text {
  text-align: center;
  font-size: 36px;
  font-weight: 900;
  color: lightgrey;
}

.mode {
  margin-top: 6px;
  margin-bottom: 6px;
  text-align: center;
  font-size: 24px;
  letter-spacing: 1px;
  color: lightgrey;
}

.btn {
  font-weight: 700;
  text-align: center;
  text-decoration: none;
  width: 260px;
  padding: 12px 32px;
  margin-bottom: 16px;
  font-size: 32px;
  background-color: rgb(40, 40, 40);
  color: rgba(255, 166, 0, 0.8);
  background-color: rgb(40, 40, 40);
  border-radius: 24px;
  border: solid rgb(62, 62, 62);
  transition: all 0.1s ease-in-out;
}
.btn:last-of-type {
  margin-bottom: 0px;
}
.btn:hover {
  transform: scale(1.05);
  box-shadow: 8px 8px 12px rgb(8, 8, 8);
  /* border: solid lightgrey; */
}
.btn-unauthorised {
  position: relative;
  font-weight: 700;
  text-align: center;
  text-decoration: none;
  width: 260px;
  height: 80px;
  padding: 12px 32px;
  margin-bottom: 16px;
  font-size: 32px;
  color: rgba(255, 166, 0, 0.5);
  cursor: unset;
  background-color: rgb(32, 32, 32);
  border-radius: 24px;
  border: solid rgb(52, 52, 52);
}
.btn-unauthorised:last-of-type {
  margin-bottom: 0px;
}
.btn-unauthorised .tooltip {
  position: absolute;
  display: none;
  top: 50%;
  left: 105%;
  transform: translateY(-50%);
  width: 100px;
  font-size: 16px;
  color: lightgrey;
}
.btn-unauthorised:hover .tooltip {
  display: block;
}
</style>
