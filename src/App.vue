<template>
  <div id="app" class="mdl-layout mdl-js-layout mdl-layout--fixed-header">
    <header class="mdl-layout__header">
      <loading></loading>
      <div class="mdl-layout__header-row">
        <span class="mdl-layout-title">Pokerface</span>
        <div class="mdl-layout-spacer"></div>
        <div class="mdl-textfield mdl-js-textfield mdl-textfield--expandable
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
      </div>
    </header>
    <navbar></navbar>
    <main class="mdl-layout__content">
      <section class="section">
        <div class="section-inner">
          <router-view></router-view>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
  import PageBase from '@/components/pages/Page'
  import Loading from '@/components/Loading'
  import NavBar from '@/components/Navbar'

  export default {
    name: 'app',
    extends: PageBase,
    components: {
      navbar: NavBar,
      loading: Loading
    }
  }
</script>

<style>
  #app{
    background: #585858;
  }
</style>
