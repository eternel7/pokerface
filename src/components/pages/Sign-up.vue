<template>
  <div id="form-container" class="mdl-card mdl-shadow--16dp">
    <div class="mdl-card__supporting-text">
      <cardFabTitle userTitle="Page.SignUp"></cardFabTitle>
      <userFields :email.sync="user.email" :password.sync="user.password"></userFields>
      <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
        <input class="mdl-textfield__input" type="password" id="passwordConfirm" required
               v-model.trim="register.confirmPassword"/>
        <label class="mdl-textfield__label" for="passwordConfirm">{{$t('SignUp.ConfirmPassword')}}</label>
        <pwdMeter v-bind:pwd="register.confirmPassword"></pwdMeter>
      </div>
      <div class="link" v-on:click="askForAnImage"
           v-on:dragover.prevent="onDragOver" v-on:drop.prevent="onDrop">
        <img id="profilePreview" v-bind:src="image" style="max-width:200px; max-height:200px">
        <input hidden='hidden' type='file' id='fileInput' ref='fileInput' v-on:change.prevent="updatePreview"
               accept="image/*">
        <p>{{$t('SignUp.ClickOrDropToUpdateYourProfilePicture')}}</p>
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
      <router-link id='third-button' class="mdl-button mdl-button--primary" to="/forgetpassword">
        {{$t('user.ForgotPassword')}}
      </router-link>
    </div>
  </div>
</template>

<script>
  import UserProfile from '@/assets/user-profile.js'
  import PageBase from '@/components/pages/Page'
  import UserFields from '@/components/user-components/Main-fields'
  import CardFabTitle from '@/components/sub-components/Card-fab-title'
  import ErrorMessages from '@/components/sub-components/ErrorMessages'
  import PwdMeter from '@/components/pwd-components/Pwd-helper'
  import {authMixin} from '@/auth/authMixin'

  function validateEmail (email) {
    // eslint-disable-next-line
    let re = /^(([^<>()\[\]\.,;:\s@\"]+(\.[^<>()\[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i
    return re.test(email)
  }

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
        message: '',
        'user': {
          'email': '',
          'password': ''
        },
        register: {},
        errors: []
      }
    },
    computed: {
      fullInfo: function () {
        return {
          email: this.user.email,
          password: this.user.password,
          confirmPassword: this.register.confirmPassword
        }
      }
    },
    methods: {
      tryRegister (evt) {
        let vm = this
        vm.errors = []
        evt.preventDefault()
        let userInfo = this.fullInfo
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
          let user = {
            'username': vm.user.email,
            'email': vm.user.email,
            'password': vm.user.password
          }
          vm.$auth.register(user).then(response => {
            vm.errors = []
            console.log('success', response)
            if (!response.data.token) {
              for (let field in response.data) {
                for (let erOnfield in response.data[field]) {
                  vm.errors.push({message: field + '.' + response.data[field][erOnfield].replace(/ /g, '_').replace(/\./g, '')})
                }
              }
            } else {
              vm.authSuccess({
                email: response.data.email,
                first_name: response.data.first_name || '',
                last_name: response.data.last_name || '',
                username: response.data.username
              }, vm, response)
            }
          }).catch(e => {
            console.log('catch error in register', e)
            vm.errors = []
            vm.errors.push(e)
          })
        }
      },
      updatePreview (file) {
        return UserProfile.updatePreview(file, this)
      },
      askForAnImage (e) {
        return UserProfile.askForAnImage(e, this)
      },
      onDrop (e) {
        return UserProfile.onDrop(e, this)
      },
      onDragOver (e) {
        return UserProfile.onDragOver(e, this)
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
