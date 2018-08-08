// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import i18n from './config/i18n'

import VueAuthenticate from 'vue-authenticate'
import VueAxios from 'vue-axios'
import axios from 'axios'

Vue.config.productionTip = true

Vue.use(VueAxios, axios)
Vue.use(VueAuthenticate, {
  baseUrl: 'http://localhost:8000',
  tokenType: 'JWT',
  providers: {
    google: {
      clientId: '338829541691-14vtulpp1bav75s243cr6cfo0dvojkjl.apps.googleusercontent.com',
      redirectUri: 'http://localhost:8000/',
      url: 'http://localhost:8000/api/login/social/token_user/google/'
    },
    twitter: {
      clientId: 'nF5AOvrq4l8FmvjeRgEPpk6ID',
      redirectUri: 'http://localhost:8000/',
      url: 'http://localhost:8000/api/login/social/token_user/twitter/'
    },
    facebook: {
      clientId: '585737338256884',
      redirectUri: 'http://localhost:8000/',
      url: 'http://localhost:8000/api/login/social/token_user/facebook/'
    }
  }
})
/* eslint-disable no-new */
new Vue({
  i18n,
  el: '#app',
  router,
  template: '<App/>',
  components: {App},
  data () {
    return {
      authenticated: undefined,
      loading: false
    }
  }
})
