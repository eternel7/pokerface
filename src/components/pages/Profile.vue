<template>
  <div id="container" class="mdl-card mdl-shadow--16dp">
    <div class="mdl-card__supporting-text">
      <cardFabTitle userTitle="Page.Profile"></cardFabTitle>
      <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label"
           v-bind:class="{'is-dirty' : (user.email) ? true : false}">
        <input class="mdl-textfield__input" type="text" id="email" :readonly="(user.email) ? true : false" required
               v-model.trim="user.email"/>
        <label class="mdl-textfield__label" for="email">{{$t('user.Email')}}</label>
      </div>
      <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label"
           v-bind:class="{'is-dirty' : (user.first_name) ? true : false}">
        <input class="mdl-textfield__input" type="text" id="first_name"
               v-model.trim="user.first_name"/>
        <label class="mdl-textfield__label" for="first_name">{{$t('user.First_name')}}</label>
      </div>
      <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label"
           v-bind:class="{'is-dirty' : (user.last_name) ? true : false}">
        <input class="mdl-textfield__input" type="text" id="last_name"
               v-model.trim="user.last_name"/>
        <label class="mdl-textfield__label" for="last_name">{{$t('user.Last_name')}}</label>
      </div>
      <div class="link" v-on:click="askForAnImage"
           v-on:dragover.prevent="onDragOver" v-on:drop.prevent="onDrop">
        <img id="profilePreview" v-bind:src="user.avatar_image">
        <input hidden='hidden' type='file' id='fileInput' ref='fileInput' v-on:change.prevent="updatePreview"
               accept="image/*">
        <p class="center-align">{{$t('SignUp.ClickOrDropToUpdateYourProfilePicture')}}</p>
      </div>
      <button id="main-button" v-on:click.prevent="tryUpdate" v-bind:class="{ pulse: updateNeeded }"
              class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--colored mdl-color-text--white">
        {{$t('user.Update')}}
      </button>
      <errorMessages v-bind:errors="errors"></errorMessages>
      <hr/>
      <p class="center-align">{{$t('user.BeforeDeleteMessage')}}</p>
      <button id="secondary-button" v-on:click.prevent="tryDelete"
              class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent mdl-color-text--white">
        {{$t('user.Delete')}}
      </button>
    </div>
  </div>
</template>

