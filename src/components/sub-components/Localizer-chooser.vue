<template>
  <div class="mdl-navigation__link" v-on:click="switchLocales()" id="lang-switcher">
    <i class="material-icons">language</i>
    <span>{{$t("language." + $i18n.locale)}}</span>
    <ul v-if="locales.length > 2" class="mdl-menu mdl-menu--bottom-left mdl-js-menu mdl-js-ripple-effect"
        for="lang-switcher">
      <li class="mdl-menu__item" v-for="lg in otherLocales(locales)" v-on:click="setLocale(lg)">{{$t("language." + lg)}}
      </li>
    </ul>
  </div>
</template>

<script>
  import i18n, { locales, setLocale } from '@/config/i18n'
  require('material-design-lite')
  export default {
    name: 'localizerChooser',
    i18n,
    data () {
      return {
        locales: locales
      }
    },
    methods: {
      otherLocales: function (loc) {
        const vm = this
        return loc.filter(function (lg) {
          return lg !== vm.$i18n.locale
        })
      },
      currentLocale: function (loc) {
        const vm = this
        return loc.filter(function (lg) {
          return lg === vm.$i18n.locale
        })
      },
      setLocale: function (lg) {
        setLocale(lg)
      },
      switchLocales: function () {
        const vm = this
        if (this.locales.length === 2) {
          for (let lg of vm.locales) {
            if (lg !== vm.$i18n.locale) {
              setLocale(lg)
              return true
            }
          }
        }
        return false
      }
    }
  }
</script>
<style>
  #lang-switcher {
    cursor: pointer
  }
</style>
