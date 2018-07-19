import axios from 'axios'

export const authMixin = {
  methods: {
    checkToken: function (provider, redirect) {
      const that = this
      const token = localStorage.getItem('vue-authenticate.vueauth_token')
      axios.post('http://localhost:8000/api/check/',
        {'token': token}, {headers: {authorization: 'JWT ' + token}}).then((response) => {
          let path = (response.data.status) ? true : '/'
          if (path !== true) {
            that.authError('server side no authentication')
          }
          redirect({path: path})
        }).catch((error) => {
          that.authError(error)
        })
    },
    authenticate: function (provider) {
      let authProvider = provider
      if (provider === 'google') {
        authProvider = 'google-oauth2'
      }
      const that = this
      this.$auth.authenticate(provider, {provider: authProvider}).then(function (response) {
        console.log(response)
        that.authSuccess({
          email: response.data.email,
          first_name: response.data.first_name,
          last_name: response.data.last_name,
          username: response.data.username
        }, that)
      }).catch(function (error) {
        that.authError(error)
      })
    },
    authSuccess: function (user, vm) {
      window.localStorage.setItem('auth-user', JSON.stringify(user))
      vm.$router.push({name: 'Profile', params: {id: user.email}})
    },
    authError: function (error) {
      console.log(error)
      this.logout()
    },
    logout: function () {
      localStorage.removeItem('vue-authenticate.vueauth_token')
      localStorage.removeItem('auth-user')
    }
  }
}
