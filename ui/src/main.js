import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
import {globalFunctions} from './globalFunctions'

Vue.config.productionTip = false
Vue.prototype.globalFunctions = globalFunctions;
if(window.location.href.includes('localhost')){
  Vue.prototype.apiUrl = 'http://0.0.0.0:8050'
}else{
  Vue.prototype.apiUrl = 'https://api-mkeller3.cloud.okteto.net'
}


new Vue({
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app')
