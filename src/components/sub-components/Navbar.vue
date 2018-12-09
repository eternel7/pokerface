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
    methods: {
      hideMenu: function () {
        let layout = document.querySelector('.mdl-layout')
        layout.MaterialLayout.toggleDrawer()
      },
      tryToLogout: function () {
        authMixin.methods.logout(this)
        this.hideMenu()
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
