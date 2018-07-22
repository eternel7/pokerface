<template>
  <div id="form-container" class="mdl-card mdl-shadow--16dp">
    <div class="mdl-card__supporting-text">
      <cardFabTitle userTitle="Page.SignIn"></cardFabTitle>
      <userFields :email.sync="user.email" :password.sync="user.password" userTitle="user.Login"></userFields>
      <socialLogin></socialLogin>
      <button id="main-button" v-on:click="login"
              class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--colored mdl-color-text--white">
        {{$t('user.Login')}}
      </button>
      <errorMessages v-bind:errors="errors"></errorMessages>
    </div>
    <div class="mdl-card__actions">
      <router-link id='secondary-button' class="mdl-button mdl-button--primary" to="/signup">
        {{$t('user.Register')}}
      </router-link>
      <router-link id='third-button' class="mdl-button mdl-button--primary" to="/forgetpassword">
        {{$t('user.ForgotPassword')}}
      </router-link>
    </div>
  </div>
</template>

<script>
  import PageBase from '@/components/pages/Page'
  import UserFields from '@/components/user-components/Main-fields'
  import SocialLogin from '@/components/user-components/Social-login'
  import ErrorMessages from '@/components/sub-components/ErrorMessages'
  import CardFabTitle from '@/components/sub-components/Card-fab-title'
  import {authMixin} from '@/auth/authMixin'

  require('material-design-lite')

  export default {
    name: 'signInDetails',
    extends: PageBase,
    mixins: [authMixin],
    components: {
      userFields: UserFields,
      socialLogin: SocialLogin,
      cardFabTitle: CardFabTitle,
      errorMessages: ErrorMessages
    },
    data () {
      return {
        'user': {
          'email': '',
          'password': ''
        },
        errors: []
      }
    },
    methods: {
      login: function (e) {
        let vm = this
        vm.errors = []
        vm.$auth.login(vm.user).then(response => {
          vm.errors = []
          if (response.data.token) {
            vm.authSuccess({
              email: response.data.email,
              first_name: response.data.first_name || '',
              last_name: response.data.last_name || '',
              username: response.data.username
            }, vm, response.data.token)
          } else {
            vm.authError(response.data.message)
            if (response.data.message) {
              vm.errors = []
              vm.errors.push({message: response.data.message})
            }
          }
        }).catch(e => {
          vm.authError(e)
          vm.errors = []
          vm.errors.push(e)
        })
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .mdl-card {
    overflow: visible !important;
    z-index: auto !important;
  }

  #form-container {
    margin: auto;
  }

  #main-button {
    width: 100%;
    height: 40px;
    min-width: initial;
  }

  #secondary-button {
    float: left;
  }

  #third-button {
    float: right;
  }
</style>
