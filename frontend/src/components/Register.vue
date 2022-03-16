<template>
  <main>
    <v-container fluid fill-height class="loginOverlay">
      <v-layout flex align-center justify-center>
        <v-flex xs12 sm4 elevation-6>
          <v-toolbar
            class="pt-5 darken-4 d-flex justify-space-around"
            style="background-color: #fc0"
          >
            <v-toolbar-title class="white--text mb-6">
              <h4>Регистрация в Web WhatsApp API</h4>
            </v-toolbar-title>
          </v-toolbar>
          <v-card>
            <v-card-text>
              <v-container>
                <v-row>
                  <formfield
                    type_input="input"
                    key_label="email"
                    labels="Email"
                    @changeInput="changeInput"
                    :error="error"
                    :cols="12"
                  />
                  <formfield
                    type_input="input"
                    key_label="username"
                    labels="Имя пользователя"
                    @changeInput="changeInput"
                    :error="error"
                    :cols="12"
                  />
                  <formfield
                    type_input="password"
                    key_label="password"
                    labels="Пароль"
                    @changeInput="changeInput"
                    :error="error"
                    :cols="12"
                  />
                  <v-layout justify-space-between>
                    <v-btn @click="signUp">Регистрация</v-btn>
                    <a href="/login">Вернуться назад</a>
                  </v-layout>
                </v-row>
              </v-container>
            </v-card-text>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </main>
</template>

<script>
import $ from "jquery";
import formfield from "../components/FormField";
export default {
  components: { formfield },
  metaInfo: {
    title: "Регистрация",
  },
  data() {
    return {
      userData: {},
      error: "",
    };
  },
  methods: {
    changeInput(key, value) {
      this.userData[key] = value;
    },
    signUp() {
      $.post(this.$store.state.backend_url + "auth/users/", this.userData, (data) => {
        this.$router.push("/login");
      }).fail((response) => {
        this.error = response.responseJSON;
        console.log(this.error);
      });
    },
  },
};
</script>
