<script setup>
const props = defineProps({
  linkTo: String,
  disabled: Boolean
})
</script>
<template>
  <button v-if="!linkTo" class="btn btn-primary roboto-bold rounded-4" :disabled="disabled">
    <slot></slot>
  </button>
  <RouterLink v-else class="btn btn-primary btn-lg roboto-bold fs-3 rounded-4" :to="linkTo">
    <slot></slot>
  </RouterLink>
</template>
<style scoped>
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
.btn-primary:active,
.btn-primary:focus {
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
