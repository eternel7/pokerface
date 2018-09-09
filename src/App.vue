<template>
  <div id="app-content" class="mdl-layout mdl-js-layout mdl-layout--fixed-header">
    <header class="mdl-layout__header">
      <loading></loading>
      <div class="mdl-layout__header-row">
        <span class="mdl-layout-title">Pokerface</span>
        <div class="mdl-layout-spacer"></div>
        <transition name="fade">
        <div v-show="searchAvailable" class="mdl-textfield mdl-js-textfield mdl-textfield--expandable
                  mdl-textfield--floating-label mdl-textfield--align-right">
          <label class="mdl-button mdl-js-button mdl-button--icon"
                 for="fixed-header-drawer-exp">
            <i class="material-icons">search</i>
          </label>
          <div class="mdl-textfield__expandable-holder">
            <input class="mdl-textfield__input" type="text" name="search"
                   id="fixed-header-drawer-exp">
          </div>
        </div>
        </transition>
      </div>
    </header>
    <navbar></navbar>
    <main class="mdl-layout__content">
      <section class="section">
        <div class="section-inner">
          <router-view></router-view>
        </div>
      </section>
      <div id="toast" class="mdl-js-snackbar mdl-snackbar">
        <div class="mdl-snackbar__text"></div>
        <button class="mdl-snackbar__action" type="button"></button>
      </div>
    </main>
  </div>
</template>

<script>
  import PageBase from '@/components/pages/Page'
  import Loading from '@/components/Loading'
  import NavBar from '@/components/Navbar'

  export default {
    name: 'app',
    props: ['message', 'searchAvailable'],
    extends: PageBase,
    components: {
      navbar: NavBar,
      loading: Loading
    },
    data () {
      return {}
    },
    methods: {
      showSnackbar: function () {
        let snackbarContainer = document.querySelector('#toast')
        snackbarContainer.MaterialSnackbar.showSnackbar(this.$root)
      }
    }
  }
</script>

<style>
  #app-content {
    background: #585858;
  }

  .fade-enter-active, .fade-leave-active {
    transition: opacity .5s;
  }

  .fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */
  {
    opacity: 0;
  }
</style>
