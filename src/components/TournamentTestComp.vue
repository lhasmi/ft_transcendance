<script setup>
import ButtonComp from './ButtonComp.vue'

const props = defineProps({
	match: Object
})

const emit = defineEmits(['winner'])

const setWinner = (winner, loser) => {
	emit('winner', winner, loser)
}

</script>

<template>
	<div class="row">
		<p class="fs-3 roboto-bold text-center" style="color: #f58562;">TEST!</p>
		<p class="fs-3 roboto-bold text-center" style="color: #f58562;">choose winner</p>
		<ButtonComp @click="setWinner(props.match[0], props.match[1])" class="btn-lg my-2">{{ props.match[0] }}</ButtonComp>
		<ButtonComp @click="setWinner(props.match[1], props.match[0])" class="btn-lg my-2">{{ props.match[1] }}</ButtonComp>
	</div>
</template>

<style scoped>
</style>