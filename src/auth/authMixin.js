import axios from 'axios'

export const authMixin = {
  methods: {
    checkToken: function (provider, redirect) {
      const token = localStorage.getItem('vue-authenticate.vueauth_token')
      axios.post('http://localhost:8000/api/check/',
        {'token': token}, {headers: {authorization: 'JWT ' + token}}).then((response) => {
          console.log(response.data.status, redirect)
          let path = (response.data.status) ? true : '/'
          redirect({path: path})
        }).catch((error) => {
          console.log(error)
          localStorage.removeItem('vue-authenticate.vueauth_token')
          localStorage.removeItem('auth-user')
        })
    },
    authenticate: function (provider) {
      if (provider === 'google') {
        const that = this
        this.$auth.authenticate('google', {provider: 'google-oauth2'}).then(function (response) {
          that.authSuccess({
            email: response.data.email,
            first_name: response.data.first_name,
            last_name: response.data.last_name,
            username: response.data.username
          }, that)
        }).catch(function (error) {
          console.log(error)
        })
      }
    },
    authSuccess: function (user, vm) {
      window.localStorage.setItem('auth-user', JSON.stringify(user))
      vm.$router.push({name: 'Profile', params: {id: user.email}})
    }
  }
}
