import axios from 'axios'

export const authMixin = {
  methods: {
    authHeader: function (token) {
      const tok = token || localStorage.getItem('vue-authenticate.vueauth_token')
      return {
        headers: {
          authorization: 'JWT ' + tok
        }
      }
    },
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
          username: response.data.username,
          avatar_image: response.data.avatar_image
        }, that, false) // Authenticate manage the local update of token
      }).catch(function (error) {
        that.authError(error, that)
      })
    },
    authSuccess: function (user, vm, token) {
      if (token) {
        window.localStorage.setItem('vue-authenticate.vueauth_token', token)
      }
      window.localStorage.setItem('auth-user', JSON.stringify(user))
      vm.$root.authenticated = true
      vm.$router.push({name: 'Profile'})
    },
    authError: function (error, vm) {
      console.log(error)
      this.logout(vm)
    },
    logout: function (vm) {
      if (vm && vm.$root) {
        vm.$root.authenticated = false
      }
      axios.post('/api/ulogout/', {}, this.authHeader()).then((response) => {
        console.log('user log out', response.data.message)
      }).catch((error) => {
        console.log('Error in user log out', error)
      })
      localStorage.removeItem('vue-authenticate.vueauth_token')
      localStorage.removeItem('auth-user')
    },
    isAuthenticated: function (onSuccess, onError) {
      const that = this
      const token = localStorage.getItem('vue-authenticate.vueauth_token')
      axios.post('/api/check/',
        {'token': token}, this.authHeader(token)).then((response) => {
          if (response.data.status) {
            onSuccess()
          } else {
            onError('server side no authentication')
            that.authError('server side no authentication')
          }
        }).catch((error) => {
          onError(error)
          that.authError(error, that)
        })
    },
    checkToken: function (provider, redirect) {
      let that = this
      this.isAuthenticated(() => {
        redirect({path: true})
      }, (error) => {
        redirect({path: '/'})
        that.authError(error, that)
      })
    },
    login: function (vm, user) {
      vm.$auth.login(user).then(response => {
        vm.errors = []
        if (response.data.token) {
          vm.authSuccess({
            email: response.data.email,
            first_name: response.data.first_name || '',
            last_name: response.data.last_name || '',
            username: response.data.username,
            avatar_image: response.data.avatar_image
          }, vm, response.data.token)
        } else {
          vm.authError(response.data.message, vm)
          if (response.data.message) {
            vm.errors = []
            vm.errors.push({message: response.data.message})
          }
        }
      }).catch(e => {
        vm.authError(e, vm)
        vm.errors = []
        vm.errors.push(e)
      })
    }
  }
}
