import axios from 'axios'

export const authMixin = {
  methods: {
    authenticate: function (provider) {
      let authProvider = provider
      if (provider === 'google') {
        authProvider = 'google-oauth2'
      }
      const that = this
      this.$auth.authenticate(provider, {provider: authProvider}).then(function (response) {
        that.authSuccess({
          email: response.data.email,
          first_name: response.data.first_name || '',
          last_name: response.data.last_name || '',
          username: response.data.username
        }, that, response)
      }).catch(function (error) {
        that.authError(error)
      })
    },
    authSuccess: function (user, vm, response) {
      if (response.data.token) {
        window.localStorage.setItem('vue-authenticate.vueauth_token', response.data.token)
      }
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
    },
    isAuthenticated: function (onSuccess, onError) {
      const token = localStorage.getItem('vue-authenticate.vueauth_token')
      axios.post('http://localhost:8000/api/check/',
        {'token': token}, {headers: {authorization: 'JWT ' + token}}).then((response) => {
          if (response.data.status) {
            onSuccess()
          } else {
            onError('server side no authentication')
          }
        }).catch((error) => {
          onError(error)
        })
    },
    checkToken: function (provider, redirect) {
      let that = this
      this.isAuthenticated(() => {
        redirect({path: true})
      }, (error) => {
        redirect({path: '/'})
        that.authError(error)
      })
    }
  }
}
