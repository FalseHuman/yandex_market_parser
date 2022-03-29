<template>
  <v-app id="inspire">
    <router-view />
  </v-app>
</template>

<script>
import adapter from "webrtc-adapter";
import $ from "jquery";
export default {
  created() {
    if (localStorage.getItem("auth-token")) {
      $.ajaxSetup({
        headers: {
          Authorization: "Token " + localStorage.getItem("auth-token"),
        },
      });
    }
    this.themeBrowser();
    if (localStorage.getItem("auth-token")) {
      this.tokenGet();
    }
  },
  methods: {
    themeBrowser() {
      //// console.log(adapter.browserDetails.browser);
      if (window.matchMedia) {
        if (
          window.matchMedia("(prefers-color-scheme: dark)").matches &&
          localStorage.getItem("theme") !== "true"
        ) {
          localStorage.setItem("theme", true);
        } else if (
          window.matchMedia("(prefers-color-scheme: light)").matches &&
          localStorage.getItem("theme") !== "true"
        ) {
          localStorage.removeItem("theme");
        }
      }
    },
    tokenGet() {
      $.post(
        this.$store.state.backend_url + "api/token/",
        { "auth-token": localStorage.getItem("auth-token") },
        (data) => {}
      ).fail((response) => {
        if (localStorage.getItem("auth-token")) {
          localStorage.removeItem("auth-token");
          this.$router.push("/login");
        }
      });
    },
  },
};
</script>
