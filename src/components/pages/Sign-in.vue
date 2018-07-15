<template>
  <div id="login-container" class="mdl-card mdl-shadow--16dp">
    <div class="mdl-card__supporting-text">
      <cardFabTitle userTitle="Page.SignIn"></cardFabTitle>
      <userFields :email.sync="user.email" :password.sync="user.password" userTitle="user.Login"></userFields>
      <socialLogin></socialLogin>
      <button id="login-button" v-on:click="login"
              class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--colored mdl-color-text--white">
        {{$t('user.Login')}}
      </button>
      <errorMessages v-bind:errors="errors"></errorMessages>
    </div>
    <div class="mdl-card__actions">
      <router-link id='register' class="mdl-button" to="/signup">
        {{$t('user.Register')}}
      </router-link>
      <router-link id='forgot-password' class="mdl-button" to="/forgetpassword">
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
  import axios from 'axios'

  require('material-design-lite')

  export default {
    name: 'signInDetails',
    extends: PageBase,
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
        axios.post(`http://localhost:8000/api/login/`, this.user)
          .then(response => {
            vm.errors = []
            console.log(response)
            localStorage.setItem('jwtToken', response.data.token)
          })
          .catch(e => {
            console.log(e)
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

  #login-container {
    margin: auto;
  }

  #login-button {
    width: 100%;
    height: 40px;
    min-width: initial;
  }

  #forgot-password {
    float: right;
  }

  #register {
    float: left;
  }
</style>
