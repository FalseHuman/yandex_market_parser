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
                  @click="userMarketCreate('link')"
                  title="Добавить ссылку"
                >
                  <v-icon dark>mdi-plus</v-icon>
                </v-btn>
                <v-btn
                  color="#fc0"
                  dark
                  small
                  fab
                  style="margin-bottom: 10px; margin-top: 0; margin-left: 5px;"
                  @click="searchGroupLink()"
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
                            type_input="select"
                            key_label="group_link"
                            :arr_select="group_name"
                            labels="Группа товара"
                            :error="error"
                            @changeInput="changeInput"
                            :cols="12"
                          />
                        <formfield
                            v-for="i in Object.keys(createData)"
                            type_input="input"
                            :key_label="i"
                            :labels="createData[i].label"
                            :error="error"
                            @changeInput="changeInput"
                            :cols="12"
                            v-show="i !== 'labels' && i!=='price_link' && i!=='id' && i!=='analog_link' &&  i!=='group_link'"
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
            <v-dialog
              v-model="group"
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
                  @click="userMarketCreate('group')"
                  title="Добавить группу"
                >
                  <v-icon dark>mdi-text-box-multiple-outline</v-icon>
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
                  <span class="text-h5">Добавить группу</span>
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
                            v-show="i !== 'labels' && i!=='id'"
                          />
                    </v-row>
                  </v-container>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="blue darken-1" text @click="group = false">Закрыть</v-btn>
                  <v-btn color="blue darken-1" @click="userDataMarketGroupSend()" text >Сохранить</v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-row>
        </div>
          <v-row>
            <formfield
              type_input="select"
              key_label="group_link"
              :arr_select="group_name"
              labels="Группа товара"
              :model="group_link_storage"
              :error="error"
              @changeInput="changeInput"
              sm="6"
              md="6"
              :cols="12"
              :search="true"
              />
              <formfield
              type_input="select"
              key_label="market_link"
              :arr_select="market_name"
              labels="Название товара"
              :cols="12"
              sm="6"
              md="6"
              :error="error"
              @changeInput="changeInput"
              :search="true"
              />
          </v-row>
              
        <p  class="text-center centered" v-show="user_link_market.length === 0">Тут пока нет ни одной ccылки:(</p> 
        <v-row>
          <v-col  cols="12" v-show="user_link_market.length !== 0">
            <v-col
            v-if="group_search !==''">Показаны результаты для {{text_search}}
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
                          v-if="key.name !== ''">Название товара: {{key.name}}</v-list-item-subtitle>
                        </v-list-item-content>
                        <v-col cols="auto" class="d-flex">
                          <v-dialog transition="dialog-bottom-transition" :fullscreen="true">
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
                                    <v-btn color="error" class="ml-2" @click="deleteLink('link', key.id)">
                                      <v-icon>mdi-delete</v-icon>
                                    </v-btn>
                                  </v-list>
                                </v-menu>
                              </div>
                              <div v-else>
                                <v-btn color="#fc0" dark v-bind="attrs" v-on="on">
                                  <v-icon>mdi-information</v-icon>
                                </v-btn>
                                <v-btn color="error" class="ml-2" @click="deleteLink('link', key.id)">
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
                                      <a :href="key.link" target="_blank">Ссылка на товар на Маркете</a> ({{key.name}})<br>
                                      <hr>
                                      <span>Не возможно построить график, нет данных.</span><br>
                                    </div>
                                    <div v-else-if="key.price_link.length !== 0">
                                      <a :href="key.link" target="_blank">Ссылка на товар на Маркете</a> ({{key.name}})<br>
                                      <monthly-sales-chart :data="parserCharts(key.price_link, key.analog_link, key.name)" :arr_length="parserCharts(key.price_link, key.analog_link, key.name).length" :theme="themeChart()" />
                                    </div>
                                    <v-dialog
                                            v-model="analog_add"
                                            persistent
                                            max-width="600px"
                                            :fullscreen="$vuetify.breakpoint.mobile"
                                            >
                                              <template v-slot:activator="{ on, attrs }">
                                                <v-btn
                                                  text
                                                  v-bind="attrs"
                                                  v-on="on"
                                                  @click="userMarketCreate('analog_link')"
                                                  title="Изменить"
                                                  >Добавить аналог
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
                                                  <span class="text-h5">Добавить аналог</span>
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
                                                      v-show="i !== 'labels' && i!=='id' && i!=='analog_link' && i!='analog_link_price'"
                                                    />
                                                  </v-row>
                                                </v-container>
                                                </v-card-text>
                                                <v-card-actions>
                                                  <v-spacer></v-spacer>
                                                  <v-btn color="blue darken-1" text @click="analog_add = false">Закрыть</v-btn>
                                                  <v-btn color="blue darken-1" @click="userAnalogSend(key.name)" text >Сохранить</v-btn>
                                                </v-card-actions>
                                                </v-card>
                                                </v-dialog>
                                    <div v-if="key.analog_link.length === 0">
                                      <span>Аналоги товара не были добавлены</span>
                                    </div>
                                    <div v-else>
                                    <span>Аналоги </span>
                                      <div v-for="analog in key.analog_link">
                                        <a :href="analog.analog_link" target="_blank">Ссылка на товар на Маркете</a> ({{analog.analog_name}})                                        <v-btn
                                                  text
                                                  color="error"
                                                  @click="deleteLink('analog_link', analog.id)"
                                                  title="Удалить"
                                                  >Удалить</v-btn><br>
                                        <!-- <monthly-sales-chart :categories="parserCharts(analog.analog_link_price, 'analog_data_parser_price')" :data="parserCharts(analog.analog_link_price, 'analog_price')" :theme="themeChart()" /> -->
                                                  
                                    </div>
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
                                                  @click="userMarketCreate('link')"
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
                                                        type_input="select"
                                                        key_label="group_link"
                                                        :arr_select="group_name"
                                                        labels="Группа товара"
                                                        :error="error"
                                                        @changeInput="changeInput"
                                                        :model="key.group_link"
                                                        :cols="12"
                                                      />                                                
                                                    <formfield
                                                      v-for="i in Object.keys(createData)"
                                                      type_input="input"
                                                      :key_label="i"
                                                      :labels="createData[i].label"
                                                      :error="error"
                                                      @changeInput="changeInput"
                                                      :model="key[i]"
                                                      :cols="12"
                                                      v-show="i !== 'labels' && i!=='price_link' && i!=='id' && i!=='link' && i!=='analog_link' && i!=='group_link'"
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
    group_market: [],
    group_link_storage: '',
    analog_add: false,
    dialog_change: false,
    group_search: null,
    search: null,
    group: false,
    dialog: false,
    group_name: [],
    market_name: [],
    text_search: '',
    search_market_link: [],
    last_price_update: "",
    userDataMarketLink: {},
  }),
  created() {
    this.searchGroupLink()
    this.loadUserLinkMarket()
    this.loadGroupMarket()
  },
  mounted() {
  },
  methods: {
    userMarketCreate(link) {
      var self = this;
      $.ajax({
        url: this.$store.state.backend_url + "api/" + link + "/",
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
    parserCharts(arr, arr_analog, key_name){
      let new_arr = []
      let name_price = ''
      let arr_price = []
      let categories_price = []
      let categories_analog_price =[]
      // console.log('chart', arr, arr_analog)
      for(let i in arr){
        name_price = key_name
        categories_price.push(this.formatDateChart(arr[i].data_parser_price))
        arr_price.push(Number(arr[i].price))
      }
      arr_price = [
          {
              'name': name_price,
              'data': arr_price
        }]
      for(let i in arr_analog){
        if(arr_analog[i].analog_link_price.length !== 0){
          let arr_analog_price= []
        for(let z in arr_analog[i].analog_link_price){
          categories_analog_price.push(this.formatDateChart(arr_analog[i].analog_link_price[z].analog_data_parser_price))
          arr_analog_price.push(arr_analog[i].analog_link_price[z].analog_price)
        }
        // console.log(arr_analog_price)
        arr_price.push({name: arr_analog[i].analog_name, data: arr_analog_price})
        }
      }
        // console.log(categories_price, categories_analog_price)
       if(categories_price.length > categories_analog_price.length){
          arr_price.push({'categories': categories_price}) 
        } else{
          arr_price.push({'categories': categories_analog_price}) 
      }
      return arr_price
    },
    loadUserLinkMarket() {
      this.load = true;
      $.get(this.$store.state.backend_url + "api/link/?group_link__group_name=null", data => {

        this.user_link_market = data;

        this.load = false;
      });
    },
    loadGroupMarket() {
      this.load = true;
      $.get(this.$store.state.backend_url + "api/group/", data => {

        this.group_market = data;
        for(let i in this.group_market){
          this.group_name.push(this.group_market[i].group_name)
        }
        this.load = false;
      });
    },
    firstUpperWord(word) {
      return word[0].toUpperCase() + word.substr(1).toLowerCase();
    },
    searchGroupLink(get, value){
      if (get===undefined){
        get = '?group_link__group_name=null'
      }
      $.get(this.$store.state.backend_url + "api/link/" + get, data => {
        this.user_link_market = data;
        // console.log(this.search_market_link)
        for(let i in this.user_link_market ){
          if(this.user_link_market[i].group_link === value){
            this.market_name.push(this.user_link_market[i].name)
          }
        }
        
      });
    },
    changeInput(key, value, search) {
      if(value === undefined || value === null){
        value = null
      }
      if(search === true){
        if(key == 'group_link'){         
          this.search = value
          this.text_search = 'группы/групп'
          this.group_search = "?group_link__group_name="  + value
          this.searchGroupLink(this.group_search, value)
        }else{
          if (value != null){
            this.text_search = 'товара/товаров'
            let group_market_search = this.group_search + "&name=" + value
            this.searchGroupLink(group_market_search)
          } else{
            this.text_search = 'группы/групп'
            this.searchGroupLink(this.group_search, value) 
          }
        }
        // console.log(this.group_search)
      }
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
            //// console.log(this.error);
        }
      );
    },
    userAnalogSend(parent_name) {
      this.userDataMarketLink['analog_link'] = parent_name

      $.post(this.$store.state.backend_url + "api/analog_link/", this.userDataMarketLink, data => {})
      .done(response => {
         var self = this;
        self.analog_add= false
         self.loadUserLinkMarket()
      }
      )
      .fail(
        response => {
            this.error = response.responseJSON;
            //// console.log(this.error);
        }
      );
    },
    userDataMarketGroupSend(dict) {
      $.post(this.$store.state.backend_url + "api/group/", this.userDataMarketLink, data => {})
      .done(response => {
         var self = this;
         self.group = false
         self.loadGroupMarket()
      }
      )
      .fail(
        response => {
            this.error = response.responseJSON;
            //// console.log(this.error);
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
          window.location.reload()
        },
        error: function(response) {
          alert(response.responseJSON);
        }
      });
    },
    deleteLink(link,id) {
      var self = this
      $.ajax({
        url: this.$store.state.backend_url + "api/" + link +"/" + id +"/",
        type: "DELETE",
        success: function(data) {
          self.loadUserLinkMarket()
          window.location.reload()
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
