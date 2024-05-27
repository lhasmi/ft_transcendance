# Pong

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin).

## Customize configuration

See [Vite Configuration Reference](https://vitejs.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```

# Suggestion for the verify (send OTP button request)
async function verifyOtp() {
    const username = document.getElementById('username').value;
    const otp = document.getElementById('otp').value;

    const response = await fetch('/verify-otp/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access')}`  // Ensure the token is sent in the headers
        },
        body: JSON.stringify({ username, otp })
    });

    const data = await response.json();

    if (response.ok) {
        // Handle successful OTP verification
        console.log('OTP verified:', data);
        // Store the new tokens if needed
        localStorage.setItem('access', data.access);
        localStorage.setItem('refresh', data.refresh);
    } else {
        // Handle errors
        console.error('Error verifying OTP:', data);
    }
}
