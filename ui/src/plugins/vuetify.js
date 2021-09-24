import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';

Vue.use(Vuetify);

export default new Vuetify({
    theme: {
      themes: {
        light: {
          primary: "#264653",
          secondary: "#E9C46A",
          accent: "#F4A261"
        },
      },
    },
  })