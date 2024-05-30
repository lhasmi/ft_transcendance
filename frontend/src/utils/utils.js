import { store } from '../store/store.js'

const refreshAccessToken = async () => {
  const response = await fetch('http://127.0.0.1:8000/api/token/refresh/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      refresh: `${localStorage.getItem('refresh')}`,
    }),
  })
  if (!response.ok) {
    console.log("couldn't refresh token")
    return false
  }
  const data = await response.json()
  console.log('refreshed')
  console.log(data)
  localStorage.setItem('access', data.access)
  return true
}

export const fetchWithJWT = async (
  url,
  method = 'GET',
  data = null,
  json = null
) => {
  if (json) {
    data = JSON.stringify(data)
  }

  let response = await fetch(url, {
    method: method,
    headers: {
      Authorization: `Bearer ${localStorage.getItem('access')}`,
    },
    ...(data && { body: data }),
  })

  if (!response.ok && response.status === 401) {
    console.log(response)
    if ((await refreshAccessToken()) == false) return response
    response = await fetch(url, {
      method: method,
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access')}`,
      },
      ...(data && { body: data }),
    })
  }
  return response
}

export const fetchWithJWTJson = async (url, method = 'GET', data = null) => {
  let response = await fetch(url, {
    method: method,
    headers: {
      Authorization: `Bearer ${localStorage.getItem('access')}`,
      'Content-Type': 'application/json',
    },
    ...(data && { body: JSON.stringify(data) }),
  })

  if (!response.ok && response.status === 401) {
    console.log(response)
    await refreshAccessToken()
    response = await fetch(url, {
      method: method,
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access')}`,
        'Content-Type': 'application/json',
      },
      ...(data && { body: JSON.stringify(data) }),
    })
  }
  return response
}

export const logout = () => {
  console.log('LOGOUT')
  localStorage.removeItem('access')
  localStorage.removeItem('refresh')
  localStorage.removeItem('lang')
  store.userAuthorised = false
  store.username = ''
  store.email = ''
  store.picture = ''
  // store.socket.close()
  store.socket = null
}

export const connectWithSocket = () => {
	// socket connection to track online status
	let protocol = window.location.protocol
	let wsProtocol = protocol == 'https' ? 'wss' : 'ws'

	store.socket = new WebSocket(
		`${wsProtocol}://ws/status/?token=${localStorage.getItem('access')}`
	)
	store.socket.onopen = () => {
		console.log(
			'CONNECTED TO STATUS CONSUMER (my online status should be online now)'
		)
	}
}