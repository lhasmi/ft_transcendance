<script setup>
import { store } from '../store/store.js'
</script>

<template>
  <header>
    <div v-if="store.userAuthorised" class="header-left">
      <p class="header-text">Friends (0)</p>
    </div>
    <div class="logo-n-text">
      <h1 class="logo roboto-bold">Pong Game</h1>
      <p class="logo-text">Don't forget to have some fun!</p>
      <!-- <button @click="store.userAuthorised = !store.userAuthorised">userAuthorised</button> -->
    </div>
    <div v-if="store.userAuthorised" class="header-right">
      <p class="header-text">Profile</p>
      <p class="header-text">Log out</p>
    </div>
    <div v-else class="header-right">
      <p class="header-text">Register</p>
      <p class="header-text">Log in</p>
    </div>
  </header>
</template>

<style scoped>
header {
  position: relative;
  width: 64%;
  margin: 0 auto;
  align-items: center;
  padding: 12px 0;
  background-color: rgb(40, 40, 40);
  border-radius: 24px / 0 0 24px 24px;
  border: solid rgb(62, 62, 62);
  border-top: none;
  box-shadow: 8px 8px 12px rgb(8, 8, 8);
}

.header-left {
  position: absolute;
  height: 100%;
  top: 0;
  left: 60px;
  display: flex;
  align-items: center;
}
.header-right {
  position: absolute;
  height: 100%;
  top: 0;
  right: 60px;
  display: flex;
  align-items: center;
}
.header-right .header-text:first-of-type {
  margin-right: 32px;
}

.header-text {
  color: rgba(255, 166, 0, 0.5);
  font-size: 22px;
  font-weight: 500;
  cursor: pointer;
}
.header-text:hover {
  text-decoration: underline;
}

.logo-n-text {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex-grow: 2;
}

.logo {
  color: rgba(255, 166, 0, 0.8);
}

.logo-text {
  color: rgba(255, 166, 0, 0.5);
  /* color: lightgrey; */
}
</style>
