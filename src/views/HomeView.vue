<script setup>
import { store } from '../store/store.js'
import { getText } from '../language/language.js';
import ButtonComp from '../components/ButtonComp.vue'

</script>

<template>
  <!-- Home View -->
  <section
    class="container flex-grow-1 d-flex flex-column justify-content-center align-items-center"
    style="height: 100%"
  >
    <div class="menu col-11 col-md-6 col-lg-4">
			<h2 class="text-center roboto-bold m-0" style="color: #f58562; font-size: 3rem;">{{ getText('playPong', store.lang) }}</h2>
			<hr class="mode-splitter my-2 col-11 mx-auto" />
			<h3 class="text-center roboto-bold fs-4 m-0 mb-3" style="color: #f58562">{{ getText('chooseMode', store.lang) }}</h3>
      <div
        class="d-flex flex-column justify-content-center align-content-center col-8 mx-auto"
      >
        <ButtonComp class="btn-lg fs-3" linkTo="/game">{{ getText('duel', store.lang) }}</ButtonComp>
        <ButtonComp class="btn-lg fs-3 mt-4" linkTo="/tournament">{{ getText('tournament', store.lang) }}</ButtonComp>
        <!-- <h3 class="align-self-center my-1 roboto-bold fs-2">{{ getText('offline', store.lang) }}</h3> -->
      </div>
      <!-- <div
        v-if="!store.userAuthorised"
        class="online-group d-flex flex-column justify-content-center align-content-center col-8 mx-auto"
      >
        <h3 class="align-self-center my-1 roboto-bold fs-2">{{ getText('online', store.lang) }}</h3>
        <ButtonComp class="btn-lg fs-3 login-disabled" disabled>
          1 vs 1
          <span class="login roboto-regular">{{ getText('loginToPlay', store.lang) }}</span>
        </ButtonComp>
      </div>
      <div
        v-else
        class="online-group d-flex flex-column justify-content-center align-content-center col-8 mx-auto"
      >
        <h3 class="align-self-center my-1 roboto-bold fs-2">{{ getText('online', store.lang) }}</h3>
        <ButtonComp class="btn-lg fs-3">1 vs 1</ButtonComp>
      </div> -->
    </div>
  </section>
  <!-- !Home View -->
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
