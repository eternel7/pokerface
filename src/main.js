// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import CookiesAccept from './components/gdpr/Cookies-accept'
import router from './router'
import i18n from './config/i18n'

import VueAuthenticate from 'vue-authenticate'
import VueAxios from 'vue-axios'
import axios from 'axios'

// https redirect on non local env
if (location.protocol !== 'https:' && window.location.href.search('localhost') === -1) {
  location.href = 'https:' + window.location.href.substring(window.location.protocol.length)
}

const appBaseUrl = window.location.protocol + '//' + window.location.hostname + ((window.location.port !== '') ? ':' + window.location.port : '') + '/'

Vue.config.productionTip = true

Vue.use(VueAxios, axios)
Vue.use(VueAuthenticate, {
  baseUrl: appBaseUrl,
  tokenType: 'JWT',
  providers: {
    google: {
      clientId: '338829541691-14vtulpp1bav75s243cr6cfo0dvojkjl.apps.googleusercontent.com',
      redirectUri: appBaseUrl,
      url: appBaseUrl + 'api/login/social/token_user/google/'
    },
    twitter: {
      clientId: 'nF5AOvrq4l8FmvjeRgEPpk6ID',
      redirectUri: appBaseUrl,
      url: appBaseUrl + 'api/login/social/token_user/twitter/'
    },
    facebook: {
      clientId: '585737338256884',
      redirectUri: appBaseUrl,
      url: appBaseUrl + 'api/login/social/token_user/facebook/'
    }
  }
})
const userDefault = {
  email: false,
  avatar_image: '/static/img/icons/apple-touch-icon-76x76.png',
  last_name: false,
  first_name: false,
  username: false,
  social_info: false
}
/* eslint-disable no-new */
new Vue({
  i18n,
  el: '#app',
  router,
  template: '<App ref="App" v-bind:message="message" ' +
    'v-bind:searchAvailable="searchAvailable"' +
    'v-bind:backAvailable="backAvailable"' +
    'v-bind:errors="errors"/>',
  components: {App},
  data () {
    return {
      loading: false,
      user: userDefault,
      message: '',
      timeout: 2750,
      actionHandler: false,
      actionText: false,
      errors: [],
      searchAvailable: false,
      backAvailable: false
    }
  },
  computed: {
    authenticated: function () {
      return (this.user.username && this.user.username !== '')
    }
  },
  methods: {
    setUnauthenticated: function () {
      this.user = userDefault
    },
    setSearch: function (val) {
      this.searchAvailable = !!val
    },
    setBack: function (val) {
      this.backAvailable = !!val
    },
    showSnackbar: function (msg) {
      if (typeof msg === 'string') {
        this.message = msg
      } else {
        this.message = msg.message
        this.timeout = msg.timeout
        this.actionHandler = msg.actionHandler
        this.actionText = msg.actionText
      }
      this.$nextTick(function () {
        this.$refs.App.showSnackbar()
        this.message = ''
        this.timeout = 2750
        this.actionHandler = false
        this.actionText = false
      })
    }
  }
})
/* eslint-disable no-new */
new Vue({
  el: '#cookies-accept',
  template: '<Cookies-accept ref="Cookies-accept"/>',
  components: {CookiesAccept},
  data () {
    return {}
  }
})
