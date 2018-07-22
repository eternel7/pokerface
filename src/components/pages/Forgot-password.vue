<template>
  <div id="form-container" class="mdl-card mdl-shadow--16dp">
    <div class="mdl-card__supporting-text">
      <cardFabTitle userTitle="Page.ForgotPassword"></cardFabTitle>
      <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
        <input class="mdl-textfield__input" type="email" id="email" required
               v-model.trim="user.email"/>
        <label class="mdl-textfield__label" for="email">{{$t('user.Email')}}</label>
      </div>
      <button id="main-button" v-on:click="sendForgotPassword"
              class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--colored mdl-color-text--white">
        {{$t('ForgotPassword.Send_password_reset_email')}}
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
    </div>
  </div>
</template>

<script>
  import PageBase from '@/components/pages/Page'
  import CardFabTitle from '@/components/sub-components/Card-fab-title'
  import ErrorMessages from '@/components/sub-components/ErrorMessages'
  import {validateEmail} from '@/auth/validateEmail'

  export default {
    name: 'Forgot-password',
    extends: PageBase,
    components: {
      cardFabTitle: CardFabTitle,
      errorMessages: ErrorMessages
    },
    data () {
      return {
        'user': {
          'email': ''
        },
        errors: []
      }
    },
    methods: {
      sendForgotPassword (evt) {
        let vm = this
        vm.errors = []
        evt.preventDefault()
        if (!vm.user.email || !validateEmail(vm.user.email)) {
          vm.errors.push({message: 'SignUp.EnterACorrectEmailAddress'})
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
