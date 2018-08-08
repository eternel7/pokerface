<template>
  <div id="form-container" class="mdl-card mdl-shadow--16dp">
    <div class="mdl-card__supporting-text">
      <cardFabTitle userTitle="Page.ForgotPassword"></cardFabTitle>
      <div v-if="state==0" class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
        We'll send you a link to reset your password.
      </div>
      <div v-if="state==1" class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
        We have send an email to {{user.email}} with instruction on how to reset your password.
        <br/><br/>
        <span class="smaller">Didn't receive the password reset email? Check your spam folder for an email with subject <strong>"Reset
        password on
        PokerFace"</strong>. If you still don't see the email <a class="link" @click="startAgain">try again</a>.</span>
      </div>
      <div v-if="state==0" class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
        <input class="mdl-textfield__input" type="email" id="email" required
               v-model.trim="user.email"/>
        <label class="mdl-textfield__label" for="email">{{$t('user.Email')}}</label>
      </div>
      <button id="main-button" v-on:click="stepForgotPassword"
              class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--colored mdl-color-text--white">
        <span v-if="state==0">{{$t('ForgotPassword.Send_password_reset_email')}}</span>
        <span v-if="state==1">{{$t('ForgotPassword.Go_to_reset_password')}}</span>
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
  import axios from 'axios'

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
        state: 0,
        errors: []
      }
    },
    methods: {
      startAgain (evt) {
        this.state = 0
        // force refresh of material design lite inputs
        window.setTimeout(function () {
          PageBase.mounted()
        }, 500)
      },
      stepForgotPassword (evt) {
        let vm = this
        if (vm.state === 0) {
          vm.sendForgotPassword(evt)
        } else {
          vm.$router.push({name: 'ResetPassword'})
        }
      },
      sendForgotPassword (evt) {
        let vm = this
        vm.errors = []
        evt.preventDefault()
        if (!vm.user.email || !validateEmail(vm.user.email)) {
          vm.errors.push({message: 'SignUp.EnterACorrectEmailAddress'})
        }
        if (vm.errors.length < 1) {
          vm.$root.loading = true
          axios.post('/fpwd', {email: vm.user.email})
            .then(function (response) {
              vm.$root.loading = false
              // handle success
              console.log(response)
              vm.state = 1
            })
            .catch(function (error) {
              // handle error
              vm.$root.loading = false
              console.log(error)
              vm.state = 0
              vm.errors = []
              vm.errors.push(error)
            })
            .then(function () {
              // always executed
              vm.$root.loading = false
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

  .smaller {
    font-size: small;
  }
</style>
