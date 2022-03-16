<template>
  <div>
    <v-navigation-drawer v-model="drawer" :mini-variant.sync="mini" permanent app>
      <p style="text-align: center; margin: 0">
        <v-sheet class="pa-4">
          <div v-if="mini === false">
            <v-avatar class="mb-4" color="grey darken-1" size="64">
              <v-img lazy-src="http://localhost:8080/favicon.png" src="http://localhost:8080/favicon.png" alt="http://localhost:8080/favicon.png"></v-img>
            </v-avatar>

            <div v-if="user.first_name === '' && user.last_name === ''" class="mb-2">
              {{ user.username }} ({{ user.email }})
            </div>
            <div v-else class="mb-2">{{ user.first_name }} {{ user.last_name }}</div>
            <v-btn color="#fc0" @click="logout" class="button-nav" title="Выход">
              <v-icon>mdi-exit-run</v-icon>
            </v-btn>
            <v-btn color="#fc0" @click="theme" class="button-nav" title="Сменить тему">
              <v-icon>mdi-theme-light-dark</v-icon>
            </v-btn>
            <v-btn
              color="#fc0"
              class="button-nav"
              title="Свернуть панель"
              @click.stop="mini = !mini"
            >
              <v-icon>mdi-chevron-left</v-icon>
            </v-btn>
          </div>
          <div v-else style="margin-left: -10px">
            <v-avatar color="grey darken-1" size="44">
              <v-img lazy-src="http://localhost:8080/favicon.png" src="http://localhost:8080/favicon.png" alt="http://localhost:8080/favicon.png"></v-img>
            </v-avatar>
          </div>
        </v-sheet>
      </p>

      <v-divider></v-divider>

      <v-list>
        <v-list-item v-for="[icon, link, text] in links" :key="icon" link :to="link">
          <v-list-item-icon>
            <v-icon>{{ icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>{{ text }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
  </div>
</template>

<script>
import $ from "jquery";
export default {
  data: () => ({
    drawer: null,
    links: [
      ["mdi-home", "/", "Домашняя страница"],
      ["mdi-account-cog", "/profile", "Настройки профиля"],
    ],
    mini: true,
    user: [],
  }),
  created() {
    //this.username = localStorage.getItem("username");
    this.token = localStorage.getItem("auth-token");
    $.ajaxSetup({
      headers: {
        Authorization: `Token ${localStorage.getItem("auth-token")}`,
      },
    });
    this.userinfo();
  },
  methods: {
    userinfo() {
      $.get(this.$store.state.backend_url + "api/user/", (data) => {
        this.user = data[0];
      });
    },
    logout() {
      $.post(
        this.$store.state.backend_url + "auth/token/logout/",
        this.token,
        (data) => {}
      );
      localStorage.removeItem("auth-token");
      localStorage.removeItem("username");
      window.location = "/login";
    },
    theme() {
      if (localStorage.getItem("theme") !== "true") {
        localStorage.setItem("theme", true);
      } else {
        localStorage.removeItem("theme");
      }
      location.reload();
    },
  },
};
</script>
<style scoped>
.button-nav {
  margin-left: 5px;
}
</style>
