<template>
  <div id="container" class="mdl-card mdl-shadow--16dp">
    <dialog ref="dialog" class="mdl-dialog">
      <div class="mdl-dialog__content">
        <p>
          {{$t('user.ConfirmDeletionQuestion')}}
        </p>
      </div>
      <div class="mdl-dialog__actions">
        <button type="button" id="CancelDialog" class="mdl-button close" v-on:click="closeConfirmDialog(true)">
          Disagree
        </button>
        <button type="button" id="OkDialog"
                class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent mdl-color-text--white"
                v-on:click="tryDeleteConfirmed">Agree
        </button>
      </div>
    </dialog>
    <div class="mdl-card__supporting-text">
      <cardFabTitle userTitle=""></cardFabTitle>
      <!-- Tabs -->
      <div class="mdl-tabs mdl-js-tabs mdl-js-ripple-effect is-upgraded">
        <div class="mdl-tabs__tab-bar">
          <div v-for="tab in tabs" class="mdl-tabs__tab link"
               v-bind:href="tab.id" v-bind:id="'profile_tab_'+tab.id" v-on:click="tabActive=tab.id"
               v-bind:class="{'is-active' : (tab.id===tabActive)}">
            <i class="material-icons">
              {{tab.icon}}
            </i><span>{{$t('user.' + tab.Title)}}</span>
          </div>
        </div>
        <div class="mdl-tabs__panel is-active" id="0" v-if="tabActive==='0'">
          <profileDetails v-bind:user="user"
                          v-bind:errors="errors"
                          v-bind:updateNeeded="updateNeeded"
                          v-on:tryUpdate="tryUpdate"></profileDetails>
        </div>
      </div>
      <div class="mdl-tabs__panel is-active" id="1" v-if="tabActive==='1'">
        <div class="page-content">More<!-- Your content goes here --></div>
      </div>
      <div class="mdl-tabs__panel is-active" id="2" v-if="tabActive==='2'">
        <profilePwdUpdate></profilePwdUpdate>
      </div>
      <div class="mdl-tabs__panel is-active" id="3" v-if="tabActive==='3'">
        <div class="page-content">
          <p class="center-align">{{$t('user.BeforeDeleteMessage')}}</p>
          <button id="secondary-button" v-on:click.prevent="tryDelete"
                  class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent mdl-color-text--white">
            {{$t('user.Delete')}}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import PageBase from '@/components/pages/Page'
  import CardFabTitle from '@/components/sub-components/Card-fab-title'
  import ProfileDetails from '@/components/user-components/Profile-details'
  import ProfilePwdUpdate from '@/components/user-components/Profile-password-update'
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
      profileDetails: ProfileDetails,
      profilePwdUpdate: ProfilePwdUpdate,
      errorMessages: ErrorMessages
    },
    data () {
      return {
        tabs: [
          {
            id: '0',
            Title: 'TabUser',
            icon: 'person'
          },
          {
            id: '1',
            Title: 'TabMore',
            icon: 'loyalty'
          },
          {
            id: '2',
            Title: 'TabPassword',
            icon: 'verified_user'
          },
          {
            id: '3',
            Title: 'TabDelete',
            icon: 'delete'
          }
        ],
        tabActive: '0',
        message: '',
        errors: [],
        updateNeeded: 'noNeed',
        loaded: false
      }
    },
    computed: {
      user: function () {
        return this.$root.user
      }
    },
    created: function (e) {
      if (storedUser) {
        this.updateNeeded = 'noNeed'
        this.$root.user = storedUser
        this.updateNeeded = false
      }
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
                vm.$root.user = response.data.user
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
                vm.$root.showSnackbar(vm.$i18n.t('user.UpdateConfirmed'))
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
          let dialog = vm.$refs['dialog']
          // eslint-disable-next-line no-undef
          dialogPolyfill.registerDialog(dialog)
          dialog.showModal()
        } else {
          vm.$router.push({name: 'Sign in'})
        }
      },
      closeConfirmDialog (evt) {
        let vm = this
        let dialog = vm.$refs['dialog']
        if (dialog) {
          // eslint-disable-next-line no-undef
          dialogPolyfill.registerDialog(dialog)
          dialog.close()
        }
      },
      tryDeleteConfirmed (evt) {
        let vm = this
        let user = vm.user
        vm.$root.loading = true
        axios.delete('/api/duser/' + user.username, vm.authHeader())
          .then(function (response) {
            // handle success
            vm.$root.loading = false
            if (response.data.email) {
              vm.errors = []
              let confirmation = {
                'message': vm.$i18n.t('user.ConfirmedDeletion', {email: response.data.email}),
                'timeout': 10000
              }
              vm.$root.showSnackbar(confirmation)
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
            vm.closeConfirmDialog(error)
          })
          .then(function () {
            // always executed
            vm.$root.loading = false
            vm.closeConfirmDialog(true)
          })
      }
    }
  }
</script>

<style scoped>

  .mdl-card {
    overflow: visible !important;
    z-index: auto !important;
    width: 75%;
    min-width: 300px;
  }

  .mdl-card__supporting-text {
    margin: auto;
  }

  #container {
    margin: auto;
    margin-top: 7vh;
  }

  .mdl-tabs__tab {
    font-size: calc(7px + .5vw);
    padding: 0 4%;
  }

  .mdl-tabs__tab > i {
    display: none;
  }

  .mdl-tabs__tab {
    display: block;
    position: relative;
    text-decoration: none;
    -webkit-transition: color .2s ease-in-out;
    transition: color .2s ease-in-out;
  }

  .mdl-tabs__tab:before {
    content: "";
    position: absolute;
    bottom: 0;
    width: 0;
    border-bottom: solid 2px;
  }

  .mdl-tabs__tab:before {
    left: 0;
  }

  .mdl-tabs__tab:hover {
    color: rgb(255, 64, 129);
  }

  .mdl-tabs__tab:hover:before {
    width: 100%;
  }

  .mdl-tabs__tab:before {
    -webkit-transition: width .2s ease-in-out;
    transition: width .2s ease-in-out;
  }

  @media all and (min-width: 0) and (max-width: 480px) {
    .mdl-card {
      width: 100%;
    }

    .mdl-tabs__tab-bar {
      width: 100%;
    }

    .mdl-tabs__tab {
      width: 100%;
      margin: 0 auto;
    }

    .mdl-tabs__tab > i {
      display: block;
      margin-top: 10px;
    }

    .mdl-tabs__tab > span {
      display: none;
    }
  }

  .page-content {
    margin: 20px auto 20px;
  }
</style>
