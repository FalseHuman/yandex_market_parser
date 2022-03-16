<template>
  <v-main>
    <div v-if="load === true">
      <loading />
    </div>
    <div v-else>
      <NavAndFooter />
      <v-card class="mx-auto" max-width="100%" tile>
        <v-col>
          <p style="text-align: center; margin: 0">
            <v-avatar color="grey darken-1" size="100">
              <v-img lazy-src="http://localhost:8080/favicon.png" src="http://localhost:8080/favicon.png" alt="http://localhost:8080/favicon.png"></v-img>
            </v-avatar>
          </p>
        </v-col>
        <v-list-item color="rgba(0, 0, 0, .4)">
          <v-list-item-content justify="center">
            <v-list-item-title
              class="title"
              style="text-align: center"
              v-for="label in Object.keys(labels)"
              :key="label"
              >{{ firstUpperWord(labels[label]) }}: {{ user[label] }}</v-list-item-title
            >
            <div style="margin-top: 15px; margin-bottom: 10px">
              <v-row justify="center">
                <v-dialog v-model="dialog" persistent max-width="600px">
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn
                      color="#fc0"
                      dark
                      v-bind="attrs"
                      v-on="on"
                      @click="userform()"
                      >Pедактировать</v-btn
                    >
                  </template>
                  <v-card>
                    <v-card-title>
                      <span class="text-h5">Редактировать профиль</span>
                    </v-card-title>
                    <v-card-text>
                      <v-container>
                        <v-row>
                          <formfield
                            v-for="i in Object.keys(createData)"
                            type_input="input"
                            :key_label="i"
                            :labels="createData[i].label"
                            :error="error"
                            @changeInput="changeInput"
                            :model="user[i]"
                            :cols="12"
                            v-show="i !== 'labels'"
                          />
                        </v-row>
                      </v-container>
                    </v-card-text>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn color="blue darken-1" text @click="dialog = false"
                        >Закрыть</v-btn
                      >
                      <v-btn color="blue darken-1" type="submit" text @click="updateUser"
                        >Сохранить</v-btn
                      >
                    </v-card-actions>
                  </v-card>
                </v-dialog>
              </v-row>
            </div>
          </v-list-item-content>
        </v-list-item>
      </v-card>
    </div>
  </v-main>
</template>
<script>
import $ from "jquery";
import NavAndFooter from "../components/NavAndFooter";
import Loading from "../components/Loading";
import formfield from "../components/FormField";
export default {
  components: { NavAndFooter, Loading, formfield },
  metaInfo: {
    title: "Профиль - Парсер Яндекс.Маркет",
  },
  data() {
    return {
      load: null,
      user: [],
      dialog: false,
      labels: [],
      createData: {},
      error: "",
      userData: {},
    };
  },
  created() {
    this.users();
  },
  methods: {
    onFileChange(file) {
      this.link = file;
    },
    users() {
      this.load = true;
      $.get(this.$store.state.backend_url + "api/user/", (data) => {
        this.user = data[0];
        (this.labels = this.user.labels), (this.load = false);
      });
    },
    userform() {
      var self = this;
      $.ajax({
        url: this.$store.state.backend_url + "api/user/",
        type: "OPTIONS",
        success: function (data) {
          self.createData = data.actions.POST;
        },
        error: function (response) {
          alert(response.responseJSON);
        },
      });
    },
    firstUpperWord(word) {
      return word[0].toUpperCase() + word.substr(1).toLowerCase();
    },
    changeInput(key, value) {
      this.userData[key] = value;
    },
    updateUser() {
      //console.log(this.row)
      var self = this;
      $.ajax({
        url: this.$store.state.backend_url + "api/update_profile/",
        data: this.userData,
        type: "PUT",
        success: function (data) {
          location.reload();
        },
        error: function (response) {
          //console.log(this.data);
          self.error = response.responseJSON;
          /*           for (let key in err) {
            alert(key, err[key].toString());
          } */
        },
      });
    },
  },
};
</script>
