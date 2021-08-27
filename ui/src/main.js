import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
import {globalFunctions} from './globalFunctions'

Vue.config.productionTip = false
Vue.prototype.globalFunctions = globalFunctions;
Vue.prototype.apiUrl = 'http://0.0.0.0:8050'

new Vue({
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app')
