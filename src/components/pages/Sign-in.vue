<template>
  <div id="form-container" class="mdl-card mdl-shadow--16dp">
    <div class="mdl-card__supporting-text">
      <cardFabTitle userTitle="Page.SignIn"></cardFabTitle>
      <userFields :email.sync="user.email" :password.sync="user.password" userTitle="user.Login"
                  v-on:enterKeyUp="tryLogin"></userFields>
      <socialLogin></socialLogin>
      <button id="main-button" v-on:click="tryLogin"
              class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--colored mdl-color-text--white">
        {{$t('user.Login')}}
      </button>
      <errorMessages v-bind:errors="errors"></errorMessages>
    </div>
    <div class="mdl-card__actions">
      <router-link id='secondary-button' class="mdl-button mdl-button--primary" to="/signup">
        {{$t('user.SignUp')}}
      </router-link>
      <router-link id='third-button' class="mdl-button mdl-button--primary" to="/forgotpassword">
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
      tryLogin: function (e) {
        let vm = this
        vm.errors = []
        if (vm.user.password.length < 6) {
          vm.errors.push({message: 'password.Ensure_this_field_has_at_least_6_characters'})
        }
        if (vm.errors.length < 1) {
          vm.login(vm, vm.user, 'Home')
        }
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
    margin-top: 7vh;
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
