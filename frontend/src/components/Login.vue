<template>
  <main>
    <v-container fluid fill-height class="loginOverlay">
      <v-layout flex align-center justify-center>
        <v-flex xs12 sm4 elevation-6>
          <v-alert dense v-model="alert" outlined type="error" dismissible>{{
            non_field_errors
          }}</v-alert>
          <v-toolbar
            class="pt-5 darken-4 d-flex justify-space-around"
            style="background-color: #fc0"
          >
            <v-toolbar-title class="white--text mb-6">
              <h4>Вход в Парсер Яндекс.Маркет</h4>
            </v-toolbar-title>
          </v-toolbar>
          <v-card>
            <v-card-text class="pt-4">
              <div>
                <v-form ref="form">
                  <v-text-field label="Логин" v-model="username" required></v-text-field>
                  <v-text-field
                    label="Пароль"
                    v-model="password"
                    :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                    :type="showPassword ? 'text' : 'password'"
                    required
                    @click:append="showPassword = !showPassword"
                  ></v-text-field>
                  <v-layout justify-space-between>
                    <v-btn color="#fc0" @click="signIn">Войти</v-btn>
                    <p>
                      <a href="/reset-password">Забыли пароль? </a>
                      <a href="/registraitions">Регистрация</a>
                    </p>
                  </v-layout>

                  <v-layout justify-space-between>
                    <!--  <p>
                      Войти с помощью:
                      <a
                        :href="`https://oauth.vk.com/authorize?client_id=8035574&display=page&redirect_uri=${
                          this.$store.state.domain_url
                        }vk-callback&scope=email&response_type=code&v=5.131&state=${getRandomIntInclusive(
                          100000,
                          999999
                        )}`"
                      >
                        <img
                          src="https://vk.com/images/icons/pwa/apple/default.png?11"
                          style="border-radius: 5px; margin-right: 5px;"
                          witdh="25px"
                          height="25px"
                          alt="VK"
                          title="Войти через Вконтакте"
                        />
                      </a>
                    </p> -->
                  </v-layout>
                </v-form>
              </div>
            </v-card-text>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </main>
</template>

<script>
import $ from "jquery";
export default {
  metaInfo: {
    title: "Вход в систему",
  },
  data() {
    return {
      username: "",
      password: "",
      non_field_errors: "",
      alert: null,
      showPassword: false,
    };
  },
  created() {
    this.cookies();
    this.getRandomIntInclusive();
  },
  methods: {
    /* Функиция генерирования state для VK */
    getRandomIntInclusive(min, max) {
      min = Math.ceil(min);
      max = Math.floor(max);
      return Math.floor(Math.random() * (max - min + 1) + min);
    },
    cookies() {
      var token = document.cookie.match(new RegExp("(^| )" + "auth_token" + "=([^;]+)"));
      if (token != null) {
        localStorage.setItem("auth-token", token[2]);
        this.$router.push("/");
        location.reload();
      }
    },
    signIn() {
      const credentials = {
        username: this.username,
        password: this.password,
      };
      $.post(this.$store.state.backend_url + "auth/token/login/", credentials, (data) => {
        localStorage.setItem("auth-token", data.auth_token);
        localStorage.setItem("username", this.username);
        this.$router.push("/");
        location.reload();
      }).fail((response) => {
        let json = response.responseJSON;
        this.non_field_errors = json.non_field_errors.toString();
        this.alert = true;
      });
    },
  },
};
</script>
