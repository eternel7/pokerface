<template>
  <div id="form-container" class="mdl-card mdl-shadow--16dp">
    <div class="mdl-card__supporting-text">
      <cardFabTitle userTitle="Page.SignUp"></cardFabTitle>
      <userFields :email.sync="user.email" :password.sync="user.password"></userFields>
      <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label"
           v-bind:class="{'is-dirty' : (user.confirmPassword) ? true : false}">
        <input class="mdl-textfield__input" type="password" id="passwordConfirm" required
               v-model.trim="user.confirmPassword"/>
        <label class="mdl-textfield__label" for="passwordConfirm">{{$t('SignUp.ConfirmPassword')}}</label>
        <pwdMeter v-bind:pwd="user.confirmPassword"></pwdMeter>
      </div>
      <button id="main-button"
              class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--colored mdl-color-text--white"
              v-on:click="tryRegister">
        {{$t('SignUp.Register')}}
      </button>
      <errorMessages v-bind:errors="errors"></errorMessages>
    </div>
    <div class="mdl-card__actions">
      <router-link id='secondary-button' class="mdl-button mdl-button--primary" to="/signin">
        {{$t('Nav.SignIn')}}
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
  import CardFabTitle from '@/components/sub-components/Card-fab-title'
  import ErrorMessages from '@/components/sub-components/ErrorMessages'
  import PwdMeter from '@/components/pwd-components/Pwd-helper'
  import {authMixin} from '@/auth/authMixin'
  import {validateEmail} from '@/auth/validateEmail'

  export default {
    name: 'signUp',
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
        image: '/static/img/icons/apple-touch-icon-76x76.png',
        'user': {
          'email': '',
          'password': '',
          'confirmPassword': ''
        },
        errors: []
      }
    },
    methods: {
      tryRegister (evt) {
        let vm = this
        vm.errors = []
        evt.preventDefault()
        let userInfo = this.user
        if (!userInfo.email || !validateEmail(userInfo.email)) {
          vm.errors.push({message: 'SignUp.EnterACorrectEmailAddress'})
        }
        if (userInfo.password.length < 6) {
          vm.errors.push({message: 'password.Ensure_this_field_has_at_least_6_characters'})
        }
        if (userInfo.password !== userInfo.confirmPassword) {
          vm.errors.push({message: 'SignUp.ConfirmedPasswordIncorrect'})
        }
        if (vm.errors.length < 1) {
          vm.register(vm, {
            'username': vm.user.email,
            'email': vm.user.email,
            'password': vm.user.password
          }, 'Chatrooms')
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

</style>
