<script setup></script>

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
              controls
            </h1>
            <button
              type="button"
              class="icon-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            >
              <span class="material-symbols-outlined" style="font-size: 2rem">
                close
              </span>
            </button>
          </div>
          <hr class="splitter col-12 mx-auto m-0 mb-2" />
        </div>
        <div class="modal-body">
          <div class="col-10 col-md-8 mx-auto d-flex justify-content-center">
            <div class="">
              <p class="roboto-medium fs-5 m-0" style="color: #f58562">
                left player:
              </p>
              <p class="text-white roboto-regular fs-6 m-0">w - up</p>
              <p class="text-white roboto-regular fs-6 m-0">s - down</p>
              <p class="roboto-medium fs-5 m-0 mt-1" style="color: #f58562">
                right player:
              </p>
              <p class="text-white roboto-regular fs-6 m-0">arrow up - up</p>
              <p class="text-white roboto-regular fs-6 m-0">
                arrow down - down
              </p>
              <p class="text-white roboto-regular fs-6 mt-3">
                space - pause/unpause
              </p>
            </div>
          </div>
        </div>
        <!-- <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
          >
            Close
          </button>
          <button type="button" class="btn btn-primary">Save changes</button>
        </div> -->
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
.icon-close:hover {
  color: #f58562;
}

.splitter {
  color: transparent;
  border-bottom: 3px solid #f58562;
  opacity: 1;
}
</style>
