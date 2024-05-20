<script setup>
import { onMounted } from "vue";
import { RouterView } from "vue-router";
import HeaderComp from "./components/HeaderComp.vue";
import { store } from "./store/store.js";
import { fetchWithJWT } from "./utils/utils.js";

onMounted(async () => {
  // try {
  //   const response = await fetch(
  //     // "https://api.intra.42.fr/oauth/token?grant_type=authorization_code&code=63858ce2f7b41cef6c055bf5202df26aa32a8422f2dfd62c1ae46491da32962c&redirect_uri=http://127.0.0.1:8000/oauth/callback/&client_id=u-s4t2ud-1303a4f7f8900a6bd31098477269cc5747fab2e7e9f510c47f0e740818e15727&client_secret=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",
  //     "https://api.intra.42.fr/oauth/token?grant_type=authorization_code&code=69fb743b582870dfabb3e42873293fcd61280bf29e829a9638a14aac10bfff4d&redirect_uri=http://127.0.0.1:8000/oauth/callback/&client_id=u-s4t2ud-1303a4f7f8900a6bd31098477269cc5747fab2e7e9f510c47f0e740818e15727&client_secret=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",
  //     {
  //       method: "POST",
  //     }
  //   );
  //   if (!response.ok) {
  //     console.log(response.error);
  //   }
  //   const data = await response.json();
  //   console.log(data);
  // } catch (error) {
  //   console.log(error);
  // }

  try {
    if (localStorage.getItem("access") && localStorage.getItem("refresh")) {
      console.log("try to login...");
      const response = await fetchWithJWT(
        "http://127.0.0.1:8000/update-profile/"
      );
      if (!response.ok) {
        console.log("can't login with existing JWT");
        return;
      }
      const data = await response.json();
      store.userAuthorised = true;
      store.username = data.user.username;
      store.email = data.user.email;
      store.picture = "http://127.0.0.1:8000" + data.profile_picture;
      console.log("logged in as " + store.username);
    }
  } catch (error) {
    console.log(error);
  }
});
</script>

<template>
  <main class="d-flex flex-column">
    <HeaderComp v-if="['login', 'register'].includes($route.name) == false" />

    <RouterView />
  </main>
</template>

<style>
body {
  background: #3b1a99;
}

main {
  min-height: 100vh;
  max-width: 100vw;
  background: linear-gradient(145deg, #5c2a84 23%, 55%, #3b1a99 85%);
}
</style>
