import { reactive } from 'vue'

export const store = reactive({
  userAuthorised: false,
  lang: '',
  username: '',
  email: '',
  picture: '',
  socket: null,
})
