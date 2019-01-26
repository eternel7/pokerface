<template>
  <div class="mdl-layout__drawer" v-show="!backAvailable">
    <span class="mdl-layout-title">Pokerface</span>
    <nav class="mdl-navigation">
      <router-link class="mdl-navigation__link" to="/" @click.native="hideMenu">
        {{ $t('Nav.Home') }}
      </router-link>
      <router-link v-if="$root.authenticated" id="nav_profile" class="mdl-navigation__link" to="/profile"
                   @click.native="hideMenu">
        {{ $t('Nav.YourProfile') }}
      </router-link>
      <router-link v-if="$root.authenticated" id="nav_logout" class="mdl-navigation__link" to="/"
                   @click.native="tryToLogout">
        {{ $t('Nav.Logout') }}
      </router-link>
      <localizerChooser></localizerChooser>
      <div class="mdl-navigation__link link" @click="requestFullScreen">
        <i v-if="!fullscreen" class="material-icons">fullscreen</i>
        <i v-else class="material-icons">fullscreen_exit</i>
        <span>{{$t('Fullscreen')}}</span>
      </div>
    </nav>
  </div>
</template>

<script>
  import LocalizerChooser from '@/components/sub-components/localizer-chooser'
  import PageBase from '@/components/pages/Page'
  import {authMixin} from '@/auth/authMixin.js'

  require('material-design-lite')

  // common authentication test to ensure we are still authenticated
  let authentication = function (vm) {
    authMixin.methods.isAuthenticated(() => {
      // doing nothing is nice
    },
      () => {
        vm.$root.setUnauthenticated()
      })
  }

  export default {
    name: 'navbar',
    extends: PageBase,
    components: {
      localizerChooser: LocalizerChooser
    },
    props: ['backAvailable'],
    data: function () {
      return {
        fullscreen: false
      }
    },
    methods: {
      hideMenu: function () {
        let layout = document.querySelector('.mdl-layout')
        layout.MaterialLayout.toggleDrawer()
      },
      tryToLogout: function () {
        authMixin.methods.logout(this)
        this.hideMenu()
      },
      requestFullScreen: function () {
        let elem = document.getElementById('app-content')
        if (elem) {
          if (elem.requestFullscreen) {
            if (document.fullscreenElement) {
              document.exitFullscreen()
              this.fullscreen = false
            } else {
              elem.requestFullscreen()
              this.fullscreen = true
            }
          } else if (elem.msRequestFullscreen) {
            if (document.msFullscreenElement) {
              document.msExitFullscreen()
              this.fullscreen = false
            } else {
              elem.msRequestFullscreen()
              this.fullscreen = true
            }
          } else if (elem.mozRequestFullScreen) {
            if (document.mozFullScreenElement) {
              document.mozCancelFullScreen()
              this.fullscreen = false
            } else {
              elem.mozRequestFullScreen()
              this.fullscreen = true
            }
          } else if (elem.webkitRequestFullscreen) {
            if (document.webkitFullscreenElement) {
              document.webkitExitFullscreen()
              this.fullscreen = false
            } else {
              elem.webkitRequestFullscreen()
              this.fullscreen = true
            }
          }
        }
      }
    },
    watch: {
      '$route' (to, from) {
        // on route change re test authentication
        authentication(this)
      },
      backavailable () {
        console.log('hi there', this.backAvailable)
      }
    },
    created: function () {
      authentication(this)
    },
    beforeUpdate: function () {
      authentication(this)
    }
  }
</script>

<style>
  .mdl-layout__drawer-button > i {
    vertical-align: middle;
    position: absolute;
    top: 50%;
    left: 50%;
    -webkit-transform: translate(-12px, -12px);
    transform: translate(-12px, -12px);
    line-height: 24px;
    width: 24px
  }

  .mdl-navigation__link:hover, .mdl-layout-title {
    background-color: rgb(96, 125, 139) !important;
    color: rgb(255, 255, 255) !important;
  }

  .mdl-layout__drawer {
    border-right: 0 !important;
  }
</style>
