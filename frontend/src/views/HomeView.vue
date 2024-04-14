<script setup>
import { store } from '../store/store.js'
import ButtonComp from '../components/ButtonComp.vue'
</script>

<template>
  <!-- Home View -->
  <section
    class="container flex-grow-1 d-flex flex-column justify-content-center align-items-center"
    style="height: 100%"
  >
    <div class="menu" style="width: 300px">
      <div
        class="offline-group d-flex flex-column justify-content-center align-content-center col-8 mx-auto"
      >
        <ButtonComp class="btn-lg fs-3" linkTo="/game">1 vs 1</ButtonComp>
        <ButtonComp class="btn-lg fs-3 mt-3" linkTo="/game">tournament</ButtonComp>
        <h3 class="align-self-center my-1 roboto-bold fs-2">offline</h3>
      </div>
      <hr class="mode-splitter my-0 col-10 mx-auto" />
      <div
        v-if="!store.userAuthorised"
        class="online-group d-flex flex-column justify-content-center align-content-center col-8 mx-auto"
      >
        <h3 class="align-self-center my-1 roboto-bold fs-2">online</h3>
        <!-- <button class="btn btn-primary btn-lg roboto-bold fs-3 rounded-4" disabled>
          1 vs 1
          <span class="login roboto-regular">login to play online</span>
        </button> -->
        <ButtonComp class="btn-lg fs-3 login-disabled" disabled>
          1 vs 1
          <span class="login roboto-regular">login to play online</span>
        </ButtonComp>
      </div>
      <div
        v-else
        class="online-group d-flex flex-column justify-content-center align-content-center col-8 mx-auto"
      >
        <h3 class="align-self-center my-1 roboto-bold fs-2">online</h3>
        <ButtonComp class="btn-lg fs-3">1 vs 1</ButtonComp>
      </div>
    </div>
  </section>
  <!-- !Home View -->

  <!-- <section>
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
  </section> -->
</template>

<style scoped>
.menu h3 {
  color: #f58562;
}

.login {
  position: absolute;
  top: 48%;
  left: 101%;
  transform: translateY(-50%);
  width: 80px;
  font-size: 14px;
  color: white;
  transition: all 0.2s ease;
  opacity: 0;
}
.login-disabled:hover .login {
  opacity: 1;
}

.mode-splitter {
  border: 2px solid #f58562;
  opacity: 1;
}
</style>
