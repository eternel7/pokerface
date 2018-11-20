<template>
  <div class="page-content">
    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label"
         v-bind:class="{'is-dirty' : (password) ? true : false}">
      <input class="mdl-textfield__input" type="password" id="password" ref="password" required autofocus
             v-model.trim="password"/>
      <label class="mdl-textfield__label" for="password">{{$t('user.Password')}}</label>
      <pwdMeter v-bind:pwd="password"></pwdMeter>
    </div>
    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label"
         v-bind:class="{'is-dirty' : (newPassword) ? true : false}">
      <input class="mdl-textfield__input" type="password" id="newPassword" required
             v-model.trim="newPassword"/>
      <label class="mdl-textfield__label" for="password">{{$t('user.NewPassword')}}</label>
      <pwdMeter v-bind:pwd="newPassword"></pwdMeter>
    </div>
    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label"
         v-bind:class="{'is-dirty' : (confirmPassword) ? true : false}">
      <input class="mdl-textfield__input" type="password" id="passwordConfirm" required
             v-model.trim="confirmPassword"/>
      <label class="mdl-textfield__label" for="passwordConfirm">{{$t('user.ConfirmNewPassword')}}</label>
      <pwdMeter v-bind:pwd="confirmPassword"></pwdMeter>
    </div>
    <button id="main-button" v-on:click.prevent="tryUpdatePassword"
            class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--colored mdl-color-text--white">
      {{$t('user.UpdatePassword')}}
    </button>
    <errorMessages v-bind:errors="errors"></errorMessages>
  </div>
</template>

<script>
  import PwdMeter from '@/components/pwd-components/Pwd-helper'
  import ErrorMessages from '@/components/sub-components/ErrorMessages'
  import {authMixin} from '@/auth/authMixin.js'
  import axios from 'axios'

  export default {
    name: 'profileDetails',
    mixins: [authMixin],
    data () {
      return {
        password: '',
        newPassword: '',
        confirmPassword: '',
        errors: []
      }
    },
    components: {
      pwdMeter: PwdMeter,
      errorMessages: ErrorMessages
    },
    methods: {
      tryUpdatePassword (evt) {
        const vm = this
        vm.errors = []
        evt.preventDefault()
        if (vm.password.length < 6) {
          vm.errors.push({message: 'newPassword.PleaseInputYourFormerPassword'})
        }
        if (vm.newPassword.length < 6) {
          vm.errors.push({message: 'newPassword.Ensure_this_field_has_at_least_6_characters'})
        }
        if (vm.newPassword === vm.password) {
          vm.errors.push({message: 'newPassword.NewPasswordSimilarToFormerOne'})
        }
        if (vm.newPassword !== vm.confirmPassword) {
          vm.errors.push({message: 'SignUp.ConfirmedPasswordIncorrect'})
        }
        if (vm.errors.length < 1) {
          let user = {
            'email': vm.$root.user.email,
            'password': vm.password,
            'newPassword': vm.newPassword,
            'confirmPassword': vm.confirmPassword,
            'language': vm.$i18n.locale
          }
          vm.$root.loading = true
          axios.post('/upwd', user, vm.authHeader())
            .then(function (response) {
              // handle success
              vm.$root.loading = false
              vm.errors = []
              if (response.data.state && response.data.state === 1) {
                vm.password = ''
                vm.newPassword = ''
                vm.confirmPassword = ''
                vm.$root.showSnackbar(vm.$i18n.t(response.data.message))
              } else {
                vm.errors.push({message: response.data.message})
              }
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
    },
    mounted () {
      this.$refs.password.focus()
    }
  }
</script>
<style scoped>
  .mdl-textfield {
    display: block;
    margin: auto;
  }

  .page-content {
    margin: 20px auto 20px;
  }
</style>