<script>
  import ImageTools from '@/assets/image-tools.js'
  import FileDrop from '@/assets/file-drop.js'
  import PageBase from '@/components/pages/Page'
  import CardFabTitle from '@/components/sub-components/Card-fab-title'
  import ErrorMessages from '@/components/sub-components/ErrorMessages'
  import {authMixin} from '@/auth/authMixin.js'
  import axios from 'axios'

  let storedUser = JSON.parse(window.localStorage.getItem('auth-user'))
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
        user: {
          email: '',
          avatar_image: '/static/img/icons/apple-touch-icon-76x76.png',
          last_name: '',
          first_name: ''
        },
        message: '',
        errors: [],
        updateNeeded: 'noNeed'
      }
    },
    created: function (e) {
      if (storedUser) {
        this.user = storedUser
      }
      this.updateNeeded = 'noNeed'
      this.$nextTick(function () {
        this.updateNeeded = false
      })
      this.tryGetUserInfo(e)
    },
    watch: {
      // whenever user changes, this function will run
      user: {
        handler: function () {
          if (this.updateNeeded !== 'noNeed') {
            this.updateNeeded = true
          }
        },
        deep: true
      }
    },
    methods: {
      updatePreview (file) {
        const vm = this
        if (file !== undefined) {
          if (file.type === 'change') {
            file = vm.$refs.fileInput.files[0]
          }
          if (file.type.match('image.*')) {
            ImageTools.resizeImageBase64(file, 300, 300, function (result) {
              if (result) {
                vm.user.avatar_image = result
                vm.message = ''
              } else {
                console.log('updatePreview error', result)
              }
            })
          }
        }
        return true
      },
      askForAnImage (e) {
        const vm = this
        e.stopPropagation()
        return vm.$refs.fileInput.click()
      },
      onDrop (e) {
        const vm = this
        FileDrop.getFilesOnDrop(e, function (r) {
          if (r) {
            vm.updatePreview(r[0])
          }
        })
        return true
      },
      onDragOver (evt) {
        // Allow drop there
        return true
      },
      tryGetUserInfo (evt) {
        let vm = this
        vm.errors = []
        vm.$root.loading = true
        axios.get('/api/guser/', vm.authHeader())
          .then(function (response) {
            vm.$root.loading = false
            // handle success
            if (response.data.user) {
              vm.authStoreUser(response.data.user, vm)
              if (response.data.user) {
                vm.user = response.data.user
                vm.updateNeeded = false
              }
            } else {
              vm.errors = []
              vm.errors.push({message: response.data.message})
            }
          })
          .catch(function (error) {
            // handle error
            console.log(error)
            vm.$root.loading = false
            vm.updateNeeded = false
            vm.state = 0
            vm.errors = []
            vm.errors.push(error)
          })
          .then(function () {
            // always executed
            vm.$root.loading = false
            vm.updateNeeded = false
          })
      },
      tryUpdate (evt) {
        let vm = this
        vm.errors = []
        if (vm.$root.authenticated) {
          let user = vm.user
          vm.$root.loading = true
          axios.put('/api/uuser/', user, vm.authHeader())
            .then(function (response) {
              // handle success
              vm.$root.loading = false
              // update done
              vm.updateNeeded = false
              if (response.data.user) {
                // store updated user
                vm.authSuccess(response.data.user, vm, false)
              } else {
                vm.errors = []
                vm.errors.push({message: response.data.message})
              }
            })
            .catch(function (error) {
              // handle error
              console.log(error)
              vm.$root.loading = false
              // update done
              vm.updateNeeded = false
              vm.state = 0
              vm.errors = []
              vm.errors.push(error)
            })
            .then(function () {
              // always executed
              vm.$root.loading = false
              vm.updateNeeded = false
            })
        } else {
          vm.$router.push({name: 'Sign in'})
        }
      },
      tryDelete (evt) {
        let vm = this
        vm.errors = []
        if (vm.$root.authenticated) {
          if (confirm(vm.$i18n.t('user.ConfirmDeletionQuestion')) === true) {
            let user = vm.user
            vm.$root.loading = true
            axios.delete('/api/duser/' + user.username, vm.authHeader())
              .then(function (response) {
                // handle success
                vm.$root.loading = false
                if (response.data.email) {
                  vm.errors = []
                  alert(vm.$i18n.t('user.ConfirmedDeletion', {email: response.data.email}))
                  vm.$router.push({name: 'Sign up'})
                }
              })
              .catch(function (error) {
                // handle error
                console.log(error)
                vm.$root.loading = false
                vm.state = 0
                vm.errors = []
                vm.errors.push(error)
              })
              .then(function () {
                // always executed
                vm.$root.loading = false
              })
          }
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

  #profilePreview {
    max-width: 200px;
    max-height: 200px;
  }

  .pulse {
    background-color: rgb(96, 125, 139);
    animation: color_change 2s infinite;
  }

  @-webkit-keyframes color_change {
    0%, 100% {
      background-color: rgb(96, 125, 139);
    }
    50% {
      background-color: rgb(255, 64, 129);
    }
  }

  @-moz-keyframes color_change {
    0%, 100% {
      background-color: rgb(96, 125, 139);
    }
    50% {
      background-color: rgb(255, 64, 129);
    }
  }

  @-ms-keyframes color_change {
    0%, 100% {
      background-color: rgb(96, 125, 139);
    }
    50% {
      background-color: rgb(255, 64, 129);
    }
  }

  @-o-keyframes color_change {
    0%, 100% {
      background-color: rgb(96, 125, 139);
    }
    50% {
      background-color: rgb(255, 64, 129);
    }
  }

  @keyframes color_change {
    0%, 100% {
      background-color: rgb(96, 125, 139);
    }
    50% {
      background-color: rgb(255, 64, 129);
    }
  }
</style>
