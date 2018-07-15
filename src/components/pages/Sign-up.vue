<template>
  <div id="login-container" class="mdl-card mdl-shadow--16dp">
    <div class="mdl-card__supporting-text">
      <cardFabTitle userTitle="Page.SignUp"></cardFabTitle>
      <userFields :email.sync="user.email" :password.sync="user.password"></userFields>
      <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
        <input class="mdl-textfield__input" type="password" id="passwordConfirm" required
               v-model.trim="register.confirmPassword"/>
        <label class="mdl-textfield__label" for="passwordConfirm">Confirm password</label>
      </div>
      <div class="link" v-on:click="askForAnImage"
           v-on:dragover.prevent="onDragOver" v-on:drop.prevent="onDrop">
        <img id="profilePreview" v-bind:src="image" style="max-width:200px; max-height:200px">
        <input hidden='hidden' type='file' id='fileInput' ref='fileInput' v-on:change.prevent="updatePreview"
               accept="image/*">
        <p class="center-align">{{$t('SignUp.ClickOrDropToUpdateYourProfilePicture')}}</p>
      </div>
      <div class="mdl-card__supporting-text">
        <button id="register-button"
                class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--colored mdl-color-text--white"
                v-on:click="tryRegister">
          {{$t('SignUp.Register')}}
        </button>
        <errorMessages v-bind:errors="errors"></errorMessages>
      </div>
      <div class="mdl-card__supporting-text">
        <p>{{$t('SignUp.SignInIfYouHaveAnAccount')}}</p>
        <router-link id='login' class="mdl-button mdl-js-button mdl-button--primary" to="/">
          {{$t('Nav.SignIn')}}
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
  import UserProfile from '@/assets/user-profile.js'
  import PageBase from '@/components/pages/Page'
  import UserFields from '@/components/user-components/Main-fields'
  import CardFabTitle from '@/components/sub-components/Card-fab-title'
  import ErrorMessages from '@/components/sub-components/ErrorMessages'

  function validateEmail (email) {
    // eslint-disable-next-line
    let re = /^(([^<>()\[\]\.,;:\s@\"]+(\.[^<>()\[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i
    console.log('validateEmail', email)
    return re.test(email)
  }

  export default {
    name: 'signUp',
    extends: PageBase,
    components: {
      userFields: UserFields,
      cardFabTitle: CardFabTitle,
      errorMessages: ErrorMessages
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
          vm.errors.push({message: 'Enter a correct email address'})
        }
        if (userInfo.password !== userInfo.confirmPassword) {
          vm.errors.push({message: 'Confirmed password incorrect'})
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

  #login-container {
    margin: auto;
  }

  #register-button {
    width: 100%;
    height: 40px;
    min-width: initial;
  }

  #login {
    width: 50%;
    height: 40px;
  }
</style>
