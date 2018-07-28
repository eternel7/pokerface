<template>
  <div id="form-container" class="mdl-card mdl-shadow--16dp">
    <div class="mdl-card__supporting-text">
      <cardFabTitle userTitle="Page.ResetPassword"></cardFabTitle>
      <userFields :email.sync="user.email" :password.sync="user.password"></userFields>
      <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
        <input class="mdl-textfield__input" type="password" id="passwordConfirm" required
               v-model.trim="user.confirmPassword"/>
        <label class="mdl-textfield__label" for="passwordConfirm">{{$t('SignUp.ConfirmPassword')}}</label>
        <pwdMeter v-bind:pwd="user.confirmPassword"></pwdMeter>
      </div>
      <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
        <input class="mdl-textfield__input" type="text" id="resetpasswordtoken" required
               v-model.trim="user.resetPasswordToken"/>
        <label class="mdl-textfield__label" for="resetpasswordtoken">{{$t('user.ResetPasswordToken')}}</label>
      </div>
      <button id="main-button" v-on:click="updatePassword"
              class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--colored mdl-color-text--white">
        {{$t('ResetPassword.Update_Password')}}
      </button>
      <errorMessages v-bind:errors="errors"></errorMessages>
    </div>
    <div class="mdl-card__actions">
      <router-link id='third-button' class="mdl-button mdl-button--primary" to="/signin">
        {{$t('user.SignIn')}}
      </router-link>
      <router-link id='secondary-button' class="mdl-button mdl-button--primary" to="/signup">
        {{$t('user.SignUp')}}
      </router-link>
      <router-link id='fourth-button' class="mdl-button mdl-button--primary" to="/forgotpassword">
        {{$t('user.ForgotPassword')}}
      </router-link>
    </div>
  </div>
</template>

<script>
  import PageBase from '@/components/pages/Page'
  import UserFields from '@/components/user-components/Main-fields'
  import CardFabTitle from '@/components/sub-components/Card-fab-title'
  import ErrorMessages from '@/components/sub-components/ErrorMessages'
  import PwdMeter from '@/components/pwd-components/Pwd-helper'
  import {validateEmail} from '@/auth/validateEmail'
  import {authMixin} from '@/auth/authMixin'
  import axios from 'axios'

  export default {
    name: 'Reset-password',
    extends: PageBase,
    mixins: [authMixin],
    components: {
      userFields: UserFields,
      cardFabTitle: CardFabTitle,
      errorMessages: ErrorMessages,
      pwdMeter: PwdMeter
    },
    data () {
      return {
        'user': {
          'email': '',
          'password': '',
          'confirmPassword': '',
          'resetPasswordToken': (this.$route.params.resetPasswordToken) ? this.$route.params.resetPasswordToken : ''
        },
        state: 0,
        errors: []
      }
    },
    methods: {
      updatePassword (evt) {
        let vm = this
        vm.errors = []
        evt.preventDefault()
        let user = vm.user
        if (!user.email || !validateEmail(user.email)) {
          vm.errors.push({message: 'SignUp.EnterACorrectEmailAddress'})
        }
        if (user.password.length < 6) {
          vm.errors.push({message: 'password.Ensure_this_field_has_at_least_6_characters'})
        }
        if (user.password !== user.confirmPassword) {
          vm.errors.push({message: 'SignUp.ConfirmedPasswordIncorrect'})
        }
        if (user.resetPasswordToken.length < 30) {
          vm.errors.push({message: 'ResetPassword.TokenIncorrect'})
        }
        if (vm.errors.length < 1) {
          axios.post('/rpwd', vm.user)
            .then(function (response) {
              // handle success
              console.log(response)
              if (response.data.state === 1) {
                vm.state = 1
                // try to log in
                vm.login(vm, vm.user)
              } else {
                vm.errors = []
                vm.errors.push({message: response.data.message})
              }
            })
            .catch(function (error) {
              // handle error
              console.log(error)
              vm.state = 0
              vm.errors = []
              vm.errors.push(error)
            })
            .then(function () {
              // always executed
            })
        }
      }
    }
  }
</script>

<style scoped>

  .mdl-card {
    overflow: visible !important;
    z-index: auto !important;
  }

  .link {
    cursor: pointer
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

  #fourth-button {
    float: none;
  }
  .smaller {
    font-size: small;
  }
</style>
