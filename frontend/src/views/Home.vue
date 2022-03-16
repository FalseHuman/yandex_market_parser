<template>
  <v-main>
    <div v-if="load === true">
      <loading />
    </div>
    <div v-else>
      <NavAndFooter />
            <v-container class="py-8 px-6" fluid>
        <div>
          <v-row justify="center">
            <v-dialog
              v-model="dialog"
              persistent
              max-width="600px"
              :fullscreen="$vuetify.breakpoint.mobile"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  color="#fc0"
                  dark
                  small
                  fab
                  v-bind="attrs"
                  v-on="on"
                  style="margin-bottom: 10px; margin-top: 0; margin-left: 5px;"
                  @click="userLinkMarketCreate()"
                  title="Добавить"
                >
                  <v-icon dark>mdi-plus</v-icon>
                </v-btn>
                <v-btn
                  color="#fc0"
                  dark
                  small
                  fab
                  style="margin-bottom: 10px; margin-top: 0; margin-left: 5px;"
                  @click="loadUserLinkMarket()"
                  title="Обновить"
                >
                  <v-icon dark>mdi-refresh</v-icon>
                </v-btn>
              </template>
              <v-card>
              <v-banner single-line v-if="error!==''">
                  <v-icon slot="icon" color="red" size="36">mdi-comment-alert</v-icon>Заполните все поля!
                  <template v-slot:actions>
                    <v-btn color="primary" text @click="error=''">Закрыть</v-btn>
                  </template>
                </v-banner>
                <v-card-title>
                  <span class="text-h5">Добавить cсылку</span>
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
                            :cols="12"
                            v-show="i !== 'labels' && i!=='price_link' && i!=='id'"
                          />
                    </v-row>
                  </v-container>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="blue darken-1" text @click="dialog = false">Закрыть</v-btn>
                  <v-btn color="blue darken-1" @click="userDataMarketLinkSend()" text >Сохранить</v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-row>
        </div>
        <p  class="text-center centered" v-show="user_link_market.length === 0">Тут пока нет ни одной ccылки:(</p> 
        <v-row>
          <v-col  cols="12" v-show="user_link_market.length !== 0">
            <v-col
            >
              <v-card>
                <v-list two-line>
                  <template >
                    <div>
                      <v-list-item v-for="key in user_link_market">
                        <v-list-item-icon>
                        <v-icon>mdi-link</v-icon>
                        </v-list-item-icon>

                        <v-list-item-content>
                          <v-list-item-title><a :href="key.link" target="_blank">Ссылка на товар на Маркете</a></v-list-item-title>

                          <v-list-item-subtitle
                            xs12
                            sm4
                            elevation-6
                          v-if="key.comment !== ''">Комментарий: {{key.comment}}</v-list-item-subtitle>
                        </v-list-item-content>
                        <v-col cols="auto" class="d-flex">
                          <v-dialog transition="dialog-bottom-transition" max-width="600">
                            <template v-slot:activator="{ on, attrs }">
                              <div v-if="$vuetify.breakpoint.mobile">
                                <v-menu>
                                  <template v-slot:activator="{ on, attrs }">
                                    <v-btn color="success" v-bind="attrs" v-on="on">
                                      <v-icon>mdi-eye</v-icon>
                                    </v-btn>
                                  </template>

                                  <v-list>
                                    <v-btn color="#fc0"  dark v-bind="attrs" v-on="on">
                                      <v-icon>mdi-information</v-icon>
                                    </v-btn>
                                    <v-btn color="error" class="ml-2" @click="deleteLink(key.id)">
                                      <v-icon>mdi-delete</v-icon>
                                    </v-btn>
                                  </v-list>
                                </v-menu>
                              </div>
                              <div v-else>
                                <v-btn color="#fc0" dark v-bind="attrs" v-on="on">
                                  <v-icon>mdi-information</v-icon>
                                </v-btn>
                                <v-btn color="error" class="ml-2" @click="deleteLink(key.id)">
                                  <v-icon>mdi-delete</v-icon>
                                </v-btn>
                              </div>
                            </template>
                            <template v-slot:default="dialog">
                              <v-card>
                                <v-card-title dark>
                                  <span class="text-h5">
                                  Данные о товаре
                                  </span>
                                </v-card-title>
                                <v-card-text>
                                  <div class="text-h5 pa-5" >
                                    <div v-if="key.price_link.length === 0">
                                    <a :href="key.link" target="_blank">Ссылка на товар на Маркете</a><br>
                                    <span>Комментарий: {{key.comment}}</span><br>
                                    <hr>
                                    <span>Не возможно построить график, нет данных.</span><br>
                                    </div>
                                    <div v-else light>
                                    <a :href="key.link" target="_blank">Ссылка на товар на Маркете</a><br>
                                    <span>Комментарий: {{key.comment}}</span><br>
                                    <monthly-sales-chart :categories="parserCharts(key.price_link, 'data_parser_price')" :data="parserCharts(key.price_link, 'price')" :theme="themeChart()" />
                                    </div>
                                  </div>
                                </v-card-text>
                                <v-card-actions class="justify-end">
                                            <v-dialog
                                            v-model="dialog_change"
                                            persistent
                                            max-width="600px"
                                            :fullscreen="$vuetify.breakpoint.mobile"
                                            >
                                              <template v-slot:activator="{ on, attrs }">
                                                <v-btn
                                                  text
                                                  v-bind="attrs"
                                                  v-on="on"
                                                  @click="userLinkMarketCreate()"
                                                  title="Изменить"
                                                  >Изменить
                                                  </v-btn>
                                              </template>
                                              <v-card>
                                                <v-banner single-line v-if="error!==''">
                                                  <v-icon slot="icon" color="red" size="36">mdi-comment-alert</v-icon>Заполните все поля!
                                                  <template v-slot:actions>
                                                      <v-btn color="primary" text @click="error=''">Закрыть</v-btn>
                                                  </template>
                                                </v-banner>
                                                <v-card-title>
                                                  <span class="text-h5">Редактировать данные</span>
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
                                                      :model="key[i]"
                                                      :cols="12"
                                                      v-show="i !== 'labels' && i!=='price_link' && i!=='id' && i!=='link'"
                                                    />
                                                  </v-row>
                                                </v-container>
                                                </v-card-text>
                                                <v-card-actions>
                                                  <v-spacer></v-spacer>
                                                  <v-btn color="blue darken-1" text @click="dialog_change = false">Закрыть</v-btn>
                                                  <v-btn color="blue darken-1" @click="updateLink(key.id)" text >Сохранить</v-btn>
                                                </v-card-actions>
                                                </v-card>
                                                </v-dialog>
                                  <v-btn text  @click="dialog.value = false">Закрыть</v-btn>
                                </v-card-actions>
                              </v-card>
                            </template>
                          </v-dialog>
                        </v-col>
                      </v-list-item>
                    </div>
                  </template>
                </v-list>
              </v-card>
            </v-col>
          </v-col>
        </v-row>
      </v-container>
    </div>
  </v-main>
    </div>
  </v-main>
</template>

<script>
import $ from "jquery";
import formfield from "../components/FormField";
import NavAndFooter from "../components/NavAndFooter";
import Loading from "../components/Loading";
import MonthlySalesChart from "../components/MonthlySalesChart";


export default {
  components: { formfield, NavAndFooter, Loading, MonthlySalesChart},
  metaInfo: {
    title: "Домашняя страница - Парсер Яндекс.Маркет",
  },
  name: "Home",
  data: () => ({
    load: null,
    createData: {},
    error: "",
    user_link_market: [],
    dialog_change: false,
    dialog: false,
    last_price_update: "",
    userDataMarketLink: {},
  }),
  created() {
    this.loadUserLinkMarket()
  },
  mounted() {
  },
  methods: {
    userLinkMarketCreate() {
      var self = this;
      $.ajax({
        url: this.$store.state.backend_url + "api/link/",
        type: "OPTIONS",
        success: function (data) {
          self.createData = data.actions.POST;
        },
        error: function (response) {
          alert(response.responseJSON);
        },
      });
    },
    themeChart(){
      if (localStorage.getItem('theme') === 'true'){
        return 'dark'
      } else{
        return 'light'
      }
    },
    formatDate(date) {
      const options = {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "numeric",
        minute: "numeric"
      };
      return new Date(date).toLocaleDateString("ru", options);
    },
    formatDateChart(date) {
      const options = {
        year: "numeric",
        month: "short",
        day: "numeric",
      };
      return new Date(date).toLocaleDateString("ru", options);
    },
    parserCharts(arr, key){
      let new_arr = []
      for(let i in arr){
        if(key === 'data_parser_price' ){
          new_arr.push(this.formatDateChart(arr[i][key]))
        } else{
          new_arr.push(arr[i][key])
        }
      }
      return new_arr
    },
    loadUserLinkMarket() {
      this.load = true;
      $.get(this.$store.state.backend_url + "api/link/", data => {

        this.user_link_market = data;

        this.load = false;
      });
    },
    firstUpperWord(word) {
      return word[0].toUpperCase() + word.substr(1).toLowerCase();
    },
    changeInput(key, value) {
      //console.log(key, value)
      this.userDataMarketLink[key] = value;
    },

    userDataMarketLinkSend(dict) {
      $.post(this.$store.state.backend_url + "api/link/", this.userDataMarketLink, data => {})
      .done(response => {
         var self = this;
         self.dialog = false
         self.loadUserLinkMarket()
      }
      )
      .fail(
        response => {
            this.error = response.responseJSON;
            //console.log(this.error);
        }
      );
    },
    updateLink(id) {
      var self = this
      $.ajax({
        url: this.$store.state.backend_url + "api/link/" + id +"/",
        type: "PUT",
        data: self.userDataMarketLink,
        success: function(data) {
          self.loadUserLinkMarket()
        },
        error: function(response) {
          alert(response.responseJSON);
        }
      });
    },
    deleteLink(id) {
      var self = this
      $.ajax({
        url: this.$store.state.backend_url + "api/link/" + id +"/",
        type: "DELETE",
        success: function(data) {
          self.loadUserLinkMarket()
        },
        error: function(response) {
          alert(response.responseJSON);
        }
      });
    },
  },
};
</script>
<style>
.centered {
  width: 100%;
  height: 100%;
  position: absolute;
  top: 50%;
  left: 0;
  overflow: auto;
}
</style>
