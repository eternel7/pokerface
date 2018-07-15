/* eslint-disable */
import VueAxios from 'vue-axios'
import axios from 'axios'
import Vue from 'vue'

export const authMixin = {
  methods: {
    checkToken: function (provider, redirect) {
      axios.post('http://localhost:8000/api/check/', {'token': localStorage.getItem('vue-authenticate.vueauth_token')}).then((response) => {
        var path = (response.data.status) ? true : '/'
        redirect({ path: path})
      }).catch((error) => {
      })
    },
    authenticate: function (provider) {
      if (provider === 'google') {
        const that = this
        this.$auth.authenticate('google', {provider: "google-oauth2"}).then(function (response) {
            let user = {
              email: response.data.email,
              first_name: response.data.first_name,
              last_name: response.data.last_name,
              username : response.data.username
              }
            window.localStorage.setItem('auth-user', JSON.stringify(user))
            that.$router.push({ name: 'Chat', params: { id: response.data.email }})
        }).catch(function (error) {
          console.log(error)
        })
      }
    }
  }
}
