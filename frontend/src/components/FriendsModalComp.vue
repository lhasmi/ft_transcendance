<script setup>
// test data
const data = {
  friends: [
    { username: 'friend1', status: 'online' },
    { username: 'friend2', status: 'online' },
    { username: 'friend3', status: 'offline' },
    { username: 'friend4', status: 'online' },
    { username: 'friend5', status: 'offline' }
  ]
}

// funcions
const getStatusColor = (status) => {
  if (status === 'online') return 'background: #66bf6a'
  else return 'background: rgba(255, 255, 255, 0.1)'
}
</script>

<template>
  <div
    class="modal fade"
    id="friendsModal"
    tabindex="-1"
    aria-labelledby="friendsModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-scrollable modal-dialog-centered">
      <div class="friends-modal modal-content myshadow border-0 rounded-4">
        <div class="modal-header border-0 d-flex flex-column m-0 p-0">
          <div class="d-flex position-relative w-100">
            <h1
              class="friends-modal-title modal-title fs-3 my-2 mx-auto roboto-bold"
              id="friendsModalLabel"
            >
              friends
            </h1>
            <button type="button" class="icon-close" data-bs-dismiss="modal" aria-label="Close">
              <span class="material-symbols-outlined" style="font-size: 2rem"> close </span>
            </button>
          </div>
          <hr class="splitter col-9 mx-auto m-0 mb-2" />
        </div>
        <div class="modal-body p-0 d-flex flex-column mb-3" style="height: 396px">
          <div
            class="friend-item col-9 col-md-7 mx-auto d-flex justify-content-center my-2"
            v-for="item in data.friends"
            :key="item.username"
          >
            <p class="friend-item-name roboto-regular fs-5 mb-0">{{ item.username }}</p>
            <div class="friend-status ms-3 my-auto" :style="getStatusColor(item.status)"></div>
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
  background: linear-gradient(145deg, rgba(60, 26, 153, 0.9) 23%, 55%, rgba(92, 42, 132, 0.9) 85%);
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

.friend-item-name {
  color: white;
}

.friend-item {
  border-top: 2px solid white;
  border-bottom: 2px solid white;
  transition: all 0.2s ease;
}
.friend-item:hover {
  border-color: #f58562;
}
.friend-item:hover .friend-item-name {
  color: #f58562;
}

.friend-status {
  height: 16px;
  width: 16px;
  border-radius: 50%;
}
</style>
