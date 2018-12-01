<template>
  <div id="app-content" class="mdl-layout mdl-js-layout mdl-layout--fixed-header">
    <loading></loading>
    <transition name="fade-slide-up" mode="out-in">
      <header v-show="!!headerAvailable" class="mdl-layout__header">
        <div aria-expanded="false" role="button" tabindex="10"
             class="mdl-layout__drawer-button" v-on:click="back">
          <transition name="fade" mode="out-in">
            <i v-if="backAvailable" key="arrow_back" class="material-icons">arrow_back</i>
            <i v-else key="menu" class="material-icons">menu</i>
          </transition>
        </div>
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
    </transition>
    <navbar v-bind:backAvailable="backAvailable"></navbar>
    <main class="mdl-layout__content">
      <section class="section">
        <div class="section-inner">
          <transition name="fade-slide-right" mode="out-in">
            <router-view></router-view>
          </transition>
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
    props: ['message', 'searchAvailable', 'backAvailable', 'headerAvailable'],
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
      },
      nothing: function (evt) {
      },
      back: function (evt) {
        if (this.headerAvailable && this.backAvailable) {
          let layout = document.querySelector('.mdl-layout')
          layout.MaterialLayout.toggleDrawer()
          history.go(-1)
        }
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

  .fade-slide-right-enter-active {
    transition: all 0.5s ease;
  }

  .fade-slide-right-leave-active {
    transition: all 0.5s ease;
  }

  .fade-slide-right-enter, .fade-slide-right-leave-to {
    transform: translateX(40px);
    opacity: 0;
  }

  .fade-slide-up-enter-active {
    transition: all 0.5s ease;
  }

  .fade-slide-up-leave-active {
    transition: all 0.5s ease;
  }

  .fade-slide-up-enter, .fade-slide-up-leave-to {
    transform: translateY(-40px) scaleY(0);
    opacity: 0;
  }
</style>
