import Vue from 'vue'
import App from './App.vue'
import router from './router'
import Meta from 'vue-meta';
import vuetify from './plugins/vuetify'
import store from './store'
import VueApexCharts from 'vue-apexcharts'
Vue.use(VueApexCharts)

Vue.component('apexchart', VueApexCharts)

Vue.config.productionTip = false
Vue.use(Meta);

new Vue({
  vuetify,
  router,
  store,
  render: h => h(App)
}).$mount('#app')
