<template>
  <div class="mdl-layout__drawer">
    <span class="mdl-layout-title">Pokerface</span>
    <nav class="mdl-navigation">
      <router-link class="mdl-navigation__link" to="/" @click.native="hideMenu">{{ $t('Nav.Home') }}</router-link>
      <router-link v-if="!$root.authenticated" class="mdl-navigation__link" to="/signin" @click.native="hideMenu">{{
        $t('Nav.SignIn') }}
      </router-link>
      <router-link v-if="!$root.authenticated" class="mdl-navigation__link" to="/signup" @click.native="hideMenu">{{
        $t('Nav.SignUp') }}
      </router-link>
      <router-link v-if="$root.authenticated" class="mdl-navigation__link" to="/chatrooms" @click.native="hideMenu">{{
        $t('Nav.StartAChat') }}
      </router-link>
      <router-link v-if="$root.authenticated" class="mdl-navigation__link" to="/profile" @click.native="hideMenu">{{
        $t('Nav.YourProfile') }}
      </router-link>
      <router-link v-if="$root.authenticated" class="mdl-navigation__link" to="/" @click.native="tryToLogout">{{
        $t('Nav.Logout')
        }}
      </router-link>
      <localizerChooser></localizerChooser>
    </nav>
  </div>
</template>

<script>
  import LocalizerChooser from '@/components/localizer-chooser'
  import PageBase from '@/components/pages/Page'
  import {authMixin} from '@/auth/authMixin.js'

  require('material-design-lite')

  // common authentication test to ensure we are still authenticated
  let authentication = function (vm) {
    authMixin.methods.isAuthenticated(() => {
      // nice
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
    methods: {
      hideMenu: function () {
        document.getElementsByClassName('mdl-layout__drawer')[0].classList.remove('is-visible')
        document.getElementsByClassName('mdl-layout__obfuscator')[0].classList.remove('is-visible')
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
