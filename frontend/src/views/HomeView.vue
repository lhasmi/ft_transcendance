<script setup>
import { store } from '../store/store.js'
</script>

<template>
  <main>
    <div class="options">
      <RouterLink class="btn" to="/game">Play</RouterLink>
      <RouterLink class="btn" to="/game">Tournament</RouterLink>
      <p class="mode roboto-regular">Offline</p>
    </div>
    <div class="options" :class="store.userAuthorised ? '' : 'options-unauthorised'">
      <p class="mode roboto-regular">Online</p>
      <RouterLink class="btn" to="/game">Play</RouterLink>
      <RouterLink class="btn" to="/game">Tournament</RouterLink>
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
  /* background-color: red; */
  /* cursor: wait; */
}
.options-unauthorised .btn {
  /* pointer: none; */
  /* cursor: wait; */
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
  /* cursor: pointer; */
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
}
</style>
