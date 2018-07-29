<template>
  <div id="container" class="mdl-card mdl-shadow--16dp">
    <div class="mdl-card__supporting-text">
      <cardFabTitle userTitle="Page.Profile"></cardFabTitle>
      <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
        <input class="mdl-textfield__input" type="text" id="email" readonly required
               v-model.trim="user.email"/>
        <label class="mdl-textfield__label" for="email">Email</label>
      </div>
      <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
        <input class="mdl-textfield__input" type="text" id="first_name"
               v-model.trim="user.first_name"/>
        <label class="mdl-textfield__label" for="first_name">First name</label>
      </div>
      <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
        <input class="mdl-textfield__input" type="text" id="last_name"
               v-model.trim="user.last_name"/>
        <label class="mdl-textfield__label" for="last_name">Last name</label>
      </div>
      <div class="link" v-on:click="askForAnImage"
           v-on:dragover.prevent="onDragOver" v-on:drop.prevent="onDrop">
        <img id="profilePreview" v-bind:src="image" style="max-width:200px; max-height:200px">
        <input hidden='hidden' type='file' id='fileInput' ref='fileInput' v-on:change.prevent="updatePreview"
               accept="image/*">
        <p class="center-align">{{$t('SignUp.ClickOrDropToUpdateYourProfilePicture')}}</p>
      </div>
      <button id="main-button" v-on:click.prevent="tryUpdate"
              class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--colored mdl-color-text--white">
        {{$t('ResetPassword.Update_Password')}}
      </button>
      <errorMessages v-bind:errors="errors"></errorMessages>
    </div>
  </div>
</template>

<script>
  import UserProfile from '@/assets/user-profile.js'
  import PageBase from '@/components/pages/Page'
  import CardFabTitle from '@/components/sub-components/Card-fab-title'
  import ErrorMessages from '@/components/sub-components/ErrorMessages'
  import {authMixin} from '@/auth/authMixin.js'
  import axios from 'axios'

  export default {
    name: 'Profile',
    extends: PageBase,
    mixins: [authMixin],
    components: {
      cardFabTitle: CardFabTitle,
      errorMessages: ErrorMessages
    },
    data () {
      return {
        image: '/static/img/icons/apple-touch-icon-76x76.png',
        message: '',
        errors: []
      }
    },
    computed: {
      user: function () {
        return JSON.parse(window.localStorage.getItem('auth-user'))
      }
    },
    methods: {
      updatePreview (file) {
        return UserProfile.updatePreview(file, this)
      },
      askForAnImage (evt) {
        return UserProfile.askForAnImage(evt, this)
      },
      onDrop (evt) {
        return UserProfile.onDrop(evt, this)
      },
      onDragOver (evt) {
        return UserProfile.onDragOver(evt, this)
      },
      tryUpdate (evt) {
        let vm = this
        vm.errors = []
        if (vm.errors.length < 1 && vm.$root.authenticated) {
          const token = localStorage.getItem('vue-authenticate.vueauth_token')
          axios.put('/uuser', vm.user, {headers: {authorization: 'JWT ' + token}})
            .then(function (response) {
              // handle success
              console.log(response)
              if (response.data.user) {
                vm.authSuccess(response.data.user, vm, false)
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
        } else {
          vm.$router.push({name: 'Sign in'})
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

  #container {
    margin: auto;
  }
</style>
