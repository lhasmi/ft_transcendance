<script setup>
import { ref, onUnmounted } from 'vue'
import { store } from '@/store/store'
import { getText } from '../language/language.js'

const largeText = ref(false)
onUnmounted(() => {
  // profileModal.classList.remove('show')
  // profileModal.style.display = 'none'
  let backdrops = document.getElementsByClassName('modal-backdrop');
  for (let i = 0; i < backdrops.length; i++) {
      backdrops[i].style.display = 'none';
  }
})
</script>

<template>
  <!-- Modal -->
  <div
    class="modal fade"
    id="helpModal"
    tabindex="-1"
    aria-labelledby="helpModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-scrollable modal-dialog-centered">
      <div class="friends-modal modal-content myshadow border-0 rounded-4">
        <div class="modal-header border-0 d-flex flex-column m-0 p-0">
          <div class="d-flex position-relative w-100">
            <div></div>
            <h1
              class="friends-modal-title modal-title fs-3 my-2 mx-auto roboto-bold"
              id="friendsModalLabel"
            >
              {{ getText('controls', store.lang) }}
            </h1>
            <button
              type="button"
              class="icon-close"
              data-bs-dismiss="modal"
              aria-label="close button"
            >
              <span class="material-symbols-outlined" style="font-size: 2rem">
                close
              </span>
            </button>
          </div>
          <hr class="splitter col-12 mx-auto m-0 mb-2" />
        </div>
        <div class="modal-body m-0 p-0" style="height: 280px">
          <div
            class="col-10 col-md-9 mx-auto d-flex flex-column justify-content-center"
          >
            <div class="d-flex align-content-center mb-2">
              <label for="large-text" class="m-0 text-white roboto-regular"
                >{{ getText('largeText', store.lang) }}:</label
              >
              <input
                v-model="largeText"
                id="large-text"
                type="checkbox"
                class="ms-2"
              />
            </div>
            <p v-if="largeText" class="text-white roboto-regular fs-2">
              <span tabindex="0" style="color: #f58562">{{ getText('leftPlayer', store.lang) }}:</span> {{ getText('leftPlayerControls', store.lang) }} <br />
              <span tabindex="0" style="color: #f58562">{{ getText('rightPlayer', store.lang) }}:</span> {{ getText('rightPlayerControls', store.lang) }} <br />
              <span tabindex="0" style="color: #f58562">{{ getText('touchscreen', store.lang) }}:</span> {{ getText('touchscreenControls', store.lang) }}
            </p>
            <p v-else class="text-white roboto-regular fs-5">
              <span tabindex="0" style="color: #f58562">{{ getText('leftPlayer', store.lang) }}:</span> {{ getText('leftPlayerControls', store.lang) }} <br />
              <span tabindex="0" style="color: #f58562">{{ getText('rightPlayer', store.lang) }}:</span> {{ getText('rightPlayerControls', store.lang) }} <br />
              <span tabindex="0" style="color: #f58562">{{ getText('touchscreen', store.lang) }}:</span> {{ getText('touchscreenControls', store.lang) }}
            </p>
						<div tabindex="0"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-body {
  scrollbar-color: rgba(255, 255, 255, 0.1) rgba(255, 255, 255, 0.1);
  scrollbar-width: thin;
}

.myshadow {
  box-shadow: -6px 6px 6px 0px rgba(0, 0, 0, 0.25);
}

.friends-modal {
  background: linear-gradient(
    145deg,
    rgba(60, 26, 153, 0.9) 23%,
    55%,
    rgba(92, 42, 132, 0.9) 85%
  );
  backdrop-filter: blur(2px);
}

.friends-modal-title {
  color: #f58562;
}

.icon-close {
  position: absolute;
  background: none;
  border: none;
  top: 0.7rem;
  right: 0.7rem;
  color: white;
  transition: all 0.2s ease;
}
.icon-close:hover,
.icon-close:focus {
  color: #f58562;
}

.splitter {
  color: transparent;
  border-bottom: 3px solid #f58562;
  opacity: 1;
}
</style>
