<template>
  <main>
    <v-container fluid fill-height class="loginOverlay">
      <v-layout flex align-center justify-center>
        <v-flex xs12 sm4 elevation-6>
          <!--<v-alert
            dense
            outlined
            type="error"
            dismissible
            v-model="alert"
          >{{ non_field }}</v-alert>-->
          <v-toolbar
            class="pt-5 darken-4 d-flex justify-space-around"
            style="background-color: #fc0"
          >
            <v-toolbar-title class="white--text mb-6">
              <h4>Восстановление</h4>
            </v-toolbar-title>
          </v-toolbar>
          <v-card>
            <v-card-text class="pt-4">
              <div v-show="email_check !== true && token !== true">
                <h3 style="text-align: center">
                  <strong>Получение токена</strong>
                </h3>
                <p>
                  Пожалуйста, укажите эл.почту, которую вы использовали при регистрации на
                  сайте. На неё придёт код восстановления.
                </p>
                <v-form ref="form">
                  <formfield
                    type_input="input"
                    key_label="email"
                    labels="E-mail"
                    @changeInput="changeInput"
                    :error="error"
                    :cols="14"
                  />
                  <v-layout justify-space-between>
                    <template>
                      <v-btn color="#fc0" @click="checkData('email')">Отправить</v-btn>
                      <a href="/login">Вернуться назад</a>
                    </template>
                  </v-layout>
                </v-form>
              </div>
              <div v-show="email_check === true">
                <h3 style="text-align: center">
                  <strong>Ввод токена</strong>
                </h3>
                <p>Вставьте токен в форму без пробелов.</p>
                <v-form ref="form">
                  <formfield
                    type_input="password"
                    key_label="token"
                    labels="Токен"
                    @changeInput="changeInput"
                    :error="error"
                    :cols="14"
                  />
                  <v-layout justify-space-between>
                    <v-btn color="#fc0" @click="checkData('token')">Обновить</v-btn>
                    <a href="/login">Вернуться назад</a>
                  </v-layout>
                </v-form>
              </div>

              <div v-show="email_check !== true && token === true">
                <p>Введите новые данные.</p>
                <v-form ref="form">
                  <formfield
                    type_input="input"
                    key_label="login"
                    labels="Имя пользователя/Логин"
                    @changeInput="changeInput"
                    :error="error"
                    :cols="12"
                  />
                  <formfield
                    type_input="password"
                    key_label="password_1"
                    labels="Введите новый пароль"
                    @changeInput="changeInput"
                    :error="error"
                    :cols="12"
                  />
                  <formfield
                    type_input="password"
                    key_label="password_2"
                    labels="Повторите новый пароль"
                    @changeInput="changeInput"
                    :error="error"
                    :cols="12"
                  />
                  <!--<v-text-field label="Логин" v-model="username" required></v-text-field>
                  <v-text-field label="Пароль" v-model="password" type="password" required></v-text-field>
                  <v-text-field
                    label="Повторите пароль"
                    v-model="new_password"
                    type="password"
                    required
                  ></v-text-field>-->
                  <v-layout justify-space-between>
                    <v-btn color="#fc0" @click="sendNewPassword">Обновить</v-btn>
                    <a href="/login">Вернуться назад</a>
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
import formfield from "../components/FormField";
export default {
  components: { formfield },
  metaInfo: {
    title: "Восстановление",
  },
  data() {
    return {
      dialog: false,
      error: "",
      email: "",
      email_check: null,
      token: null,
      data_user: {},
    };
  },
  methods: {
    changeInput(key, value) {
      this.data_user[key] = value;
    },
    checkData(key) {
      $.post(
        this.$store.state.backend_url + "api/check_" + key + "/",
        this.data_user,
        (data) => {
          if (key === "email") {
            this.email_check = true;
          } else {
            this.email_check = false;
            this.token = true;
          }
        }
      ).fail((response) => {
        this.error = response.responseJSON;
        // console.log(this.error);
      });
    },
    sendNewPassword() {
      $.post(
        this.$store.state.backend_url + "api/password/change_password/change_password/",
        this.data_user,
        (data) => {
          this.$router.push("/login");
        }
      ).fail((response) => {
        this.error = response.responseJSON;
        //// console.log(this.error)
      });
    },
  },
};
</script>
